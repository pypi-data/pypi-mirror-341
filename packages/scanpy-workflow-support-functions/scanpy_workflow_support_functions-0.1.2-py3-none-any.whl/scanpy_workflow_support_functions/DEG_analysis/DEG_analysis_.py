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
# os.environ['R_HOME'] = '/data/home/hmy327/anaconda/envs/R_python2/lib/R'
# import anndata2ri
# import logging
# import rpy2.rinterface_lib.callbacks as rcb
# import rpy2.robjects as ro
# rcb.logger.setLevel(logging.ERROR)
# ro.pandas2ri.activate()
# anndata2ri.activate()

# #%load_ext rpy2.ipython > equates to:
# #get_ipython().run_line_magic('load_ext', 'rpy2.ipython')


######################################################
#set data directory
#DATA_DIR = "/data/BCI-SingleCell/Ankit/SCVI_sanofi_analysis/"
######################################################


#DEG analysis and saving csv file with all DEG genes
import scanpy as sc
import pandas as pd
from IPython.display import display
from pandas import option_context

DEG analysis and saving dotplot with 10 genes in each cluster
def deg_analysis_for_20_genes(adata, key_added_in_adata, groupby_in_adata):
#     #ask user to provide key_added string name
#     key_added_in_adata = (input('how you want to add key into adata:' ))
#     #key_added_in_adata = (input('how you want to add key into adata:' ))

#     #ask user for groupby category
#     groupby_in_adata = (input('provide groupby clusters:' ))
#     #groupby_in_adata = "'{}'".format(groupby_in_adata)
    
    
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
    
    #saving as .csv file
    answer = input('save deg20 as csv file - yes / no:  ')
    if answer == 'yes':
        deg20.to_csv('top20_genes_table_in_cell_types.csv', index=0)
        print('saved deg20 table as csv file')
    else:
        print('not saving deg20 table')
        
        
    
    
    #making markers as global variable
    #global markers
    markers = deg20.groupby('clusters')['names'].apply(list).to_dict()
    
    
    #saving markers with genes and cluster only as .csv file
    answer = input('save top 20 markers for each cluster as csv file - yes / no:  ')
    if answer == 'yes':
        markers.to_csv('top20_markers_in_cell_types.csv', index=0)
        print('saved top20 markers as csv file')
    else:
        print('not saving top20 markers as csv')
   
    
    # Set the figure size
    #plt.figure(figsize=(10, 10))
    #fig, ax = plt.subplots(figsize=(10, 10))

    ## Run dendrogram here
    sc.tl.dendrogram(adata, groupby = groupby_in_adata)
    
    sc.pl.rank_genes_groups_dotplot(adata, groupby=groupby_in_adata, standard_scale="var", key=key_added_in_adata, var_names = markers,)
                                    #save = 'saved_top20_DEG_dot_plot.png',)
    
    print(adata)
    return adata,deg20,markers

### why global is not working. ???????????????
#repalce below deg_10 as well

## same deg function as above but for 5 genes dotplot
def deg_analysis_for_10genes(adata, key_added_in_adata, groupby_in_adata):
    
#     #ask user to provide key_added string name
#     key_added_in_adata = (input('how you want to add key into adata:' ))
#     #key_added_in_adata = "'{}'".format(key_added_in_adata)
    
#     #ask user for groupby category
#     groupby_in_adata = (input('provide groupby clusters:' ))
#     #groupby_in_adata = "'{}'".format(groupby_in_adata)
        
    
#     ## Adding if statment > only running deg if previous deg_analysis fun not run
#     if key_added_in_adata not in adata.uns:
        
#         #DEG analysis with wilcoxon method
#         sc.tl.rank_genes_groups(adata, groupby=groupby_in_adata, method='wilcoxon', pts = True, key_added = key_added_in_adata)
        
#     else:
       
#         print('DEG analysis already performed')
    
    
    #DEG analysis with wilcoxon method
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
    
    # getting top 10 markers in each cluster
    deg10 = deg.groupby('clusters').head(10)
    
    #removing unnecessary columns
    deg10.drop(columns=['level_0', 'level_1', 'level_2'], inplace=True)
    
    #printing df nicely
    with option_context('display.max_rows', 50, 'display.max_columns', 100):
        display(deg10)
    
    #making markers as global variable
    #global markers
    markers = deg10.groupby('clusters')['names'].apply(list).to_dict()

    # Set the figure size
    #plt.figure(figsize=(10, 10))
    #fig, ax = plt.subplots(figsize=(10, 10))

    ## Run dendrogram here
    sc.tl.dendrogram(adata, groupby = groupby_in_adata)
    
    sc.pl.rank_genes_groups_dotplot(adata, groupby=groupby_in_adata, standard_scale="var", key=key_added_in_adata, var_names = markers,)
                                    #save = 'saved_top10_DEG_dot_plot.png',)
    
    print(adata)
    return adata,deg10,markers



def deg_default(adata):
    #ask user to provide key_added string name
    key_added_in_adata = (input('how you want to add key into adata:' ))
    #key_added_in_adata = "'{}'".format(key_added_in_adata)

    #ask user for groupby category
    groupby_in_adata = (input('provide groupby clusters:' ))
    #groupby_in_adata = "'{}'".format(groupby_in_adata)

    ## Adding if statment > only running deg if previous deg_analysis fun not run
    if key_added_in_adata in adata.uns:
        print('DEG analysis already performed')
    else:
         
        sc.tl.rank_genes_groups(adata, groupby=groupby_in_adata, method='wilcoxon', pts = True, key_added = key_added_in_adata)


    #print(f'Genes in each cluster:\n{deg['group'].value_counts()}')
    #print(adata.uns[key_added_in_adata].value_counts())

    sc.pl.rank_genes_groups_dotplot(adata, groupby=groupby_in_adata, standard_scale="var", n_genes=10, key=key_added_in_adata)

    #### WILL NOT BE ABLE TO SAVE OBJECT AFTER THIS >.SO BE CAREFULL
    sc.tl.filter_rank_genes_groups(adata,
                                    min_in_group_fraction=0.2,
                                    max_out_group_fraction=0.2,
                                    key=key_added_in_adata,
                                    key_added="DEG_filtered",
                                    )

    ## WILL NOT BE ABLE TO SAVE OBJECT AFTER THIS >.SO BE CAREFULL
    sc.tl.dendrogram(adata, groupby = groupby_in_adata)
    
    sc.pl.rank_genes_groups_dotplot(adata,
                                    groupby=groupby_in_adata,
                                    standard_scale="var",
                                    n_genes=10,
                                    key="DEG_filtered",
                                    save = 'saved_top10_DEG_filtered_dot_plot.png',)

    #removing the DEG_filtered layer or it will not let the save adata object
    adata.uns.pop("DEG_filtered")

    print(adata)
    return adata


def DEG_deg_analysis_to_get_csv_file(adata, key_added, groupby, apply_cutoff=True, 
                                 pval_cutoff=0.05, log2fc_min=0.5, output_file="DEG_genes_in_cell_types.csv"):
    """
    Perform differential expression analysis on an AnnData object and save results as a CSV file.

    Parameters:
    adata : AnnData
        The annotated data matrix of shape (n_obs, n_vars).
    key_added : str
        Name of the key under which DEG results will be stored in `adata.uns`.
    groupby : str
        Column name in `adata.obs` used for grouping cells.
    apply_cutoff : bool, optional
        Whether to apply log2FC & adjusted p-value cutoffs. Default is True.
    pval_cutoff : float, optional
        Adjusted p-value cutoff if `apply_cutoff` is True. Default is 0.05.
    log2fc_min : float, optional
        Minimum log2 fold change cutoff if `apply_cutoff` is True. Default is 0.5.
    output_file : str, optional
        Name of the output CSV file. Default is "DEG_genes_in_cell_types.csv".

    Returns:
    DataFrame
        A DataFrame containing DEG results.
    """

    # Perform differential expression analysis
    sc.tl.rank_genes_groups(adata, groupby=groupby, method="wilcoxon", pts=True, key_added=key_added)

    # Retrieve DEG results with or without cutoff
    if apply_cutoff:
        print(f"Applying cutoffs: pval < {pval_cutoff}, log2FC > {log2fc_min}")
        deg = sc.get.rank_genes_groups_df(adata, group=None, key=key_added, 
                                          pval_cutoff=pval_cutoff, log2fc_min=log2fc_min)
    else:
        print("No cutoffs applied.")
        deg = sc.get.rank_genes_groups_df(adata, group=None, key=key_added)

    # Print count of genes per cluster
    print(deg['group'].value_counts())

    # Rename 'group' to 'clusters' and calculate percentage difference
    deg.rename(columns={'group': 'clusters'}, inplace=True)
    deg['pct_diff'] = deg['pct_nz_group'] - deg['pct_nz_reference']

    # Sort by logfold changes and percentage difference within each cluster
    deg = deg.sort_values(['clusters', 'logfoldchanges', 'pct_diff'], ascending=[True, False, False])

    # Reset index
    deg.reset_index(drop=True, inplace=True)

    # Save results to CSV
    deg.to_csv(output_file, index=False)
    
    # Display nicely formatted output
    with option_context("display.max_rows", 50, "display.max_columns", 50):
        display(deg)

    return deg
