import math

dataFolder = '/Users/marjanfarahbod/Documents/projects/CMP984_assignmentMaterial/'
inputFile = 'pr_expression.tsv'

outputFile = dataFolder + 'pr_expression_asinh.tsv'

with open(inputFile, 'r') as input, open(outputFile, 'w') as output:
    for line in input:
        splitLine = line.split()

        v1 = math.asinh(float(splitLine[2]))
        v2 = math.asinh(float(splitLine[3]))

        output.write(splitLine[0] + '\t' + splitLine[1] + '\t' + str(v1) + '\t' + str(v2) + '\n')

        
