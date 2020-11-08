import json
import csv

db = open('db_alt.json','r')

destf = open('snps.json','w')

print('loading database')
data = json.load(db)

# extracting positions
print('building snp dict')
snps = {}
for transcript in data.keys():
    snps[transcript] = {}
    pos_lst = []
    for entry in data[transcript]:
        var = entry['var']
        # extract pos from variant "c.[pos]X>X"
        pos = int(var[2:-3])
        pos_lst.append(pos)
        
        # get gene length: denominator of fraction
        snps[transcript]["len"] = int(entry['length'].split("/")[1])
        snps[transcript]["pos"] = sorted(pos_lst)

print('dumping json')
json.dump(snps, destf, sort_keys=True, indent=2)

db.close()
destf.close()
print('done')