import csv
import vcf

# load index ==================================================================
index = open("snp_index.csv", "r")

reader = csv.reader(index)

index = []

# Load in Athena's CDS-NS loci and save them as a list of tuples for reference
# Functions as index
line_count = 0
for row in reader:
    if line_count > 0:
        chrom = row[1]
        pos = int(row[2])
        index.append((chrom, pos))
    line_count += 1

# Prep for data table
data = {}
for i in index:
    data[i] = {}

# read file ====================================================================

filename = "/DATA/vcf/PoplarVCFsMerged/merged.vcf"

f = open(filename, 'r')

vcf_reader = vcf.Reader(f)

found_list = []
# Allele frequence stored in AF field of INFO
for record in vcf_reader:

    chrom = record.CHROM
    pos = record.POS

    snp = (chrom, pos)
    if snp in index:
        found_list.append(snp)
        print("found", snp)
        data[snp] = record.INFO['AF']

# process dict ===================================================================

destf = open('vcftools_merge_data.csv', 'w')
writer = csv.writer(destf)

print('printing file...')

row = []
for snp in data.keys():
    row.append(snp)
    row.append(data[snp])

writer.writerow(row)