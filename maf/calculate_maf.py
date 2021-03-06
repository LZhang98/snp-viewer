import csv
import vcf
import glob
import sys

# set bar or local ============================================================

# VIA COMMAND LINE ARGUMENT
if sys.argv[1] == "bar":
    print("set bar config")
    (bar, local) = (True, False)
elif sys.argv[1] == "local":
    print("set local machine config")
    (bar, local) = (False, True)

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

# read VCFs ===================================================================

# Helper function to extract individual name from filepath
def remove_prefix(my_string, prefix, suffix):
    my_string = my_string.lstrip(prefix)
    my_string = my_string.rstrip(suffix)
    return my_string

# Get list of all filenames from Poplar VCF folder
if bar:
    file_list = glob.glob("../../PoplarVCFsAnnotated/*.filter.vcf")
elif local:
    file_list = glob.glob("../test_data/*.filter.vcf")

print(file_list)

# Initialize array of 0s for classifying SNPs per locus per genotype
for f in file_list:

    if local:
        individual = remove_prefix(f, '../test_data/', '.filter.vcf')
    elif bar:
        individual = remove_prefix(f, '../../PoplarVCFsAnnotated/', '.filter.vcf')

    for snp in data.keys():
        data[snp][individual] = 0

total_files = len(file_list)
num_files = 1

# Start reading each file proper
for f in file_list:

    # extract individual name
    if local:
        individual = remove_prefix(f, '../test_data/', '.filter.vcf')
    elif bar:
        individual = remove_prefix(f, '../../PoplarVCFsAnnotated/', '.filter.vcf')

    print("reading " + individual + " " + str(num_files) + "/" + str(total_files))

    vcf_reader = vcf.Reader(open(f, 'r'))

    num_hits = 0
    num_lines = 0
    found_list = []
    hit_list = []
    num_hom_ref = 0
    num_hom_alt = 0
    num_het = 0

    # for each record in the vcf:
    # 1. Check that this line isn't a duplicate (check that the locus has been processed before)
    # 2. Check that this locus is in our index of interest
    # 3. Add its gt_type field (0, 1, 2) to our data table (while counting for testing purposes)

    # UPDATE:
    # Use call.data.GT to get 0/1, 1/1, etc directly to count minor allele

    # UPDATE 2:
    # Get raw gt directly written into table (just to make sure counting is right)
    for record in vcf_reader:
        chrom = record.CHROM
        pos = record.POS

        call = record.samples[0]

        # print(call.data.GT)
        gt = call.data.GT
        snp = (chrom, pos)
        if snp not in found_list:
            if snp in index:
                found_list.append(snp)
                num_hits += 1
                # if call.gt_type == 1:
                #     num_het += 1
                #     data[snp][individual] = 1
                # elif call.gt_type == 2:
                #     num_hom_alt += 1
                #     data[snp][individual] = 2
                # if gt == "0/1":
                #     num_het += 1
                #     data[snp][individual] = 1
                # elif gt == "1/1":
                #     num_hom_alt += 1
                #     data[snp][individual] = 2

                gt_new = gt.replace("/", ".")
                data[snp][individual] = gt_new
                
        num_lines += 1

        # Make sure the code isn't slowing down over time
        if num_lines % 10000 == 0:
            print("read " + str(num_lines) + " lines")

    num_hom_ref = len(index) - num_het - num_hom_alt
    print(num_hom_ref)
    print(num_het)
    print(num_hom_alt)
    num_files += 1

# process dict =======================================================================

# Write data table into CSV
if bar:
    destf = open("bar_maf.csv", "w")
elif local:
    destf = open("local_maf.csv", "w")

writer = csv.writer(destf)

print('writing file...')

col_names = ['genotype']
for i in index:
    col_names.append(str(i[0]).zfill(2) + '_' + str(i[1]))

writer.writerow(col_names)

for f in file_list:
    if local:
        individual = remove_prefix(f, '../test_data/', '.filter.vcf')
    elif bar:
        individual = remove_prefix(f, '../../PoplarVCFsAnnotated/', '.filter.vcf')

    row = [individual.split('_')[0]]
    for snp in index:
        row.append(str(data[snp][individual]))
    writer.writerow(row)
