# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:07:13 2022

@author: alexs
"""

import pandas as pd
import re
import numpy as np
import csv
def read_vcf(vcf_file, separator = '\t'):
    head_line = recognize_vcf_head(vcf_file)
    vcf = pd.read_table(vcf_file, header = head_line, sep = separator)
    vcf = vcf.set_index('ID')
    vcf = vcf.drop(['QUAL', 'FILTER', 'INFO', 'FORMAT'], axis = 1)
    locis = vcf.columns[4:]
    for loci in locis:
        vcf[loci] = vcf[loci].str.extract(r'([\d\.]/[\d\.]):*')
    return vcf
def vcf_to_genepop(vcf_file,ped_name):
    
    map_name = ped_name.split('.')[0] + '.map'
    vcf = read_vcf(vcf_file)
    locis = vcf.columns[4:]
    for loci in locis:
        rag = vcf['REF'] + vcf['ALT'] + vcf[loci]
        vcf[loci] = rag.apply(change_num_to_base)

    ped = vcf
    
    #Generate ped map file
    generate_ped_map(ped[['#CHROM','POS']],map_name)
    
    chrom_pos = vcf['#CHROM'].astype(str) + '_' +(vcf['POS']-1).astype(str) 
    ped.insert(0,'CHROM_POS', chrom_pos)
    ped = ped.drop(['REF','ALT','#CHROM', 'POS' ], axis = 1)
    
    ped = ped.T
    ped.columns = ped.iloc[0]
    
    #Change format to the ped format
    ped = ped.drop('CHROM_POS')
    ped.insert(0,'CHROMPOS',ped.index)
    
    zero_column = np.zeros(ped.index.shape).astype(int)
    for i in range (4):
        ped.insert(1,str(i),zero_column)
    ped.to_csv(ped_name, header = False, sep = '\t')
    
    #The file add " for every genotype, so we open the file and delete them
    ped_file = open('ped_test')
    new_text = ped_file.read()
    new_text = new_text.replace('"','')
    ped_file.close()
    ped_file = open('ped_test','w')
    ped_file.write(new_text)
    ped_file.close()
    
    print('Ped and map ped files were generated')
    return ped

def generate_ped_map(chrom_pos,map_name):
    zero_column = np.zeros(chrom_pos.index.shape).astype(int)
    combined_column = chrom_pos['#CHROM'].astype(str) + ':' +(chrom_pos['POS']-1).astype(str)
    chrom_pos.insert(1,'zero',zero_column)
    chrom_pos.insert(1,'combined',combined_column)
    chrom_pos.to_csv(map_name, header = False, sep  = '\t', index = False)
    
    
def change_num_to_base(ref_alt_gen):
    ref = ref_alt_gen[0]
    alt = ref_alt_gen[1]
    ref_alt_gen = ref_alt_gen.replace('0',ref)
    ref_alt_gen = ref_alt_gen.replace('1',alt)
    ref_alt_gen = ref_alt_gen.replace('/','\t')
    ref_alt_gen = ref_alt_gen.replace('.','0')
    return ref_alt_gen[2:]


def recognize_vcf_head(vcf_file):
    with open(vcf_file) as file:
        line = file.readline()
        i = 0
        while 'CHROM' not in line:
            line = file.readline()
            i += 1
    return i

usage = '''vcf2ped.py vcf_file out_file.ped'''
if __name__== '__main__':
    vcf_file = sys.argv[1]
    out_file = sys.argv[2]
    
    vcf_to_genepop(vcf_file,out_file)

else:
    print(usage)