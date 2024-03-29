# snp_format_converter

This repository contains Python programs that change the snp file format from vcf to genepop, structure, and ped.

All programs support two alleles files. To convert to structure and genepop it is requiered a population file in the next format:

~~~
sample1 1
sample2 1
sample3 2
sample4 2
~~~

vcf format must follow:
~~~
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	sample1	sample2	sample3
1 123	id	T	C	.	PASS	NS=69;AF=0.500	GT:DP:AD:GQ:GL	0/1:17:7,10:40:-29.93,0.00,-19.83	0/1:15:9,6:40:-17.31,0.00,-27.04	./.
~~~

### vcf2stru

How to use :
~~~
vcf2stryu.py vcf_file pop_file out_file.stru
~~~

### vcf2genepop

How to use :
~~~
vcf2genepop.py vcf_file pop_file out_file.genepop
~~~

### vcf2ped

This program generated both ped and map file

How to use :
~~~
vcf2genepop.py vcf_file out_file.ped
~~~

### stru2phy

This program generated a phylip file from a struc file.

How to use:
~~~
stru2phy.py stru_file out_file
~~~

### fltlknSNP.py 
This program use a linkage matrix of SNPs to filter linkage raws. 

Its produce a one colunm file with unique no linkage SNP. 
How to use:
~~~
fltlknSNP.py filename out_folder
~~~

### SNP_subgen.py 
This program allow to generate a subsample from a SNP whitelist file. 

Its produce a new whitelist that contain the random subsample.

The program takes a folfer that contain one or multiple files and crete new files in a new or existing folder
How to use:
~~~
python SNP_subgen.py in_path out_path n prefix
~~~
