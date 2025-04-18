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




#function to get signature score (gene list from Chu et al. 2023) analysis
def signature_score_Chu_analysis(adata):
    
    DATA_DIR_markers = "/data/BCI-SingleCell/Ankit/SCVI_sanofi_analysis/"
    
    markers = pd.read_excel(f'{DATA_DIR_markers}Figure2E_marker_list.xlsx')
    
    gene_list = []

    for column in markers.columns:
        list_1 = markers[column].dropna().tolist()
        gene_list.append(list_1)
        #print(gene_list)
        
    gene_columns = list(markers)
    #gene_columns
    
    #assign gene column to lists

    # Create a dictionary to assign names to lists
    named_list = {}

    # Iterate over the lists and names
    for name, lst in zip(gene_columns, gene_list):
        named_list[name] = lst
        
    print(named_list)
    
    ## calculating score now
    adata = sc.tl.score_genes(adata,
                           gene_list = named_list['Naive'],
                           score_name = "Naive",
                           copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Activation_Effector_function'],
                               score_name = "Activation_Effector_function",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Exhaustion'],
                               score_name = "Exhaustion",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['TCR_Signaling'],
                               score_name = "TCR_Signaling",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Cytotoxicity'],
                               score_name = "Cytotoxicity",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Cytokine_Cytokine_receptor'],
                               score_name = "Cytokine_Cytokine_receptor",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Chemokine_Chemokine_receptor'],
                               score_name = "Chemokine_Chemokine_receptor",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Senescence'],
                               score_name = "Senescence",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Anergy'],
                               score_name = "Anergy",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['NFKB_Signaling'],
                               score_name = "NFKB_Signaling",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Stress_response'],
                               score_name = "Stress_response",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['MAPK_Signaling'],
                               score_name = "MAPK_Signaling",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Adhesion'],
                               score_name = "Adhesion",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['IFN_Response'],
                               score_name = "IFN_Response",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Oxidative_phosphorylation'],
                               score_name = "Oxidative_phosphorylation",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Glycolysis'],
                               score_name = "Glycolysis",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Fatty_acid_metabolism'],
                               score_name = "Fatty_acid_metabolism",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Pro_apoptosis'],
                               score_name = "Pro_apoptosis",
                               copy = True)

    adata = sc.tl.score_genes(adata,
                               gene_list = named_list['Anti_apoptosis'],
                               score_name = "Anti_apoptosis",
                               copy = True)
    
    return adata


#first selecting specific sample_types and making scaled df for heatmap
def sample_types_sig_score_TO_df(adata):
    
    answer = input("sig scores by sample types - yes/no: ")
    if answer == 'yes':
        input_sample_types = input('adata.obs sample_types: ')
        adata = adata[adata.obs.sample_types == input_sample_types]
        adata
        
    else:
        print('sign scores by whole object')
    
    groupby_obs_column_name = input('groupby_obs_column_for_mean == ')
    
    
    
    markers_score = pd.DataFrame(adata.obs, 
                                 columns = [groupby_obs_column_name,
                                            'Naive', 'Activation_Effector_function', 'Exhaustion', 'TCR_Signaling', 
                                            'Cytotoxicity', 'Cytokine_Cytokine_receptor', 'Chemokine_Chemokine_receptor', 
                                            'Senescence', 'Anergy', 'NFKB_Signaling', 'Stress_response', 'MAPK_Signaling', 
                                            'Adhesion', 'IFN_Response', 'Oxidative_phosphorylation', 'Glycolysis', 
                                            'Fatty_acid_metabolism', 'Pro_apoptosis', 'Anti_apoptosis'])

    #Getting the mean of all scores

    grouped_df = markers_score.groupby(groupby_obs_column_name).mean()
    grouped_df

    ## scaling all mean values

    scaled_df = (grouped_df - grouped_df.mean()) / grouped_df.std()
    scaled_df
    
    #declaring df as global variable
    global df_1
    
    # Transpose the DataFrame
    df_1 = scaled_df.transpose()

    
    
    #df_1.to_csv('transposed_df_scc_sig_score_26Oct23.csv', index=True)
    
    return df_1


def CD8_KLRB1_sig_plot_with_Chu_etal_genes_list():
    
    df_1 = pd.read_csv('/data/home/hmy327/sanofi_Liu_scvi_labelling/SoupX_HR9LR1_cleaned_Sanofi_Tcells_Bcells/sanofi_scc_cd8_chu_sig_scores_9Jan24.csv', index_col=0)
    
    
    # Set the figure size
    #plt.figure(figsize=(8, 8))
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.grid(False)

    # Define the desired order of x-axis labels
    custom_order = ['NK_FGFBP2','NK_XCL1', 'Teff_c', 'Tex', 'Teff_KLRD1','Teff_KLF2', 'Teff_DUSP4', 'Teff_GZMK','Teff_TRBV', 'Teff_Tisg', 'Tmem', 'Tn_TCF7']

    # Reorder the columns based on the custom order
    df_1 = df_1.reindex(columns=custom_order)


    # Create your own group labels for the y-axis (replace this with your actual labels)
    # For demonstration, dividing 10 rows into 4 groups
    #group_labels = ['Differentiation'] * 3 + ['Function'] * 11 + ['Metabolism'] * 3 + ['Apoptosis'] * 2


    # Plot the heatmap
    ax = sns.heatmap(df_1, annot=False, cmap="coolwarm", linewidths=0.2,
                #vmax = 0.1
                #xticklabels='auto',
                #cbar=True, 
                square=True,
                cbar_kws={"shrink": 0.5, "location": 'right', "anchor": (0, 1.0)}, fmt=".2f",)

    ax.xaxis.tick_top()
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='left')
    #plt.yticks(labels=group_labels, rotation=0)
    ax.hlines([3, 14, 17, 19], *ax.get_xlim(), linestyle='dashed', colors='black')

    # Customize the axis labels and title
    plt.xlabel("", fontsize=7)
    plt.ylabel("", fontsize=2)


    # Adjust the layout to prevent cutoff of labels
    plt.tight_layout()

    # Display the heatmap
    plt.show()
    
    return plt.show()










