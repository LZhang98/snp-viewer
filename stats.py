import csv
import numpy as np

data = open("data.tsv")

reader = csv.reader(data, delimiter="\t")

dest_f = open("stats.csv", "w")

num_rows = 0
num_snps_lst = []
more_than_one_lst = []

for row in reader:
    num_rows+=1
    num_snps_lst.append(int(row[2]))
    if row[2] > 1:
        more_than_one_lst.append(row[2])
    
    str_lst = row[3]
    var_lst = str_lst.strip('][').split(', ')
    for i in range(len(var_lst)):
        var_lst[i] = var_lst[i][1:-1]
    
    pos_lst = []
    for i in range(len(var_lst)):
        pos_lst.append(int(''.join(filter(str.isdigit, var_lst[i]))))

    pos_lst.sort()

    dist_lst = []
    mean_dist = 0
    if len(pos_lst) > 1:
        more_than_one_lst.append(row[2])
        for i in range(len(pos_lst)-1):
            dist_lst.append(pos_lst[i+1] - pos_lst[i])
        mean_dist=sum(dist_lst)/len(dist_lst)
    else:
        mean_dist = "NA"
    
    new_entry = row[1]+','+row[2]+','+str(mean_dist)+'\n'
    dest_f.write(new_entry)

print("frequency of >1 SNPs on a gene:", str(len(more_than_one_lst)/float(num_rows)))
print("average number of SNPs per gene:", str(sum(num_snps_lst)/float(num_rows)))

