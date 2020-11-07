import json
import vcf
import glob

# Helper function to extract individual name from filepath
def remove_prefix(my_string, prefix, suffix):
    my_string = my_string.lstrip(prefix)
    my_string = my_string.rstrip(suffix)
    return my_string

# Get list of all filenames from Poplar VCF folder
file_list = glob.glob("../PoplarVCFsAnnotated/*.filter.vcf")

# db built here:
data = {}

# json database will be written here:
destf = open('main_db.json', 'w')

# tracking important stats will be written here:
tracking = open('tracking.txt', 'w')

# for each file in the glob list:
for f in file_list:

    # extract individual name
    individual = remove_prefix(f, '../PoplarVCFsAnnotated/', '.filter.vcf')

    # build up a database for the current file/individual, then add it to the main data dict
    curr_individual = {}

    print("reading "+individual)
    vcf_reader = vcf.Reader(open(f, 'r'))

    total_count = 0
    num_duplicates = 0

    for record in vcf_reader:

        annotations = record.INFO['ANN']
        for ann in annotations:
            fields = ann.split('|')
            duplicate = False
            # According to SnpEff docs, fields are (1-indexed):
            # 1. allele
            # 2. effect
            # 4. gene name
            # 5. gene ID
            # 7. feature ID
            # 10. variant using HGVS notation
            # 12. cDNA_position / cDNA_len
            if ('missense_variant' in fields[1]):
                chrom = record.CHROM

                transcript_id = fields[6]
                entry = {
                    'var': fields[9],
                    'individual': individual,
                    'chrom': chrom,
                    'length': fields[11]
                }

                if (transcript_id not in curr_individual):
                    curr_individual[transcript_id] = [entry]
                    total_count += 1
                else:
                    for snp in curr_individual[transcript_id]:
                        if snp['var'] == entry['var']:
                            duplicate = True
                            num_duplicates += 1
                            break
                    
                    if not duplicate:
                        curr_individual[transcript_id].append(entry)
                        total_count += 1
                
                if (total_count % 5000 == 0 and not duplicate):
                    print('added ' + str(total_count) + ' entries')
    
    # WRITE STATS
    print('writing stats')
    tracking.write(individual+':\n')
    tracking.write('number of snps added: '+str(total_count)+'\n')
    print('number of snps added: '+str(total_count))
    tracking.write('number of dupes removed: '+str(num_duplicates)+'\n')
    print('number of dupes removed: '+str(num_duplicates))

    # Now combine curr_individual dict into data
    for transcript in curr_individual.keys():
        if transcript not in data:
            data[transcript] = curr_individual[transcript]
        else:
            data[transcript].extend(curr_individual[transcript])

print('dumping json')
json.dump(data, destf, sort_keys=True, indent=2)
destf.close()
tracking.close()
print('done')