# in the tr_exp_geneID_selected.tsv do a few things:
# 1. merge transcripts from the same gene to the longest region
# 2. remove the fpkm
# 3. change the strand direction on the coordinate, remove the strand column
#

dataFolder = '/Users/marjanfarahbod/Documents/projects/CMP984_assignmentMaterial/'
inputFile = dataFolder + 'expFile01.csv'
outputFile1 = dataFolder + 'expFile02.csv'
outputFile2 = dataFolder + 'expFile03.csv'

input = open(inputFile, 'r')

mapping = {} # mapping of the the gene_id all the other info
with open(inputFile, 'r') as input:

    line = input.readline() # header
    for line in input:
        splitLine = line.strip().split(',')
        if splitLine[5] in mapping:
            start = min(mapping[splitLine[5]][1], int(splitLine[1]))
            end = max(mapping[splitLine[5]][2], int(splitLine[2]))
            mapping[splitLine[5]][1] = start
            mapping[splitLine[5]][2] = end
        else:
            mapping[splitLine[5]] = [splitLine[0], int(splitLine[1]), int(splitLine[2]), splitLine[3], splitLine[4]]

with open(outputFile1, 'w') as output:
    output.write('%s,%s,%s,%s,%s,%s\n' %('chromosome', 'start', 'end', 'strand', 'asinh_TPM', 'gene_id'))
    for gene in mapping:
        output.write('%s,%d,%d,%s,%s,%s\n' %(mapping[gene][0], mapping[gene][1], mapping[gene][2], mapping[gene][3],  mapping[gene][4], gene))
        
# same as above, but removing the strand and switching the start and end cor
with open(outputFile2, 'w') as output:
    output.write('%s,%s,%s,%s,%s\n' %('chromosome', 'start', 'end', 'asinh_TPM', 'gene_id'))
    for gene in mapping:
        if mapping[gene][3] == '+':
            output.write('%s,%d,%d,%s,%s\n' %(mapping[gene][0], mapping[gene][1], mapping[gene][2], mapping[gene][4], gene))
        else:
            output.write('%s,%d,%d,%s,%s\n' %(mapping[gene][0], mapping[gene][2], mapping[gene][1], mapping[gene][4], gene))

            
        
