import scanpy as sc
import pandas as pd
from IPython.display import display
from pandas import option_context

def deg_analysis_to_get_csv_file_sample_types(adata, key_added_in_adata, groupby_in_adata, 
                                 apply_cutoff=True, log2fc_min=0.5, pval_cutoff=0.05,
                                 groups=None, reference=None, sample_types='sample_types',
                                 output_file=None):
    """
    Perform differential expression analysis on the input AnnData object and optionally save the results to a CSV file.

    Parameters:
    - adata: AnnData object containing the data.
    - key_added_in_adata: str, name of the key to store DE results in `adata`.
    - groupby_in_adata: str, the column or category to group the analysis by (e.g., clusters).
    - apply_cutoff: bool, whether to apply cutoff on log2 fold-change and adjusted p-values. Default is True.
    - log2fc_min: float, minimum log2 fold-change to include (applies if `apply_cutoff=True`). Default is 0.5.
    - pval_cutoff: float, cutoff for adjusted p-value (applies if `apply_cutoff=True`). Default is 0.05.
    - groups: list or None, groups to perform DE analysis on (from the `sample_types` column). Must be provided with `reference`.
    - reference: str or None, reference group to compare against (from the `sample_types` column). Must be provided with `groups`.
    - sample_types: str, the column in `adata.obs` to extract `groups` and `reference` from. Default is 'sample_types'.
    - output_file: str or None, the filename for saving the DE results to CSV. If None, the results are not saved.

    Returns:
    - deg: DataFrame, the DE genes results.
    """

    # Ensure that if one of `groups` or `reference` is provided, the other is also provided
    if (groups is not None and reference is None) or (groups is None and reference is not None):
        raise ValueError("Both `groups` and `reference` must be provided together.")

    # If groups and reference are provided, check if they exist in the sample_types column
    if groups is not None and reference is not None:
        available_sample_types = adata.obs[sample_types].unique()
        if not all(group in available_sample_types for group in groups):
            raise ValueError(f"Some groups {groups} not found in the column {sample_types}. Available groups: {available_sample_types}")
        if reference not in available_sample_types:
            raise ValueError(f"Reference group '{reference}' not found in the column {sample_types}. Available groups: {available_sample_types}")

    # Perform DE analysis using the Wilcoxon rank-sum test, with or without specific groups/reference
    if groups is not None and reference is not None:
        print(f"Performing DE analysis for groups: {groups} compared to reference: {reference}.")
        deg = sc.tl.rank_genes_groups(adata, groupby=groupby_in_adata, method='wilcoxon', pts=True, 
                                key_added=key_added_in_adata, groups=groups, reference=reference)
    else:
        print("Performing DE analysis for all groups.")
        deg = sc.tl.rank_genes_groups(adata, groupby=groupby_in_adata, method='wilcoxon', pts=True,key_added=key_added_in_adata)
        

    # Modify the dataframe
    deg = deg.rename(columns={'group': 'clusters'})
    deg['pct_diff'] = deg.pct_nz_group - deg.pct_nz_reference

    # Sorting by log fold change and pct_diff within each cluster
    deg = deg.groupby('clusters', as_index=False).apply(lambda x: x.sort_values('logfoldchanges', ascending=False))
    deg = deg.groupby('clusters', as_index=False).apply(lambda x: x.sort_values('pct_diff', ascending=False))
    deg = deg.reset_index(drop=True)

    # Drop unnecessary columns
    deg.drop(columns=['level_0', 'level_1'], inplace=True, errors='ignore')
    
    # Retrieve DE genes with or without cutoffs
    if apply_cutoff:
        print('Applying cutoff for log2fc and adjusted p-value.')
        deg = deg[(deg['logfoldchanges'].abs() > logfc_cutoff) & (deg['pvals_adj'] < pval_cutoff)]
    else:
        print('No cutoff applied.')
    
    
    # Save to CSV if output_file is provided
    if output_file is not None:
        deg.to_csv(output_file, index=False)
        print(f'Differential expression results saved to {output_file}.')

    # Display the dataframe nicely
    with option_context('display.max_rows', 50, 'display.max_columns', 50):
        display(deg)

    return deg