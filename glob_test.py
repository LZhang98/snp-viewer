import json
import glob

# Helper function to extract individual name from filepath
def remove_prefix(my_string, prefix, suffix):
    my_string = my_string.lstrip(prefix)
    my_string = my_string.rstrip(suffix)
    return my_string

file_list = glob.glob("../PoplarVCFsAnnotated/*.filter.vcf")

data = {}

destf = open('main_db.json', 'w')

for f in file_list:
    individual = remove_prefix(f, '../PoplarVCFsAnnotated/', '.filter.vcf')
    curr_individual = {}
    print("reading "+individual)
