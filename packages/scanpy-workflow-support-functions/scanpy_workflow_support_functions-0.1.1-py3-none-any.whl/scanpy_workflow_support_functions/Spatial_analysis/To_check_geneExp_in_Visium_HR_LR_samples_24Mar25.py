import scanpy as sc
import seaborn as sns
import matplotlib.pyplot as plt
from statannotations.Annotator import Annotator

def plot_gene_expression_boxplot(bdata, selected_indexes, genes_to_plot, output_file):
    """
    Plots a boxplot comparing gene expression levels between risk groups.

    Parameters:
    - bdata: AnnData object
    - selected_indexes: List of cell indexes to filter
    - genes_to_plot: List of genes to analyze (e.g., ['MDK', 'STMN1'])
    - output_file: File path to save the plot

    Returns:
    - A boxplot with statistical annotations.
    """

    # Subset the AnnData object based on selected indexes
    filtered_data = bdata[bdata.obs.index.isin(selected_indexes)]

    # Extract gene expression data
    df_genes = sc.get.obs_df(filtered_data, keys=genes_to_plot, gene_symbols='genes', use_raw=False)

    # Merge with metadata (Sample and risk_groups)
    df_genes = df_genes.merge(filtered_data.obs[['Sample', 'risk_groups']], 
                              left_index=True, right_index=True)

    # Compute the mean expression per Sample
    df_genes_avg = df_genes.groupby('Sample')[genes_to_plot].mean().reset_index()

    # Add risk group information
    df_genes_avg = df_genes_avg.merge(df_genes[['Sample', 'risk_groups']].drop_duplicates(), on='Sample')

    # Reshape for plotting
    df_genes_melted = df_genes_avg.melt(id_vars=['Sample', 'risk_groups'], 
                                        value_vars=genes_to_plot, 
                                        var_name='Gene', 
                                        value_name='Expression')

    # Create the boxplot
    plt.figure(figsize=(6, 4))
    ax = sns.boxplot(data=df_genes_melted, x='Gene', y='Expression', hue='risk_groups', 
                     palette='Set2', hue_order=['low_risk', 'high_risk'])

    # Define pairs for statistical comparison
    pairs = [((gene, "low_risk"), (gene, "high_risk")) for gene in genes_to_plot]

    # Add statistical annotations
    annotator = Annotator(ax, pairs, data=df_genes_melted, x='Gene', y='Expression', hue='risk_groups')
    annotator.configure(test='Mann-Whitney', text_format='star', loc='inside', verbose=2)
    annotator.apply_and_annotate()

    # Labeling and saving the plot
    plt.ylabel("Average Expression")
    plt.title(f"Expression of {', '.join(genes_to_plot)} in Selected Spots")
    plt.legend(title="Risk Group")
    plt.savefig(output_file, dpi=600)
    plt.show()