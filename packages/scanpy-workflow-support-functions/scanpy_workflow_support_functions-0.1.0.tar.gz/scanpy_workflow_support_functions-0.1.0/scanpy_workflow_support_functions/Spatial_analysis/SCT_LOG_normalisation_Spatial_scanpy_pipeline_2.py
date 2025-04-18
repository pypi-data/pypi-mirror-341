## For R_python2 environment
import warnings
warnings.filterwarnings('ignore')

import scanpy as sc
import numpy as np
import os
os.environ['R_HOME'] = '/data/home/hmy327/anaconda/envs/R_python2/lib/R'
import anndata2ri
from rpy2.robjects import r, pandas2ri, Formula
from rpy2.robjects.packages import importr

# Activate the automatic conversion between anndata and R data structures
anndata2ri.activate()

# Import necessary R packages
base = importr('base')
seurat = importr('Seurat')
sce = importr('SingleCellExperiment')

def sct_log_norm_to_layers_2(adata):
    
    # Normalising data with SCT if 'soupX_counts' in layers
    if 'soupX_counts' in adata.layers:
        adata.X = adata.layers["soupX_counts"]

    def prepare_adata_for_sctnorm(adata):
        adata_ = sc.AnnData(adata.X.copy())
        adata_.obs_names = adata.obs_names.copy()
        adata_.var_names = adata.var_names.copy()
        adata_.obs["Sample"] = adata.obs["Sample"].copy()
        return adata_

    adata_ = prepare_adata_for_sctnorm(adata)

    # Run SCT normalization in R
    anndata2ri.activate()
    
    # Convert the AnnData object to an R object
    r_adata = anndata2ri.py2rpy(adata_)
    
    # Assign the R object to a variable in R and run SCT normalization
    r.assign("adata_", r_adata)
    r('''
        library(SingleCellExperiment)
        library(Seurat)

        seu <- as.Seurat(adata_, data=NULL, counts='X')
        seu <- RenameAssays(object = seu, originalexp = "RNA", verbose=TRUE) 
        seu <- SCTransform(seu, verbose=TRUE)  #assay='spatial'
        ann_ <- as.SingleCellExperiment(seu, assay='SCT')
    ''')
    
    # Retrieve the normalized R object and manually construct the AnnData object
    r_ann_ = r('ann_')
    
    # Extract the logcounts layer from the SingleCellExperiment object as a numpy array
    logcounts = np.array(r('as.matrix(assay(ann_, "logcounts"))'))
    
    # Check the type of logcounts
    print(f'logcounts type: {type(logcounts)}')
    dim(logcounts)
    
    try:
        # Manually construct the AnnData object using the numpy array
        ann_ = sc.AnnData(X=logcounts)
        ann_.obs_names = adata_.obs_names  # Ensure obs_names match
        ann_.var_names = adata_.var_names  # Ensure var_names match

        # Transfer SCT normalized counts to adata layers
        adata.layers['sctransform'] = ann_.X.copy()
        
    except Exception as e:
        print(f'Error during conversion: {e}')
        raise e
        
    # Deactivate the automatic conversion when not needed
    anndata2ri.deactivate()

    def log_normalisation(adata):
        np.random.seed(0)

        # Normalising data with log1p if 'soupX_counts' in layers
        if 'soupX_counts' in adata.layers:
            adata.X = adata.layers["soupX_counts"]

        scales_counts = sc.pp.normalize_total(adata, target_sum=None, inplace=False)
        adata.layers["log1p_norm"] = sc.pp.log1p(scales_counts["X"], copy=True)
        return adata

    adata = log_normalisation(adata)

    return adata









# import warnings
# warnings.filterwarnings('ignore')

# import scanpy as sc
# import numpy as np
# import pandas as pd
# import sklearn
# import scanpy.external as sce
# #import squidpy as sq

# import os
# os.environ['R_HOME'] = '/data/home/hmy327/anaconda/envs/R_python2/lib/R'
# import anndata2ri

# from rpy2.robjects import r
# anndata2ri.activate()
# %load_ext rpy2.ipython

# ##function to normalised anndata object with SCTtransfom
# def sct_log_norm_to_layers(adata):
    
#     # normalising data with sct
#     if 'soupX_counts' in adata.layers:
#         adata.X = adata.layers["soupX_counts"]

#     def prepare_adata_for_sctnorm(adata):

#         adata_ = sc.AnnData(adata.X.copy())
#         adata_.obs_names = adata.obs_names.copy()
#         adata_.var_names = adata.var_names.copy()
#         adata_.obs["Sample"] = adata.obs["Sample"].copy()
#         return adata_

#     adata_ = prepare_adata_for_sctnorm(adata)

#     #Run this after running above prepare adata function

#     %%R -i adata_ -o ann_
#     suppressPackageStartupMessages({
#         library(SingleCellExperiment)
#         library(Seurat)
#     })
#     set.seed(123)

#     seu = as.Seurat(adata_, data=NULL, counts='X')
#     seu <- RenameAssays(object = seu, originalexp = "RNA", verbose=TRUE) 
#     seu <- SCTransform(seu, verbose=TRUE)  #assay='saptial'
#     seu

#     #saving back to anndata
#     ann_ <- as.SingleCellExperiment(seu, assay='SCT')


#     ##logcount in layer is the sct transformed counts
#     print(ann_)

    
#     #transfer to adata layers
#     adata.layers['sctransform'] = ann_.layers['logcounts']
    
    
#     def log_normalisation(adata):
#         np.random.seed(0)

#         # normalising data with log1p
#         if 'soupX_counts' in adata.layers:
#             adata.X = adata.layers["soupX_counts"]

#         scales_counts = sc.pp.normalize_total(adata, target_sum=None, inplace=False)
#         # log1p transform
#         adata.layers["log1p_norm"] = sc.pp.log1p(scales_counts["X"], copy=True)
#         return adata

#     adata = log_normalisation(adata)

#     return adata






# ##function to normalised anndata object with SCTtransfom

# def prepare_adata_for_sctnorm(adata):
    
#     adata_ = sc.AnnData(adata.X.copy())
#     adata_.obs_names = adata.obs_names.copy()
#     adata_.var_names = adata.var_names.copy()
#     adata_.obs["Sample"] = adata.obs["Sample"].copy()
#     return adata_



# ## Run this after running above prepare adata function

# %%R -o ann_
# suppressPackageStartupMessages({
#     library(SingleCellExperiment)
#     library(Seurat)
# })
# set.seed(123)

# seu = as.Seurat(adata_, data=NULL, counts='X')
# seu <- RenameAssays(object = seu, originalexp = "RNA", verbose=TRUE) 
# seu <- SCTransform(seu, verbose=TRUE)
# seu

# ## %%R -o ann_
# ann_ <- as.SingleCellExperiment(seu, assay='SCT')

# ##logcount in layer is the sct transformed counts




# scanpy pipeline for spatial data analysis

def scanpy_pipeline_local(adata, norm_layers = None):
    np.random.seed(0)
    
    if norm_layers is None:
        scales_counts = sc.pp.normalize_total(adata, target_sum=None, inplace=False)
        # log1p transform
        adata.layers["log1p_norm"] = sc.pp.log1p(scales_counts["X"], copy=True)    
    else:
        #chaning main layer with norm_layers
        adata.X = adata.layers[norm_layers]
    
    adata.raw = adata ## >> this is very imp>freeze the state if anndata
    
    #sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
    
    sc.pp.highly_variable_genes(adata, flavor="seurat", n_top_genes=2000)
    
    sc.tl.pca(adata, svd_solver='arpack', random_state=0)
    sc.pl.pca_variance_ratio(adata, log=True)#, save = 'sanofi_pca_plots.png')

    # Harmony integration
    #sce.pp.harmony_integrate(adata, 'sample_ID')

    sc.pp.neighbors(adata, n_pcs=20, random_state=0) #use_rep = "X_pca_harmony", 
    sc.tl.umap(adata, random_state=0)
    sc.tl.leiden(adata, random_state=0, key_added="clusters", directed=False, n_iterations=2)

    print(adata)
    return adata


