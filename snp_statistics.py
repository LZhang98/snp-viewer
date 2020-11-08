"""
Run after snps_per_gene.py

Given a database of snp pos and gene length per gene, compute occurrence stats.
Write the result to a csv.

Input: snps.json

Output: snps.csv
"""

import json
import csv
import numpy as np

db = open('snps.json','r')

destf = open('snps.csv','w')

writer = csv.writer(destf, delimiter=',')

print('loading database')
data = json.load(db)

writer.writerow(['transcript_id', 'gene_length','num_snps','num_snps_unique', 'mean_snp_spacing'])

num_entries = 0
for transcript in data.keys():
    entry = [transcript]
    snps = data[transcript]

    # TODO: gene length
    # perhaps read separately

    # non-unique SNP occurences
    entry.append(len(snps))

    # unique SNP occurences
    unique_snps = list(set(snps))
    entry.append(len(unique_snps))

    # mean snp spacing
    arr = np.asarray(unique_snps)
    spacing = np.diff(arr)
    mean_spacing = np.mean(spacing)
    entry.append(mean_spacing)

    writer.writerow(entry)

    num_entries += 1

    if num_entries % 10000 == 0:
        print("wrote " + str(num_entries) + " entries")