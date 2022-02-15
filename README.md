# snp_format_convertor

This repository contains Python programs that change the snp file format such as: vcf, stru.

### vcf2stru

This program convert a vcf file into a stru file. It requieres a population map file in order to work.
Currently, the program just support vcf with two alleles.
The pop file format must be in the next format
~~~
sample1 1
sample2 2
sample3
~~~
