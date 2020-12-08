import csv
import vcf
import glob

# load index ===================================================
index = open("snp_index.csv", "r")

reader = csv.reader(index)

index = []

line_count = 0
for row in reader:
    if line_count > 0:
        chrom = row[1]
        pos = int(row[2])
        index.append((chrom, pos))
    line_count += 1

data = {}

for i in index:
    data[i] = {}

# read VCFs ====================================================

# Helper function to extract individual name from filepath
def remove_prefix(my_string, prefix, suffix):
    my_string = my_string.lstrip(prefix)
    my_string = my_string.rstrip(suffix)
    return my_string

# Get list of all filenames from Poplar VCF folder
# BAR
file_list = glob.glob("../PoplarVCFsAnnotated/*.filter.vcf")
# local test
# file_list = glob.glob("../test_data/*.filter.vcf")

for f in file_list:
    # individual = remove_prefix(f, '../test_data/', '.filter.vcf')
    individual = remove_prefix(f, '../PoplarVCFsAnnotated/', '.filter.vcf')
    for snp in data.keys():
        data[snp][individual] = 0

for f in file_list:

    # extract individual name
    individual = remove_prefix(f, '../PoplarVCFsAnnotated/', '.filter.vcf')
    # individual = remove_prefix(f, '../test_data/', '.filter.vcf')
    print("reading "+individual)
    vcf_reader = vcf.Reader(open(f, 'r'))

    num_hits = 0
    num_lines = 0
    found_list = []
    hit_list = []
    num_hom_ref = 0
    num_hom_alt = 0
    num_het = 0
    for record in vcf_reader:
        chrom = record.CHROM
        pos = record.POS

        call = record.samples[0]
        snp = (chrom, pos)
        if snp not in found_list:
            if snp in index:
                found_list.append(snp)
                num_hits += 1
                if call.gt_type == 1:
                    num_het += 1
                    data[snp][individual] = 1
                elif call.gt_type == 2:
                    num_hom_alt += 1
                    data[snp][individual] = 2
        num_lines += 1

        if num_lines % 10000 == 0:
            print("read " + str(num_lines) + " lines")

    num_hom_ref = len(index) - num_het - num_hom_alt
    print(num_hom_ref)
    print(num_het)
    print(num_hom_alt)

# process dict ==================================================

# BAR
destf = open("bar_maf.csv", "w")
# local test
# destf = open("local_maf.csv", "w")
writer = csv.writer(destf)

print('writing file...')

col_names = ['genotype']
for i in index:
    col_names.append(str(i[0]).zfill(2) + '_' + str(i[1]))

writer.writerow(col_names)
print(col_names)

for f in file_list:
    # individual = remove_prefix(f, '../PoplarVCFsAnnotated/', '.filter.vcf')
    individual = remove_prefix(f, '../test_data/', '.filter.vcf')

    row = [individual.split('_')[0]]
    for snp in index:
        row.append(str(data[snp][individual]))
    writer.writerow(row)