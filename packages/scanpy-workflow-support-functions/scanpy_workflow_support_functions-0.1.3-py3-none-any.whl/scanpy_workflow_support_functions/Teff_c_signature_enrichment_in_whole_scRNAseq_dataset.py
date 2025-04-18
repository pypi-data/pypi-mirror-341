import numpy as np
import pandas as pd
import scanpy as sc

DATA_DIR = '/data/BCI-SingleCell/Ankit/FIGURES_APR2024/'



def teff_c_enrichment(adata, dataset_name):
   
    
    teffc = ['STMN1', 'MKI67', 'TYMS', 'PCLAF', 'NUSAP1', 'TOP2A', 'RRM2', 'SMC2', 'CENPF', 'ZWINT', 
         'ASF1B', 'TPX2', 'KNL1', 'CLSPN', 'CENPU', 'TK1', 'ASPM', 'FANCI', 'UBE2C', 'CDK1', 
         'MAD2L1', 'KIFC1', 'NCAPG2', 'MCM7', 'CKS1B', 'CENPM', 'PCNA', 'UHRF1', 'CEP55', 'ATAD2']
    
    adata = sc.tl.score_genes(adata, 
                          gene_list = teffc,
                          score_name = "sanofi_Teff_c",
                          copy = True)
    
    sc.settings.set_figure_params(scanpy=True, transparent=True, vector_friendly=True, dpi_save=300)#, figsize = (8, 8))

    FIG2SAVE = f"{DATA_DIR}"
    # set the global variable: sc.settings.figdir to save all plots
    sc.settings.figdir = FIG2SAVE
    
    
    sc.pl.umap(adata, color = ['annotation', 'sanofi_Teff_c'], 
           frameon = False, wspace=0.1, color_map = 'RdPu',
           legend_loc='on data', legend_fontsize=8, title= dataset_name + '_dataset',
               save = dataset_name + '_teff_c_sanofi_enrichment.png'
          )
    
    return adata



