# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 15:07:13 2022

@author: alexs
"""

import pandas as pd
import sys 

def vcf_to_stru(vcf_file, pop_map ,stru_out, separator = '\t',):
    '''This function convert a vcf file to a struc file'''
    
    head_line = recognize_vcf_head(vcf_file)
    vcf = pd.read_table(vcf_file, header = head_line, sep = separator)
    vcf = vcf.set_index('ID')
    locis = vcf.columns[8:]
    stru = pd.DataFrame()

    for loci in locis:
        stru[loci] = vcf[loci].apply(get_GT)
    all1, all2 = separate_alleles(stru)
    all1['REF'] = vcf['REF'] 
    all1['ALT'] = vcf['ALT']
    
    all2['REF'] = vcf['REF'] 
    all2['ALT'] = vcf['ALT']
    
    all1 = replace_bases(all1, locis)
    all2 = replace_bases(all2, locis)
    all1 = all1.drop(['REF','ALT'], axis = 1)
    all2 = all2.drop(['REF','ALT'], axis = 1)
    structure_file = all1.T.iloc[[0,1]]
    structure_file = structure_file.drop(structure_file.index)

    for index in all1.T.index:
        i = 0
        structure_file.loc[str(i) + index] = all1.T.loc[index]
        i+= 1
        structure_file.loc[str(i) + index] = all2.T.loc[index]
    structure_file.index = [id[1:] for id in structure_file.index]
    
    pop_dict = read_pop_map(pop_map)
    sample_column = structure_file.index.to_series().map(pop_dict)
    structure_file.insert(0,column = '', value = sample_column)
    structure_file.to_csv(stru_out, sep = '\t')
    return structure_file

def read_pop_map(pop_map):
    pop_file = pd.read_table(pop_map, header = None, sep = '\t')
    pop_file = pop_file.drop_duplicates()
    pop_file = pop_file.set_index(0)
    pop_file[1].to_dict()
    return pop_file[1].to_dict()
    
    
def recognize_vcf_head(vcf_file):
    with open(vcf_file) as file:
        line = file.readline()
        i = 0
        while 'CHROM' not in line:
            line = file.readline()
            i += 1
    return i
def get_GT(loci):
    return loci[:3]
def drop_GT(GT):
    return GT[0]
def drop_get(GT):
    return GT[-1]

def separate_alleles(stru_file):
    all1 = pd.DataFrame()
    all2 = pd.DataFrame()
    for loci in stru_file.columns:
        all1[loci] = stru_file[loci].apply(drop_GT)
        all2[loci] = stru_file[loci].apply(drop_get)
    return all1, all2
def replace_bases(stru, locis):
    mut_stru_dict = {'.':0, 'A':1,'T':2,'G':3,'C':4}
    for loci in locis:
        stru.loc[stru[loci] == '0',loci] = stru[stru[loci] == '0']['REF']
        stru.loc[stru[loci] == '1',loci] = stru[stru[loci] == '1']['ALT']
        stru[loci] = stru[loci].map(mut_stru_dict)
    return stru

usage = '''vcf2stru.py vcf_file pop_map out_file.stru'''
if __name__== '__main__':
    vcf_file = sys.argv[1]
    pop_file = sys.argv[2]
    out_file = sys.argv[3]
    
    vcf_to_stru(vcf_file, pop_file, out_file)

else:
    print(usage)