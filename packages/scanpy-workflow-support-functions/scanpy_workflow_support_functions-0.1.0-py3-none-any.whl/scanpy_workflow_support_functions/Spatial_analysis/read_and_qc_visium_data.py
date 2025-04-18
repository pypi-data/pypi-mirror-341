import os
import scanpy as sc
import session_info
import squidpy as sq


#import pandas as pd
#import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
#from matplotlib import rcParams
#import dask.dataframe as dd

#import cell2location

# QC utils functions - a package 
#from vistools import utils

import random
random.seed(117)





##just to read raw files >> from jason folder
DATA_DIR = "/data/BCI-Skin/Visium/GC_data/" 

def read_jason_visium_data():
    
    """
    read jason's visium data 12 total samples
    6 High HRD and
    6 Low HRD samples
    
    HRD_low <- c("S1A1", "S1B1", "S1C1", "S1D1", "S3A1", "S3D1")
    HRD_high <- c("S2A1", "S2B1", "S2C1", "S2D1", "S3B1", "S3C1”)
    
    this function doesnt take any arguments
    Just reads all samples and outputs adatas: list of all anndata objects
    
    """
    ##just to read raw files >> from jason folder
    DATA_DIR = "/data/BCI-Skin/Visium/GC_data/" 
    
    ##Getting full file paths::
    path_dir = os.path.join(DATA_DIR, 'Analysis/')
    path_dir

    def list_full_paths(path_dir):
        return [os.path.join(path_dir, file) for file in os.listdir(path_dir)]

    file_paths = list_full_paths(path_dir)
    file_paths = [f for f in file_paths if f.endswith('_count')]
    file_paths = [path + '/outs' for path in file_paths]
    print(file_paths)

    ##Getting file name::
    files = os.listdir(path_dir)
    files = [f for f in files if f.endswith('_count')]
    print(files)

    def read_and_qc(path, count_file_prefix='', sample_name=None):
        
        adata = sq.read.visium(path)
                               #count_file=f'{count_file_prefix}filtered_feature_bc_matrix.h5', load_images=True)

        print('Sample ', (list(adata.uns['spatial'].keys())[0]))
        adata.obs['Sample'] = list(adata.uns['spatial'].keys())[0]

        # since we need unique gene names (or it would actually be better to have ensembl ids), we can make them unique
        # Otherwise, error occurs (intersect, find shared genes and subset both anndata and reference signatures)
        adata.var_names_make_unique()

        # Calculate QC metrics
        from scipy.sparse import csr_matrix
        adata.X = adata.X.toarray()

        # find mitochondria-encoded (MT) genes
        adata.var['mt'] = [gene.startswith('MT-') for gene in adata.var_names]
        adata.var['ribo'] = [gene.startswith(('RPS','RPL')) for gene in adata.var_names]
        #adata.obs['mt_frac'] = adata[:, adata.var['mt'].tolist()].X.sum(1).A.squeeze()/adata.obs['total_counts']

        sc.pp.calculate_qc_metrics(adata, inplace=True, log1p=True, qc_vars=['mt','ribo'])
        adata.X = csr_matrix(adata.X)

        # some traditional filtering
        #sc.pp.filter_cells(adata, min_genes=5)
        #sc.pp.filter_genes(adata, min_cells=10)

        # add sample name to obs names
        adata.obs["Sample"] = [str(i) for i in adata.obs['Sample']]
        adata.obs_names = adata.obs["Sample"] \
                              + '_' + adata.obs_names
        adata.obs.index.name = 'spot_id'

        return adata
    
    #now read all samples and output list
    adatas = [read_and_qc(path) for path in file_paths]
    
    return adatas
    
    
    
    
    
### reading very simple way >> specifically to read one by one sample
## read from vistools>utils


## Median absolute deviation function::
from scipy.stats import median_abs_deviation as mad

def mad_outlier(adata, metric: str, nmads: int):
    random.seed(117)
    M = adata.obs[metric]
    
    return (M < np.median(M) - nmads * mad(M)) | (np.median(M) + nmads * mad(M) < M)

def read_and_qc_with_MAD(path, count_file_prefix='', sample_name=None):
    r""" This function reads the data for one 10X spatial experiment into the anndata object.
    It also calculates QC metrics

    :param sample_name: Name of the sample
    :param path: path to data
    :param count_file_prefix: prefix in front of count file name filtered_feature_bc_matrix.h5
    """

    adata = sq.read.visium(path)
                           #count_file=f'{count_file_prefix}filtered_feature_bc_matrix.h5', load_images=True)

    print('Sample ', (list(adata.uns['spatial'].keys())[0]))
    adata.obs['Sample'] = list(adata.uns['spatial'].keys())[0]
    #adata.obs['sample'] = sample_name

    #adata.var['SYMBOL'] = adata.var_names
    #adata.var.rename(columns={'gene_ids': 'ENSEMBL'}, inplace=True)
    #adata.var_names = adata.var['ENSEMBL']
    #adata.var.drop(columns='ENSEMBL', inplace=True)
    
       # since we need unique gene names (or it would actually be better to have ensembl ids), we can make them unique
    # Otherwise, error occurs (intersect, find shared genes and subset both anndata and reference signatures)
    adata.var_names_make_unique()

    # Calculate QC metrics
    from scipy.sparse import csr_matrix
    adata.X = adata.X.toarray()

    # find mitochondria-encoded (MT) genes
    adata.var['mt'] = [gene.startswith('MT-') for gene in adata.var_names]
    adata.var['ribo'] = [gene.startswith(('RPS','RPL')) for gene in adata.var_names]
    #adata.obs['mt_frac'] = adata[:, adata.var['mt'].tolist()].X.sum(1).A.squeeze()/adata.obs['total_counts']

    sc.pp.calculate_qc_metrics(adata, inplace=True, log1p=True, qc_vars=['mt','ribo'])
    adata.X = csr_matrix(adata.X)
    
     #filter outliers
    bool_vector = mad_outlier(adata, 'log1p_total_counts', 3)# +\
        #mad_outlier(adata, 'log1p_n_genes_by_counts', 5) +\
        #mad_outlier(adata, 'pct_counts_in_top_20_genes', 5)
        #mad_outlier(adata, 'pct_counts_mt', 5) # no mito cut off now
    adata = adata[~bool_vector]
    
    sc.pp.filter_cells(adata, min_genes=5)
    sc.pp.filter_genes(adata, min_cells=10)

    # add sample name to obs names
    adata.obs["Sample"] = [str(i) for i in adata.obs['Sample']]
    adata.obs_names = adata.obs["Sample"] \
                          + '_' + adata.obs_names
    adata.obs.index.name = 'spot_id'

    return adata
