import pandas as pd
import sys 
import numpy as np


def read_stru(stru_file):
    '''This function read a structure file and return the matrix with no populations column and bases instead of numbers'''
    
    #Ignore metadata if exist
    header = True
    i = 0
    file = open(stru_file)
    while header:
        line = file.readline()
        if '#' not in line:
            header = False
        else:
            i += 1
    file.close()

    mut_stru_dict = {0:'.', 1:'A',2:'T',3:'G',4:'C'}
    
    stru = pd.read_table(stru_file,sep = '\t', skiprows=i)
    mut_stru_dict = {0:'.', 1:'A',2:'T',3:'G',4:'C'}
    df = stru.iloc[:,2:].applymap(lambda x: mut_stru_dict[x])
    df = df.set_index(stru.iloc[:,0])
    return df

def generated_phy(stru_file):
    readed_stru = read_stru(stru_file)
    
    #Combine alleles into one row
    readed_stru = readed_stru.groupby(readed_stru.index).agg('sum')
    readed_stru = readed_stru.applymap(lambda x: ''.join(sorted(x)))
    stru_phy_dict = {'AA':'A', 'TT':'T','CC':'C','GG':'G', '..':'?',
                     'AT':'W', 'AG':'R','AC':'M',
                     'GT':'K', 'CT':'Y','CG':'S'}
    phy_df = readed_stru.applymap(lambda x: stru_phy_dict[x])
    
    
    return phy_df

def write_phy(stru_name,out_name):
    phy_df = generated_phy(stru_name)
    phy_df = phy_df[phy_df.columns].T.agg(''.join)
    
    n_samples = len(phy_df)
    n_gts = len(phy_df[0])
    header = '{0} {1}\n'.format(n_samples,n_gts)
    
    file = open(out_name,'w')
    file.write(header)
    file.close()
    phy_df.to_csv(out_name,sep = ' ', mode = 'a', header = False)
    print('Phy file was generated succesfully')

usage = '''vcf2phy.py stru_file out_file.phy'''
if __name__== '__main__':
	stru_file = sys.argv[1]
	out_file = sys.argv[2]
	write_phy(stru_file,out_file)

else:
    print(usage)