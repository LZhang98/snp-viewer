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

writer.writerow(['transcript_id',
                 'gene_length',
                 'num_snps',
                 'snps_per_kb',
                 'num_snps_unique',
                 'unique_snps_per_kb',
                 'mean_snp_spacing'])

num_entries = 0

#build up row by row and add
for transcript in data.keys():

    # transcript_id
    entry = [transcript]

    # gene length
    gene_length = data[transcript]["len"]
    entry.append(gene_length)

    snps = data[transcript]["pos"]

    # non-unique SNP occurences (num_snps)
    num_snps = len(snps)
    entry.append(num_snps)

    # snps_per_kb
    length_kb = float(gene_length)/1000
    snps_per_kb = num_snps/length_kb
    entry.append(round(snps_per_kb, 5))

    # unique SNP occurences (num_snps_unique)
    unique_snps = list(set(snps))
    num_unique = len(unique_snps)
    entry.append(num_unique)

    # unique snps per kb
    unique_snps_per_kb = num_unique/length_kb
    entry.append(round(unique_snps_per_kb, 5))

    # mean snp spacing
    arr = np.asarray(sorted(unique_snps))
    spacing = np.diff(arr)
    mean_spacing = np.mean(spacing)
    entry.append(round(mean_spacing, 5))

    writer.writerow(entry)

    num_entries += 1

    if num_entries % 10000 == 0:
        print("wrote " + str(num_entries) + " entries")