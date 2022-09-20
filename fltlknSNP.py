# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 11:47:51 2022

@author: alexs
"""

import pandas as pd
import re
import sys
import os

def filter_linked_snp(filename,output_path = './no_linked_SNPs'):
    '''This function will return a dataframe with no linked SNP. Requieres a file file that contains 
    the linkage level between two SNPs and R2 values. 
    
    Input data must be in the next format, separator must be spaces:
     CHR_A         BP_A      SNP_A  CHR_B         BP_B      SNP_B           R2 
     0            7   975199:6      0            8    78320:7     0.344341 
     0            7   975199:6      0            8   650402:7     0.725188 
    
    
    The function return the non duplicate rows where R2>=0.8 of the first SNP column, that must be the third column
    
    '''
    filename_1 = filename.split('/')
    filename_1 = filename_1[-1] 
    
    link_data = pd.read_csv(filename, sep = r'\s+', engine = 'python')
    no_link_data = link_data[link_data['R2']>= 0.8]
    sorted_no_link = no_link_data.sort_values('SNP_A')
    no_duplica_data = sorted_no_link.iloc[:,:3].drop_duplicates()
    
    final_serie = no_duplica_data.iloc[:,2].drop_duplicates()
    
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    print('Data was filtered and file was generated at:' + output_path)
    
    outputname = output_path + '/' + filename_1
    final_serie.to_csv(outputname, index = False)
    
    return final_serie


usage = '''fltlknSNP.py linked_R2_file outputdir'''
if __name__== '__main__':
    linked_data = sys.argv[1]
    outputdir = sys.argv[2]
    
    filter_linked_snp(linked_data, outputdir)

else:
    print(usage)