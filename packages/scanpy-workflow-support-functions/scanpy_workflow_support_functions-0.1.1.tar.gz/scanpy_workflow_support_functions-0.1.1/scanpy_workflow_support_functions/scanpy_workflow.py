#!/usr/bin/env python
# coding: utf-8


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

from anndata import AnnData

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


def adata_read():
    '''
    first ask for file path > provide full path of .h5ad file path
    adata.h5ad object saved after initial filtering

    read with read_h5ad function in scanpy
    '''
    file = input('provide h5ad file path:' )
    #file = f'\'{file}\''
    file = "'{}'".format(file)

    adata = sc.read_h5ad(file)
    print(adata)
    return adata


# First check doublets and removing doublets from whole object
def doublet_removel(adata):
    if 'doublet' in adata.obs['scDblFinder_class'].values:
        adata = adata[~(adata.obs['scDblFinder_class'] == 'doublet')]
        
    print(adata)
    #print(adata.obs)
    return adata


### Adding shifted logarithm
def shifted_log(adata):

    if 'soupX_counts' in adata.layers:
        adata.X = adata.layers["soupX_counts"]

    scales_counts = sc.pp.normalize_total(adata, target_sum=None, inplace=False)
    # log1p transform
    adata.layers["log1p_norm"] = sc.pp.log1p(scales_counts["X"], copy=True)

    return adata

################################################################
################## main scanpy_workflow ########################

def scanpy_pipeline(adata):
    np.random.seed(0)
    
    # normalising data with log1p
    if 'soupX_counts' in adata.layers:
        adata.X = adata.layers["soupX_counts"]

    scales_counts = sc.pp.normalize_total(adata, target_sum=None, inplace=False)
    # log1p transform
    adata.layers["log1p_norm"] = sc.pp.log1p(scales_counts["X"], copy=True)
    
    #chaning main layer with log1p
    adata.X = adata.layers["log1p_norm"]
    
    adata.raw = adata ## >> this is very imp>freeze the state if anndata
    
    #KEEP 'highly_variable' AS ITIS, ONLY THEN PCA WILL USE IT
    sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
    
    #actually dont need to do this, for pca it used highly variable genes after above function
    #adata = adata[:, adata.var.highly_variable]

    ## Regress out effects of total counts per cell and the percentage of mitochondrial genes expressed.
    sc.pp.regress_out(adata, ['total_counts', 'pct_counts_mt'])
    ## Scale the data to unit variance.
    sc.pp.scale(adata, max_value=10)

    #sc.pp.pca(adata, svd_solver="arpack", use_highly_variable=True)
    sc.tl.pca(adata, svd_solver='arpack', random_state=0)
    sc.pl.pca_variance_ratio(adata, log=True)#, save = 'sanofi_pca_plots.png')

    # Harmony integration
    sce.pp.harmony_integrate(adata, 'sample_ID')

    sc.pp.neighbors(adata, n_pcs=50, use_rep = "X_pca_harmony", random_state=0)
    sc.tl.umap(adata, random_state=0)
    sc.tl.leiden(adata, random_state=0)

    print(adata)
    return adata



#

## write function to transfer cells from one obeject to another /// or cell labels
# by index match
def label_transfer_anndata_to_anndata(to_adata, from_adata, to_adata_obs_label, from_adata_obs_label):
    
#     to_adata_obs_label = (input('column name for to_adata:' ))
#     #to_adata_obs_label = "'{}'".format(to_adata_obs_label)

#     from_adata_obs_label = (input('column name for from_adata:' ))
#     #from_adata_obs_label = "'{}'".format(from_adata_obs_label)
    
    
#     #ask if need to create .obs.column into to_adata
#     #then copy the same column from from_adata to to_adata
#     answer = input('if column need to create in to_adata yes/no: ')
#     if answer == 'yes':
#         #column_name = input('name of the column to create in to_adata')
#         to_adata.obs[to_adata_obs_label] = from_adata.obs[from_adata_obs_label]

    
    to_adata.obs[to_adata_obs_label] = to_adata.obs[to_adata_obs_label].astype('str')
    from_adata.obs[from_adata_obs_label] = from_adata.obs[from_adata_obs_label].astype('str')

    for index in to_adata.obs.index:
        if index in from_adata.obs.index:
            to_adata.obs.loc[index, to_adata_obs_label] = from_adata.obs.loc[index, from_adata_obs_label]

    return to_adata

### IF from_adata is df use this
def label_transfer_df_to_anndata(to_adata, from_adata, to_adata_obs_label, from_adata_obs_label):
    """
    to_adata: targte anndata object
    from_adata: pd df from where the labels needs to be transferred
    """
    
    to_adata.obs[to_adata_obs_label] = to_adata.obs[to_adata_obs_label].astype('str')
    from_adata[from_adata_obs_label] = from_adata[from_adata_obs_label].astype('str')
    
    for index in to_adata.obs.index:
        if index in from_adata.index:
            to_adata.obs.loc[index, to_adata_obs_label] = from_adata.loc[index, from_adata_obs_label]

    return to_adata


## relable the clusters in same adata column
def celltype_relabel_in_same_column(adata: AnnData, column_to_change: str, label_to_change, relabel_into):
    # Ensure label_to_change is a list
    if not isinstance(label_to_change, list):
        label_to_change = [label_to_change]
    
    # If relabel_into is not a list, convert it to a list of the same length as label_to_change
    if not isinstance(relabel_into, list):
        relabel_into = [relabel_into] * len(label_to_change)
    
    # Check if both lists have the same length
    if len(label_to_change) != len(relabel_into):
        raise ValueError("Input lists must have the same length, or relabel_into must be a single value.")
    
    # Perform relabeling
    for item_a, item_b in zip(label_to_change, relabel_into):
        adata.obs[column_to_change] = np.where(
            adata.obs[column_to_change] == item_a,
            item_b,
            adata.obs[column_to_change]
        )
    
    return adata

# def celltype_relabel_in_same_column(adata, column_to_change, label_to_change, relabel_into):
    
#     if isinstance(label_to_change, list) and isinstance(relabel_into, list):
#         if len(label_to_change) != len(relabel_into):
#             raise ValueError("Input lists must have the same length.")
            
#         for item_a, item_b in zip(label_to_change, relabel_into):
            
#             adata.obs[column_to_change] = np.where((adata.obs[column_to_change] == item_a),
#                                            item_b,
#                                            adata.obs[column_to_change])
            
#     else:

#         adata.obs[column_to_change] = np.where((adata.obs[column_to_change] == label_to_change),
#                                            relabel_into,
#                                            adata.obs[column_to_change])
    
#     return adata

