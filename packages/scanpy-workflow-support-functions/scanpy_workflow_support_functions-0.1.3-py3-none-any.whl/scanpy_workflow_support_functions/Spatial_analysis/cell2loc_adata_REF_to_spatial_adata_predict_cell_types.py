import warnings
warnings.filterwarnings('ignore')


import scanpy as sc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import session_info
#import dask.dataframe as dd
import squidpy as sq
import os
import cell2location
import sys

import random
random.seed(117)


folder_to_save = 'adata_REF_Khav_and_Zhou_only'
DATA_DIR3 = f'/data/BCI-SingleCell/Ankit/10x_visium_analysis/{folder_to_save}/' 

#Load adata_ref trained models and adata_ref

adata_ref = sc.read_h5ad(f'{DATA_DIR3}/khavari_ref_trained_for_cell2loc.h5ad')

mod = cell2location.models.RegressionModel.load(f'{DATA_DIR3}', adata_ref)


## Estimating signature

# export estimated expression in each cluster
if 'means_per_cluster_mu_fg' in adata_ref.varm.keys():
    inf_aver = adata_ref.varm['means_per_cluster_mu_fg'][[f'means_per_cluster_mu_fg_{i}'
                                    for i in adata_ref.uns['mod']['factor_names']]].copy()
else:
    inf_aver = adata_ref.var[[f'means_per_cluster_mu_fg_{i}'
                                    for i in adata_ref.uns['mod']['factor_names']]].copy()
inf_aver.columns = adata_ref.uns['mod']['factor_names']
inf_aver.iloc[0:5, 0:5]

inf_aver['Bcells'].sort_values(ascending=False).head(30)
inf_aver['iCAF'].sort_values(ascending=False).head(30)
inf_aver['Keratinocytes'].sort_values(ascending=False).head(30)

## Reading adata_spatial obejct

adata_DIR = '/data/BCI-SingleCell/Ankit/10x_visium_analysis/'

adata = sc.read_h5ad(f'{adata_DIR}all_slides_concatenated_raw_20May24.h5ad')

# find shared genes and subset both anndata and reference signatures
intersect = np.intersect1d(adata.var_names, inf_aver.index)
adata = adata[:, intersect].copy()
inf_aver = inf_aver.loc[intersect, :].copy()

# prepare anndata for cell2location model
cell2location.models.Cell2location.setup_anndata(adata=adata, batch_key="batch")


# create and train the model
mod = cell2location.models.Cell2location(
    adata, cell_state_df=inf_aver,
    # the expected average cell abundance: tissue-dependent
    # hyper-prior which can be estimated from paired histology:
    N_cells_per_location=5,
    # hyperparameter controlling normalisation of
    # within-experiment variation in RNA detection:
    detection_alpha=20   #200
)
mod.view_anndata_setup()

mod.train(max_epochs=30000,
          # train using full data (batch_size=None)
          batch_size=None,
          # use all data points in training because
          # we need to estimate cell abundance at all locations
          train_size=1,
          #use_gpu=True,
         )

# plot ELBO loss history during training, removing first 100 epochs from the plot
mod.plot_history(1000)
plt.legend(labels=['full data training']);

# plot ELBO loss history during training, removing first 100 epochs from the plot

rcParams["figure.figsize"] = 8, 8
mod.plot_history(1000)
plt.legend(labels=['full data training']);

# In this section, we export the estimated cell abundance (summary of the posterior distribution).
adata = mod.export_posterior(
    adata, sample_kwargs={'num_samples': 1000, 'batch_size': mod.adata.n_obs}
)


# Save model
DATA_DIR4 = f'{DATA_DIR3}adata_spatial_model/'

# Check if the directory exists, and if not, create it
if not os.path.exists(DATA_DIR4):
    os.makedirs(DATA_DIR4)
    print(f"Directory {DATA_DIR4} created.")
else:
    print(f"Directory {DATA_DIR4} already exists.")


## save model and adata

mod.save(f"{DATA_DIR4}", overwrite=True)

# mod = cell2location.models.Cell2location.load(f"{run_name}", adata_vis)

# Save anndata object with results
adata.write(f'{DATA_DIR4}/Jason_visium_cell2loc_estimated_cells_01June24.h5ad')


# plot ELBO loss history during training, removing first 100 epochs from the plot
mod.plot_history(1000)
plt.legend(labels=["full data training"]);

mod













