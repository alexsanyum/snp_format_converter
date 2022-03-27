# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 15:07:13 2022

@author: alexs
"""


import pandas as pd
import re
import numpy as np
import sys 

def read_vcf(vcf_file, separator = '\t'):
    head_line = recognize_vcf_head(vcf_file)
    vcf = pd.read_table(vcf_file, header = head_line, sep = separator)
    vcf = vcf.set_index('ID')
    vcf = vcf.drop(['QUAL', 'FILTER', 'INFO', 'FORMAT'], axis = 1)
    locis = vcf.columns[4:]
    for loci in locis:
        vcf[loci] = vcf[loci].str.extract(r'([\d\.]/[\d\.]):*')
    return vcf

def vcf_to_genepop(vcf_file, popmap,genepop_name):
    pop_map_dict = read_pop_map(popmap)
    vcf = read_vcf(vcf_file)
    locis = vcf.columns[4:]
    for loci in locis:
        rag = vcf['REF'] + vcf['ALT'] + vcf[loci]
        vcf[loci] = rag.apply(change_num_to_base)

    genepop = vcf
    chrom_pos = vcf['#CHROM'].astype(str) + '_' +(vcf['POS']-1).astype(str) 
    genepop.insert(0,'CHROM_POS', chrom_pos)
    genepop = genepop.drop(['REF','ALT','#CHROM', 'POS' ], axis = 1)
    
    for loci in locis:
        genepop[loci] = genepop[loci].apply(change_base_to_genepop_number)
    
    genepop = genepop.T
    genepop.columns = genepop.iloc[0]
    genepop.head(1).to_csv(genepop_name, header = False, index  = False, sep  = '\t')
    for pop in pop_map_dict:
        with open(genepop_name,'a') as f:
            f.write('pop' + '\n')
            f.close()
        genepop.loc[pop_map_dict[pop]].to_csv(genepop_name, 
                                               header = False, 
                                               index  = True, 
                                               sep  = '\t', 
                                               mode = 'a')
    print('File was generated')
    return genepop


def change_num_to_base(ref_alt_gen):
    ref = ref_alt_gen[0]
    alt = ref_alt_gen[1]
    ref_alt_gen = ref_alt_gen.replace('0',ref)
    ref_alt_gen = ref_alt_gen.replace('1',alt)
    ref_alt_gen = ref_alt_gen.replace('/','')
    return ref_alt_gen[2:]

def change_base_to_genepop_number(genotype):
    bases_dict = {'A':'01','T':'02','G':'03','C':'04','.':'00'}
    genepop_code = ''
    for base in genotype:
        genepop_code += bases_dict[base]
    return genepop_code
        
    
def read_pop_map(popmap, separator = '\t'):
    popdf = pd.read_table(popmap, sep = separator, header = None)
    popdf = popdf.drop_duplicates()
    unique_pops = popdf[1].unique()
    pop_dict = {}
    for unique_pop in unique_pops:
        pop_dict[unique_pop] =  popdf[popdf[1] == unique_pop][0].values.tolist()
    return pop_dict
def recognize_vcf_head(vcf_file):
    with open(vcf_file) as file:
        line = file.readline()
        i = 0
        while 'CHROM' not in line:
            line = file.readline()
            i += 1
    return i

usage = '''vcf2genepop.py vcf_file pop_map out_file.genepop'''
if __name__== '__main__':
    vcf_file = sys.argv[1]
    pop_file = sys.argv[2]
    out_file = sys.argv[3]
    
    vcf_to_genepop(vcf_file, pop_file,out_file)

else:
    print(usage)