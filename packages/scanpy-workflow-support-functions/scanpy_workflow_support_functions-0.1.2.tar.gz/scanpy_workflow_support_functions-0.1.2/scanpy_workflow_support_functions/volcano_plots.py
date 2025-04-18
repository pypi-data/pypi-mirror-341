
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



## to plot volcano in R >> get df
def volcano_plot_sample_types_csv(adata):
    
    cluster_name = (input('provide_cluster_name:'  ))
    obs_column = (input('cell type label column:'  ))
    
    obj = adata[adata.obs.obs_column == cluster_name]
    
    sc.tl.rank_genes_groups(obj, 'sample_types', groups=['cSCC'], reference='PL', 
                            method='wilcoxon', pts = True, key_added = 'temp_deg')
    
    global tempdf
    tempdf = sc.get.rank_genes_groups_df(obj, group = ['cSCC'], key = 'temp_deg')
    
    #printing df nicely
    with option_context('display.max_rows', 30, 'display.max_columns', 50):
        display(tempdf)
    
    tempdf.to_csv(f'{cluster_name}_sample_types_deg_for_volcano.csv')
    
    print(sc.pl.rank_genes_groups(obj, groups=['cSCC'], n_genes=20, key = 'temp_deg'))
    
    return tempdf





