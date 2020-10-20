import json
import csv

db = open('db_alt.json','r')

destf = open('snps.json','w')

print('loading database')
data = json.load(db)
genes = {}

# extracting positions
print('building snp dict')
snps = {}
for chrom in data.keys():
    print(chrom)
    snps[chrom] = {}
    for gene_name in data[chrom].keys():
        pos_lst = []
        for entry in data[chrom][gene_name]:
            var = entry['variant']
            # extract pos from variant "c.[pos]X>X"
            pos = int(var[2:-3])
            pos_lst.append(pos)
        
        snps[chrom][gene_name] = sorted(pos_lst)

print('dumping json')
json.dump(snps, destf, sort_keys=True, indent=2)

db.close()
destf.close()
print('done')