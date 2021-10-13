# the code is just to put together the final file

# adding expression levels to the genomic coordinate file
#############
dataFolder = '/Users/marjanfarahbod/Documents/projects/CMP984_assignmentMaterial/'
inputFile1 = dataFolder + 'pr_V38_wholeGene_hg38' # genomic coordinates, transcript IDs for pilot region
inputFile2 = dataFolder + 'pr_expression_asinh.tsv' # gene_id, transcript_ids, tpm, fpkm
outputFile = dataFolder + 'tr_exp.tsv' # output 

mapping = {} # mapping of transcript ids to both tpm and fpkm expression levels 
with open(inputFile2, 'r') as file2:
    for line in file2:
        splitLine = line.strip().split('\t')
        for tid in splitLine[1].split(','):
            mapping[tid] = (splitLine[2], splitLine[3])


# print(mapping)

with open(inputFile1, 'r') as file1, open(outputFile, 'w') as output:
    for line in file1:
        splitLine = line.split('\t')
        id = splitLine[7]
        if id in mapping:
            output.write('%s\t%s\t%s\n' %(line.strip(), mapping[id][0], mapping[id][1]))
            
# making the final file, with gene_ids (I could use the original expression file to get the gene_ids)
###############
inputFile1 = dataFolder + 'tr_exp.tsv'
inputFile2 = dataFolder + 'pr_mart_export'
outputFile = dataFolder + 'tr_exp_geneID_selected.csv'

mapping = {}
with open(inputFile2, 'r') as file2:
    for line in file2:
        splitLine = line.strip().split('\t')
        tid = splitLine[3]
        mapping[tid] = (splitLine[1])

# print(mapping)

with open(inputFile1, 'r') as file1, open(outputFile, 'w') as output:
    output.write('%s,%s,%s,%s,%s,%s,%s,%s\n' %('chromosome', 'start', 'end', 'transcript_id', 'strand', 'asinh_TPM', 'asinh_FPKM', 'gene_id'))
    for line in file1:
        splitLine = line.strip().split('\t')
        tid = splitLine[7]
        if tid in mapping:
            output.write('%s,%s,%s,%s,%s,%s,%s,%s\n' %(splitLine[4],splitLine[5],splitLine[6],splitLine[7],splitLine[9],splitLine[16],splitLine[17], mapping[tid]))
        else:
            output.write('%s,%s,%s,%s,%s,%s,%s,%s\n' %(splitLine[4],splitLine[5],splitLine[6],splitLine[7],splitLine[9],splitLine[16],splitLine[17], ' '))

