# CMPT984-dataprep

# CMP 984 assignment data prep notes

The idea is that the students will build a model for epigenomic clustering similar to Segway, using a manageable, curated data set. I'd like to give two files to students:

(1) CSV file of genomic positions x epigenetic marks. Binned to 100 bp and restricted to the ENCODE pilot regions. Six histone marks: H3K4me3, H3K4me1, H3K36me3, H3K27me3, H3K9me3, H3K27ac. Asinh signals. Data from GM12878, or any other reasonable cell type.

(2) CSV file of genes x genomic position + asinh RNA-seq expression.

## item (1):

## item (2):

### 1. Getting the files

**File1: the expression data**

I got the expression file from ENCODE website labeled as gene quantification. There are two files, I got the one with the star at the Default column, no clue what it means. 

File name: ENCFF345SHY.tsv. **

Snapshot of header: 

![Screen Shot 2021-10-11 at 12.56.58 PM.png](https://github.com/marjanfarahbod/CMPT984-dataprep/blob/main/Screen_Shot_2021-10-11_at_12.56.58_PM.png)

I am not sure what are the gene_ids and transcript_ids in the first few thousands first lines, but after that they are ensembl IDs. At first I thought they are HGNC id(here [https://www.genenames.org/about/](https://www.genenames.org/about/) ) so I got the mapping of HGCN to ensembl from the biomart (kept it here since "getting the mappings from biomart comes up here and there")

**File2: the pilot region** 

We need the genes in the pilot region. The pilot region is ~30milbp, about 1% of the genome, in 44 chucks from 21 chromosomes (all minus 3, 17, y). Here [http://hgdownload.cse.ucsc.edu/goldenpath/hg19/encodeDCC/referenceSequences/encodePilotRegions.hg19.bed](http://hgdownload.cse.ucsc.edu/goldenpath/hg19/encodeDCC/referenceSequences/encodePilotRegions.hg19.bed)

Filename: encodePilotRegions.hg19.bed

**File3: genomic coordinates**

We get this from ucsc table browser. From genome.ucsc.edu, in "Tools", select "table browser", here: [https://genome.ucsc.edu/cgi-bin/hgTables](https://genome.ucsc.edu/cgi-bin/hgTables). Select the desired dataset/region. Check out the table schema to see what the file will look like and "get the output". 

Filename: V38_wholeGene_hg38 (this has the genomic coordinates without exonic regions)

Filename: V38_exonplus02 (genomic coordinates with exonic regions, we don't need it for this project) - to get this file, in the output page you must pick "exon plus". 

Other settings: 

![Screen Shot 2021-10-11 at 4.50.18 PM.png](https://github.com/marjanfarahbod/CMPT984-dataprep/blob/main/Screen_Shot_2021-10-11_at_12.56.58_PM.png)

**File4: the mapping of the gene IDs (HGNC) to gene Ensembl IDs and transcript Ensembl IDs**

We get that from [ensembl.org](http://ensembl.org) ([https://www.ensembl.org/biomart/martview](https://www.ensembl.org/biomart/martview/0bc2019d6be77ce081d9d383026b81ff)). Choose the database as "Ensembl Genes 104", Choose the organism "Human genes (GRCH38.p13)"

Filename: mart_export.txt

### 2. Select the genomic coordinates in the pilot region, using bedtools

We used bedtools for this part. It's a great tool for working with .bed files, here [https://bedtools.readthedocs.io/en/latest/](https://bedtools.readthedocs.io/en/latest/) 

bedtool command used: bedtools intersect -wa -wb -a encodePilotRegions.hg19.bed -b V38_wholeGene_hg38 > pr_V38_wholeGene_hg38

3,424 genes are selected from file 3-1. output file name: pr_V38_wholeGene_hg38.bed. 

20,057 exons are selected, from file 3-2. output file name: pr_V38_exonplus02.bed 

### 3. Get the transcript values for the pilot region

get the transcript IDs:

>> awk '{print$8}' pr_V38_wholeGene_hg38 > pr_ensemblDs

get the relevant columns from the expression file:

>> awk '{print$1, $2, $8,$9}' ENCFF345SHY.tsv > expression_selectColumns.tsv

filter the expression file for the transcript IDs:

>> grep -F -f pr_ensemblIDs expression_selectColumns.tsv > pr_expression.tsv

### 4. Get the asinh for expression

from asinhCode.py  I get pr_expression_asinh.tsv. 

### 5. Put together the final file

from the finalTogether.py I get pr_exp_geneID_selected.csv
