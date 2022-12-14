# -*- coding: utf-8 -*-
"""
author: Alex F. Sanchez
December 14, 2022
"""
import sys
import os
import random

def get_sub_sample(filename,in_path,out_path,n,prefix):
    file = open(in_path +'/'+filename).readlines()
    outfile = open(out_path + '/' + prefix + filename,'w') 
    sub = random.sample(file,n)
    for line in sub:
        outfile.write(line)
    outfile.close()
def do_multiple_files(in_path,out_path,n,prefix):
    isExist = os.path.exists(out_path)
    if not isExist:
        os.makedirs(out_path)
    for file in os.listdir(in_path):
        get_sub_sample(file,in_path,out_path,n,prefix)
    print('Subsamples were generated!')



usage = '''python SNP_subgen.py in_path out_path n prefix

            in_path: Path to the folder that contain the whitelist
            out_path: Path to the folder where subsamples will be generated
            n: number of subsamples 

            It is important to DO NOT include '/' at the end of the paths'''
if __name__== '__main__':
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    n = int(sys.argv[3])
    prefix = sys.argv[4]
    do_multiple_files(in_path,out_path,n,prefix)

else:
    print(usage)