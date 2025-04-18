import scanpy as sc
import matplotlib.pyplot as plt
import gc  # Garbage collector

def plot_umap_all(selected_datasets=None, color=['annotation'], save_path=None):
    """
    Plots UMAP projections from selected AnnData objects side by side while managing memory efficiently.

    Parameters:
    - selected_datasets (list, optional): List of dataset names to include. If None, use all.
    - color (list or str): Genes or annotations to color the UMAP by.
    - save_path (str, optional): If provided, saves the figure to this path.
    """

    # Define all available datasets #replace with your dataset paths
    data_dirs = {
        "Sanofi": "/Users/ankitpatel/Library/Mobile Documents/com~apple~CloudDocs/My Drive/Projects/Anaconda/Sanofi_python_analysis/sanofi_soupx_ScDblFinder_filtered_10Jun23_processed_NoHVGsubset_12Jan24.h5ad",
        "Khavari": "/Users/ankitpatel/Library/Mobile Documents/com~apple~CloudDocs/My Drive/Projects/Ji_Multimodal_analysis_SCC_2020/scanpy_cSCC_analysis_Khavari/KhavariCell_sc_workflow_v3_noHVG_subset_24Sep23.h5ad",
        "Lyko": "/Users/ankitpatel/Library/Mobile Documents/com~apple~CloudDocs/My Drive/Projects/IMP_info/From_Alex/Nat_comm_Lyko_CAFs_2023/Lyka_scanpy_pipeline_v2_11Dec23.h5ad",
        "Zou": "/Users/ankitpatel/Library/Mobile Documents/com~apple~CloudDocs/My Drive/Projects/IMP_info/From_Alex/eLife_Zou_etal_2023_scRNAseq/aksccZou_sc_workflow_v2_12Jul23.h5ad"
    }

    # If selected_datasets is None, use all available datasets
    if selected_datasets is None:
        selected_datasets = list(data_dirs.keys())

    # Filter the datasets based on selection
    filtered_data_dirs = {name: path for name, path in data_dirs.items() if name in selected_datasets}

    if not filtered_data_dirs:
        print("No valid datasets selected.")
        return

    # Ensure color is a list
    if isinstance(color, str):
        color = [color]

    # Process datasets one by one to prevent memory overload
    for name, path in filtered_data_dirs.items():
        print(f"Processing dataset: {name}")

        # Read AnnData object
        adata = sc.read_h5ad(path)

        # Create subplots for multiple colors
        fig, axes = plt.subplots(1, len(color), figsize=(5 * len(color), 5))

        if len(color) == 1:
            axes = [axes]  # Ensure axes is iterable when there's only one color

        # Plot UMAP for each color
        for ax, c in zip(axes, color):
            sc.pl.umap(adata, color=c, color_map='RdPu', frameon=False,
                       legend_loc='on data', legend_fontsize=7, ax=ax, show=False)
            ax.set_title(f"{name} - {c}")

        plt.tight_layout()

        # Save or show the plot
        if save_path:
            plt.savefig(f"{save_path}_{name}.png", dpi=300, bbox_inches='tight')
            print(f"UMAP plot for {name} saved to {save_path}_{name}.png")
        else:
            plt.show()

        # Free up memory
        del adata
        gc.collect()  # Force garbage collection

    print("All selected datasets processed.")
