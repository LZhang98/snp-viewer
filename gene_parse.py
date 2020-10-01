import vcf
import csv

vcf_reader = vcf.Reader(open('test_data/ALAA20-3_DNA366.filter.vcf', 'r'))

num_records = 0

snp_dict = {}

dest_f = open('data.tsv', 'w')

curr_chrom = 1
for record in vcf_reader:
    
    chrom = int(record.CHROM)
    # write to csv one chromosome at a time.
    if (chrom != curr_chrom):
        print("writing chromosome", chrom)
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
        # 4. gene name
        # 5. gene ID
        # 10. variant using HGVS notation
        # 12. cDNA pos/len
        # 13. CDS pos/len
        gene_name = fields[3]
        var = fields[9]
        cdna_pos_len = fields[11]
        if (len(cdna_pos_len) > 0):
            if (gene_name in snp_dict.keys()) :
                if (var not in snp_dict[gene_name]):
                    snp_dict[gene_name].append(var)
            else:
                snp_dict[gene_name] = [var]

print('done')
dest_f.close()