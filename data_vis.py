import matplotlib.pyplot as plt
import csv

datafile = open('snps.csv')

destd = 'figures/'

csv_reader = csv.reader(datafile)

ids = []
gene_length = []
num_snps = []
snps_per_kb = []
num_snps_unique = []
unique_snps_per_kb = []
mean_snp_spacing = []

line_count=0

for row in csv_reader:
    if line_count != 0:
        ids.append(row[0])
        gene_length.append(int(row[1]))
        num_snps.append(int(row[2]))
        snps_per_kb.append(float(row[3]))
        num_snps_unique.append(int(row[4]))
        unique_snps_per_kb.append(float(row[5]))
        if row[6] != 'nan':
            mean_snp_spacing.append(float(row[6]))
    line_count += 1

print('ids = ', len(ids))
print('mean_snp_spacing = ', len(mean_snp_spacing))

# Mean snp spacing
plt.hist(mean_snp_spacing, bins=50)
plt.xlabel('mean spacing between adjacent snps')
plt.ylabel('number of genes')
plt.title('Mean SNP Spacing')
plt.savefig(destd+'mean_snp.spacing.png')
plt.clf()

# Scatter plot for gene length
plt.scatter(gene_length,num_snps_unique)
plt.xlabel('gene length')
plt.ylabel('number of snps')
plt.title('Number of SNPS per gene')
plt.savefig(destd+'scatter.png')
plt.clf()

# Regularized unique snps
plt.hist(unique_snps_per_kb, bins=50)
plt.xlabel('regularized number of snps per gene')
plt.ylabel('number of genes')
plt.title('Regularized SNP counts')
plt.savefig(destd+'reg_num_snps_unique.png')

datafile.close()