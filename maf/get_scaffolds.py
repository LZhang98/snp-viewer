import csv

index = [
    "scaffold_1_25051104",    "scaffold_2_3156956",    "scaffold_2_8329767",
    "scaffold_3_13279794",    "scaffold_3_14451224",    "scaffold_3_15213042",
    "scaffold_4_7478176",    "scaffold_5_13994673",    "scaffold_6_23164577",
    "scaffold_6_24767093",    "scaffold_6_2489698",    "scaffold_6_25893186",
    "scaffold_6_25893407",    "scaffold_6_3756001",    "scaffold_7_14802316",
    "scaffold_7_14891160",    "scaffold_8_5198105",    "scaffold_8_6568803",
    "scaffold_8_8018360",    "scaffold_9_12818481",    "scaffold_9_2160922",
    "scaffold_10_15938437",    "scaffold_10_19078879",    "scaffold_10_19080923",
    "scaffold_10_19215715",    "scaffold_12_1814799",    "scaffold_12_2876156",
    "scaffold_13_1353254",    "scaffold_13_2018492",    "scaffold_13_3764023",
    "scaffold_14_9522855",    "scaffold_15_14137531",    "scaffold_15_14342360",
    "scaffold_15_247054",    "scaffold_15_247811",    "scaffold_15_382827",
    "scaffold_15_718240",    "scaffold_16_1404",    "scaffold_16_905064",
    "scaffold_17_12392091",    "scaffold_17_5220579",    "scaffold_18_6191825",
    "scaffold_143_2955"
]
source = open('s1b.csv', 'r')

reader = csv.reader(source)

destf = open('reference_mafs.csv', 'w')

writer = csv.writer(destf)

line_count = 0

for row in reader:
    if line_count == 9:
        writer.writerow(row)

    if line_count > 9:
        if row[0] in index:
            writer.writerow(row)
    line_count += 1

source.close()
destf.close()