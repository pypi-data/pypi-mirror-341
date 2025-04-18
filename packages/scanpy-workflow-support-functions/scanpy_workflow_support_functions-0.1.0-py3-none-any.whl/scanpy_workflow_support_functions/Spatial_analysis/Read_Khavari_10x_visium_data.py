from pathlib import Path
from typing import Union, Optional
import logging as logg
from matplotlib.image import imread
import json
import pandas as pd
import scanpy as sc
from anndata import AnnData
import random
import scanpy as sc
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#import session_info
#import squidpy as sq
#import os
#import cell2location
#import sys

def read_visium_khavari_10x_global(
    path: Union[Path, str],
    genome: Optional[str] = None,
    *,
    count_file: Union[Path, str],
    library_id: Optional[str] = None,
    load_images: Optional[bool] = True,
    source_image_path: Optional[Union[Path, str]] = None,
) -> AnnData:
    """\
    Read 10x-Genomics-formatted visum dataset.

    In addition to reading regular 10x output,
    this looks for the `spatial` folder and loads images,
    coordinates and scale factors.
    Based on the `Space Ranger output docs`_.

    See :func:`~scanpy.pl.spatial` for a compatible plotting function.

    .. _Space Ranger output docs: https://support.10xgenomics.com/spatial-gene-expression/software/pipelines/latest/output/overview

    Parameters
    ----------
    path
        Path to directory for visium datafiles.
    genome
        Filter expression to genes within this genome.
    count_file_path
        Path to directory for `.mtx` and `.tsv` files,
        e.g. './filtered_gene_bc_matrices/hg19/'.
    library_id
        Identifier for the visium library. Can be modified when concatenating multiple adata objects.
    source_image_path
        Path to the high-resolution tissue image. Path will be included in
        `.uns["spatial"][library_id]["metadata"]["source_image_path"]`.

    Returns
    -------
    Annotated data matrix, where observations/cells are named by their
    barcode and variables/genes by gene name. Stores the following information:

    :attr:`~anndata.AnnData.X`
        The data matrix is stored
    :attr:`~anndata.AnnData.obs_names`
        Cell names
    :attr:`~anndata.AnnData.var_names`
        Gene names for a feature barcode matrix, probe names for a probe bc matrix
    :attr:`~anndata.AnnData.var`\\ `['gene_ids']`
        Gene IDs
    :attr:`~anndata.AnnData.var`\\ `['feature_types']`
        Feature types
    :attr:`~anndata.AnnData.obs`\\ `[filtered_barcodes]`
        filtered barcodes if present in the matrix
    :attr:`~anndata.AnnData.var`
        Any additional metadata present in /matrix/features is read in.
    :attr:`~anndata.AnnData.uns`\\ `['spatial']`
        Dict of spaceranger output files with 'library_id' as key
    :attr:`~anndata.AnnData.uns`\\ `['spatial'][library_id]['images']`
        Dict of images (`'hires'` and `'lowres'`)
    :attr:`~anndata.AnnData.uns`\\ `['spatial'][library_id]['scalefactors']`
        Scale factors for the spots
    :attr:`~anndata.AnnData.uns`\\ `['spatial'][library_id]['metadata']`
        Files metadata: 'chemistry_description', 'software_version', 'source_image_path'
    :attr:`~anndata.AnnData.obsm`\\ `['spatial']`
        Spatial spot coordinates, usable as `basis` by :func:`~scanpy.pl.embedding`.
    """
    path = Path(path)
    
    #adata = read_10x_h5(path / count_file, genome=genome)
    adata = sc.read_10x_mtx(path / count_file)
    
    adata.uns["spatial"] = dict()

#     from h5py import File

#     with File(path / count_file, mode="r") as f:
#         attrs = dict(f.attrs)
#     if library_id is None:
#         library_id = str(attrs.pop("library_ids")[0], "utf-8")


    adata.uns["spatial"][library_id] = dict()

    if load_images:
        tissue_positions_file = (
            path / "tissue_positions.csv"
            if (path / f"{library_id}_tissue_positions.csv").exists()
            else path / f"{library_id}_tissue_positions_list.csv"
        )
        files = dict(
            tissue_positions_file=tissue_positions_file,
            scalefactors_json_file=path / f"{library_id}_scalefactors_json.json",
            hires_image=path / f"{library_id}_tissue_hires_image.png",
            lowres_image=path / f"{library_id}_tissue_lowres_image.png",
        )

        # check if files exists, continue if images are missing
        for f in files.values():
            if not f.exists():
                if any(x in str(f) for x in ["hires_image", "lowres_image"]):
                    logg.warning(
                        f"You seem to be missing an image file.\n"
                        f"Could not find '{f}'."
                    )
                else:
                    raise OSError(f"Could not find '{f}'")

        adata.uns["spatial"][library_id]["images"] = dict()
        for res in ["hires", "lowres"]:
            try:
                adata.uns["spatial"][library_id]["images"][res] = imread(
                    str(files[f"{res}_image"])
                )
            except Exception:
                raise OSError(f"Could not find '{res}_image'")

        # read json scalefactors
        adata.uns["spatial"][library_id]["scalefactors"] = json.loads(
            files["scalefactors_json_file"].read_bytes()
        )

#         adata.uns["spatial"][library_id]["metadata"] = {
#             k: (str(attrs[k], "utf-8") if isinstance(attrs[k], bytes) else attrs[k])
#             for k in ("chemistry_description", "software_version")
#             if k in attrs
#         }

        # read coordinates
        positions = pd.read_csv(
            files["tissue_positions_file"],
            header=0 if tissue_positions_file.name == "tissue_positions.csv" else None,
            index_col=0,
        )
        positions.columns = [
            "in_tissue",
            "array_row",
            "array_col",
            "pxl_col_in_fullres",
            "pxl_row_in_fullres",
        ]

        adata.obs = adata.obs.join(positions, how="left")

        adata.obsm["spatial"] = adata.obs[
            ["pxl_row_in_fullres", "pxl_col_in_fullres"]
        ].to_numpy()
        adata.obs.drop(
            columns=["pxl_row_in_fullres", "pxl_col_in_fullres"],
            inplace=True,
        )

        # put image path in uns
        if source_image_path is not None:
            # get an absolute path
            source_image_path = str(Path(source_image_path).resolve())
            adata.uns["spatial"][library_id]["metadata"]["source_image_path"] = str(
                source_image_path
            )

    return adata


from scipy.stats import median_abs_deviation as mad

def mad_outlier_khavari(adata, metric: str, nmads: int):
    random.seed(117)
    M = adata.obs[metric]
    
    return (M < np.median(M) - nmads * mad(M)) | (np.median(M) + nmads * mad(M) < M)

def adata_and_qc(adata, count_file_prefix='', sample_name=None):
    r""" This function reads the data for one 10X spatial experiment into the anndata object.
    It also calculates QC metrics

    :param sample_name: Name of the sample
    :param path: path to data
    :param count_file_prefix: prefix in front of count file name filtered_feature_bc_matrix.h5
    """

    #adata = sq.read.visium(path)
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
