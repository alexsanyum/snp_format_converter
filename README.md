# snp_format_convertor

This repository contains Python programs that change the snp file format from vcf to genepop, structure, and ped.

All programs support two alleles files. To convert to structure and genepop it is requiered a population file in the next format:

~~~
sample1 1
sample2 1
sample3 2
sample3 2
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
