import json
import vcf

individuals = [
    'ALAA20-3_DNA366',
    'BELA18-1_DNA57', 
    'BELA18-3_DNA58',
    'BELA18-4_DNA59',
    'BELC18-1_DNA127',
    'BELC18-2_DNA128',
    'BELC18-4_DNA129'
]

data = {}

destf = open('db.json', 'w')
tracking = open('tracking.txt', 'w')

for individual in individuals:
    print("reading "+individual)
    vcf_reader = vcf.Reader(open('test_data/'+individual+'.filter.vcf', 'r'))
    data[individual] = {}

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
            if ('missense_variant' in fields[1]):
                chrom = record.CHROM
                if chrom not in data[individual].keys():
                    data[individual][chrom] = {}

                gene_name = fields[3]
                entry = {
                    'transcript_id': fields[6],
                    'variant': fields[9]
                }

                if (gene_name not in data[individual][chrom].keys()):
                    data[individual][chrom][gene_name] = [entry]
                    total_count += 1
                else:
                    # removing duplicates by checking previously entered entries
                    # define duplicate: two snps share the same position and mutation
                    # maybe same transcript id?
                    for snp in data[individual][chrom][gene_name]:
                        if snp['variant'] == entry['variant']:
                            duplicate = True
                            num_duplicates += 1
                            break

                    if not duplicate:
                        data[individual][chrom][gene_name].append(entry)
                        total_count += 1

                if (total_count % 5000 == 0 and not duplicate):
                    print('added '+str(total_count)+' entries')
        
    print('writing stats')
    tracking.write(individual+':\n')
    tracking.write('number of snps added: '+str(total_count)+'\n')
    print('number of snps added: '+str(total_count))
    tracking.write('number of dupes removed: '+str(num_duplicates)+'\n')
    print('number of dupes removed: '+str(num_duplicates))

print('dumping json')
json.dump(data, destf, sort_keys=True, indent=2)
destf.close()
tracking.close()
print('done')