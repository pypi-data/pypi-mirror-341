
################################################################
################## Load python packages ###########################
################################################################
import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import scanpy as sc
import scanpy.external as sce
import sys
import scipy.stats
import os
from IPython.display import display
from pandas import option_context

################################################################
################## TO RUN R PACKAGES ###########################
################################################################


#DEG analysis and saving dotplot with 10 genes in each cluster
def deg_analysis_for_20_genes_and_as_gmt_file(adata):
    #ask user to provide key_added string name
    key_added_in_adata = (input('how you want to add key into adata:' ))
    #key_added_in_adata = (input('how you want to add key into adata:' ))

    #ask user for groupby category
    groupby_in_adata = (input('provide groupby clusters:' ))
    #groupby_in_adata = "'{}'".format(groupby_in_adata)
    
    
    sc.tl.rank_genes_groups(adata, groupby=groupby_in_adata, method='wilcoxon', pts = True, key_added = key_added_in_adata)

    #Return only adjusted p-values below the cutoff.
    deg = sc.get.rank_genes_groups_df(adata, group = None, key=key_added_in_adata, pval_cutoff=0.05, log2fc_min=0.5)

    #print(f'Genes in each cluster:\n{deg['group'].value_counts()}')
    print(deg['group'].value_counts())

    deg = deg.rename(columns={'group':'clusters'})
    deg['pct_diff'] = deg.pct_nz_group - deg.pct_nz_reference
    deg = deg.groupby('clusters', as_index=False).apply(lambda x: x.sort_values('logfoldchanges', ascending=False))
    deg = deg.groupby('clusters', as_index=False).apply(lambda x: x.sort_values('pct_diff', ascending=False))
    deg = deg.reset_index()
    
    #printing nicely
    with option_context('display.max_rows', 50, 'display.max_columns', 100):
        display(deg)
    
    #global deg20
    # getting top 20 markers in each cluster
    deg20 = deg.groupby('clusters').head(20)
    
    #removing unnecessary columns
    deg20.drop(columns=['level_0', 'level_1', 'level_2'], inplace=True)
    
    #printing df nicely
    with option_context('display.max_rows', 50, 'display.max_columns', 100):
        display(deg20)
    
    #making markers as global variable
    #global markers
    markers = deg20.groupby('clusters')['names'].apply(list).to_dict()

     #converting to df and transposed
    markers = pd.DataFrame(markers).T
    #adding N/A
    markers.insert(0, '', 'N/A')
    
    #saving as .txt file
    markers.to_csv('top20_genes_in_cell_types.txt', sep=' ',header=False)
    
    #converting .txt file to .gmt
    ####################################### #######################################
        # Read space-separated text file
    with open('top20_genes_in_cell_types.txt', 'r') as file:
        lines = file.readlines()

    # Process the lines to create the GMT format
    gmt_data = []
    for line in lines:
        elements = line.strip().split(' ')
        gene_set_name = elements[0]
        #description = ''  # Add description if available in the input file
        genes = elements[1:]  # Assuming genes start from the second element onwards
        gmt_entry = [gene_set_name] + genes
        gmt_data.append(gmt_entry)

    # Save as GMT file
    with open('top20_genes_in_cell_types.gmt', 'w') as gmt_file:
        for entry in gmt_data:
            gmt_file.write('\t'.join(entry) + '\n')
    #######################################  #######################################
    
    #print(adata)
    return deg20,markers



#wrting function

def volcano_plot_sample_types_csv(adata):
    
    cluster_name = (input('provide_cluster_name:'  ))
    obs_column = (input('cell type label column:'  ))
    
    obj = adata[adata.obs.obs_column == cluster_name]
    
    sc.tl.rank_genes_groups(obj, 'sample_types', groups=['cSCC'], reference='PL', method='wilcoxon', pts = True, key_added = 'temp_deg')
    
    global tempdf
    tempdf = sc.get.rank_genes_groups_df(obj, group = ['cSCC'], key = 'temp_deg')
    
    #printing df nicely
    with option_context('display.max_rows', 30, 'display.max_columns', 50):
        display(tempdf)
    
    tempdf.to_csv(f'{cluster_name}_sample_types_deg_for_volcano.csv')
    
    print(sc.pl.rank_genes_groups(obj, groups=['cSCC'], n_genes=20, key = 'temp_deg'))
    
    return tempdf
    






