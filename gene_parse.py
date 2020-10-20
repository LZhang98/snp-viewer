import vcf
import csv

vcf_reader = vcf.Reader(open('test_data/ALAA20-3_DNA366.filter.vcf', 'r'))

num_records = 0

snp_dict = {}

dest_f = open('data.tsv', 'w')

total_count = 0

curr_chrom = 1
for record in vcf_reader:

    chrom = int(record.CHROM)
    # write to csv one chromosome at a time.
    if (chrom != curr_chrom):
        print("writing chromosome " + str(chrom))
        for key in snp_dict.keys():
            num_snps = len(snp_dict[key])
            new_row = str(curr_chrom) + '\t' + key + '\t' + str(num_snps) + '\t' + str(snp_dict[key]) + '\n'
            dest_f.write(new_row)
        curr_chrom = chrom
        snp_dict = {}    
    annotations = record.INFO['ANN']

    for ann in annotations:
        fields = ann.split('|')
        
        # According to SnpEff docs, fields are (1-indexed):
        # 1. allele
        # 2. effect
        # 4. gene name
        # 5. gene ID
        # 10. variant using HGVS notation
        # 12. cDNA pos/len
        # 13. CDS pos/len
        if ('missense_variant' in fields[1]):
            gene_name = fields[3]
            gene_ID = fields[4]
            var = fields[9]
            cdna_pos_len = fields[11]
            if (gene_ID in snp_dict.keys()) :
                if (var not in snp_dict[gene_ID]):
                    snp_dict[gene_ID].append(var)
                    total_count += 1
            else:
                snp_dict[gene_ID] = [var]
                total_count += 1
    
# Write last chromosome
print("writing last chromosome")
for key in snp_dict.keys():
    num_snps = len(snp_dict[key])
    new_row = str(curr_chrom) + '\t' + key + '\t' + str(num_snps) + '\t' + str(snp_dict[key]) + '\n'
    dest_f.write(new_row)

print('counted '+ str(total_count) + ' snps')
print('done')
dest_f.close()