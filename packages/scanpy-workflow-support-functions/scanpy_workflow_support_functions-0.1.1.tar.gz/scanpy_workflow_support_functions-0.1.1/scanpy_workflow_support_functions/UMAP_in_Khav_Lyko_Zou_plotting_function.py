import scanpy as sc
import matplotlib.pyplot as plt
import os

def plot_umap_all(data_dirs, color=['annotation'], save_path=None):
    """
    Plots UMAP projections from three AnnData objects side by side.
    
    Parameters:
    - data_dirs (dict): Dictionary with dataset names as keys and file paths as values.
    - color (list or str): Genes or annotations to color the UMAP by.
    - save_path (str, optional): If provided, saves the figure to this path.
    
    """
    
    # Ensure color is a list
    if isinstance(color, str):
        color = [color]
    
    # Read all AnnData objects
    adata_dict = {name: sc.read_h5ad(path) for name, path in data_dirs.items()}
    
    # Create subplots
    fig, axes = plt.subplots(1, len(adata_dict), figsize=(5 * len(adata_dict), 5))
    
    if len(adata_dict) == 1:
        axes = [axes]  # Ensure axes is iterable when there's only one subplot
    
    # Plot UMAPs
    for ax, (name, adata) in zip(axes, adata_dict.items()):
        sc.pl.umap(adata, color=color, color_map='RdPu', wspace=0.1, frameon=False,
                   legend_loc='on data', legend_fontsize=7, ax=ax, show=False)
        ax.set_title(name)
    
    plt.tight_layout()
    
    # Save or show the plot
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"UMAP plot saved to {save_path}")
    else:
        plt.show()

# Define file paths
data_dirs = {
    "Khavari": "/Users/ankitpatel/Library/Mobile Documents/com~apple~CloudDocs/My Drive/Projects/Ji_Multimodal_analysis_SCC_2020/scanpy_cSCC_analysis_Khavari/KhavariCell_sc_workflow_v3_noHVG_subset_24Sep23.h5ad",
    "Lyko": "/Users/ankitpatel/Library/Mobile Documents/com~apple~CloudDocs/My Drive/Projects/IMP_info/From_Alex/Nat_comm_Lyko_CAFs_2023/Lyka_scanpy_pipeline_v2_11Dec23.h5ad",
    "Zou": "/Users/ankitpatel/Library/Mobile Documents/com~apple~CloudDocs/My Drive/Projects/IMP_info/From_Alex/eLife_Zou_etal_2023_scRNAseq/aksccZou_sc_workflow_v2_12Jul23.h5ad"
}

# Example usage
plot_umap_all(data_dirs, color=['annotation', 'gene_name1', 'gene_name2'], save_path="UMAP_plots.pdf")
