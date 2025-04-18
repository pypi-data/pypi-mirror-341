



import numpy as np
import pandas as pd
from anndata import AnnData

def celltype_relabel_in_same_column(adata: AnnData, column_to_change: str, label_to_change, relabel_into):
    """
    Relabel specified cluster labels within the same column of an AnnData object.

    Parameters:
        adata (AnnData): The AnnData object containing the observation metadata.
        column_to_change (str): The column in `adata.obs` where labels need to be changed.
        label_to_change (str or list): The original labels to be replaced.
        relabel_into (str or list): The new labels to replace with.

    Returns:
        AnnData: Updated AnnData object with relabeled cluster values.
    """
    # Convert inputs to lists if they are not already
    if isinstance(label_to_change, str):
        label_to_change = [label_to_change]
    if isinstance(relabel_into, str):
        relabel_into = [relabel_into] * len(label_to_change)

    # Validate inputs
    if len(label_to_change) != len(relabel_into):
        raise ValueError("Both `label_to_change` and `relabel_into` must have the same length.")

    # Create a mapping dictionary and apply the changes efficiently
    relabel_dict = dict(zip(label_to_change, relabel_into))
    adata.obs[column_to_change] = adata.obs[column_to_change].replace(relabel_dict)

    return adata



from statsmodels.formula.api import ols
from scipy.stats import mannwhitneyu

def zurr_cell_type_abundance_local(mc, 
                                   annotation = 'annotation',
                                   sample_types = 'sample_types',
                                   sample_ID = 'sample_ID',
                                   sample_types_1 = 'cSCC', 
                                   sample_types_2 = 'PL'):
    
    """
    mc: anndata metadata dataframe. length should be equal to the desired TME, where the proportion of the 
    annotated cell type needs to be tested
    sample_types: conditions
    sample_ID: patient ID
    sample_types_1: tumour or treatment condition
    sample_types_2: normal or PL condition    
    
    """
    
    
    # Convert 'annotation' column to character
    mc[annotation] = mc[annotation].astype(str)
    mc[sample_types] = mc[sample_types].astype(str)
    mc[sample_ID] = mc[sample_ID].astype(str)
    
    # Calculate fractions
    x = mc.groupby([sample_ID, sample_types, annotation]).size().reset_index(name='n')
    x['fraction'] = x['n'] / x.groupby([sample_ID, sample_types])['n'].transform('sum')
    x['total'] = x.groupby([sample_ID, sample_types])['n'].transform('sum')
    
    
    # Prepare table
    prep_table = pd.DataFrame({'V1': x[annotation].unique(),
                               'V2': 'none',
                               'V3': 'none'})

    counter = 0
    for cell_t in prep_table['V1']:
        fractions_x_sub = x[x[annotation].isin([cell_t])]
        fractions_x_sub[sample_types] = pd.Categorical(fractions_x_sub[sample_types], categories=[sample_types_1, sample_types_2])

        # Linear regression
        model = ols('fraction ~ C(sample_types)', data=fractions_x_sub).fit()
        slope_sub = model.params[1]
        R2 = model.rsquared



        # Assuming fractions_x_sub is a DataFrame in Python
        scc_values = fractions_x_sub[fractions_x_sub[sample_types] == sample_types_1]['fraction']
        pl_values = fractions_x_sub[fractions_x_sub[sample_types] == sample_types_2]['fraction']

        #test_statistic, p_value = ranksums(pl_values, scc_values)

        test_statistic, p_value = mannwhitneyu(pl_values, scc_values)


        prep_table.at[counter, 'V2'] = ((-slope_sub) / abs(slope_sub)) * R2
        prep_table.at[counter, 'V3'] = p_value
        counter += 1
        
    
    #update prep table
    prep_table['V2'] = pd.to_numeric(prep_table['V2'])
    prep_table['V3'] = pd.to_numeric(prep_table['V3'])
    prep_table['Y'] = 0

    # Order prep_table based on 'V2' and 'V3'
    prep_table = prep_table.sort_values(by=['V2', 'V3'])
    
    
    # Add p-value cutoffs and color cell states
    prep_table['sig_p'] = 'p>0.5'
    prep_table.loc[prep_table['V3'] < 0.3, 'sig_p'] = 'p<0.5'
    prep_table.loc[prep_table['V3'] < 0.1, 'sig_p'] = 'p<0.1'
    prep_table.loc[prep_table['V3'] < 0.05, 'sig_p'] = 'p<0.05'
    prep_table.loc[prep_table['V3'] < 0.01, 'sig_p'] = 'p<0.01'


    # Convert 'sig_p' to a factor with specified levels
    levels_order = ["p>0.5", "p<0.5", "p<0.1", "p<0.05", "p<0.01"]
    prep_table['sig_p'] = pd.Categorical(prep_table['sig_p'], categories=levels_order, ordered=True)


    ##assigning colour column

    # Read the text file into a DataFrame
    #colours = 'final_annotations_colors_JAN2025.txt'
    colours = 'cell_type_colors.txt'
    col_path = colours
    col_mc = pd.read_table(col_path,)
    col_mc = col_mc.rename(columns={'annotation': 'V1'})

    # Now replace 'Annotation' with 'mc' annotation
    col_mc = col_mc[col_mc.V1.isin(prep_table['V1'])]
    
    #merging col_mc and prep_table
    prep_table = pd.merge(prep_table, col_mc, on='V1')
    
    # Remove rows with missing values
    prep_table = prep_table.dropna()

    # Set color to "grey" for rows where 'V3' > 0.1 in colors_mc_1
    prep_table.loc[prep_table['V3'] > 0.1, 'colors'] = 'grey'
    
    # Set 'V1' as a factor with its own levels
    prep_table['V1'] = pd.Categorical(prep_table['V1'], categories=prep_table['V1'].unique())

    # Display the resulting DataFrame
    #print(col_mc)
    print(prep_table)

    return prep_table


from plotnine import (
    ggplot, aes, geom_point, geom_vline, scale_color_manual,
    labs, scale_size_manual, geom_segment, theme_bw, theme,
    element_text, xlim
)

def plot_cell_type_abundance(prep_table, sample_type1, sample_type2, output_path="figures/cell_type_abundance.pdf"):
    # Calculate x-axis limits
    min_x = prep_table["V2"].min() - 0.2
    max_x = prep_table["V2"].max() + 0.2

    # Calculate subtitle positions
    midpoint_neg = min_x / 2
    midpoint_pos = max_x / 2

    # Create plot
    p = (ggplot(prep_table, aes(x='V2', y='V1', color='V1', size='sig_p')) +
         geom_point() +
         geom_vline(xintercept=0) +
         scale_color_manual(values=prep_table['colors'].tolist()) +
         labs(x="Cell Type Abundance Coefficient", y="", title="All Cell Types") +
         scale_size_manual(values=[2, 3.5, 5.5, 6.5, 8]) +
         xlim(min_x, max_x) +
         geom_segment(aes(y='V1', yend='V1', x='Y', xend='V2'), size=0.4) +
         theme_bw() +
         theme(panel_grid_major=None, panel_grid_minor=None) +
         theme(figure_size=(5, 5)) +
         theme(legend_position='none') +
         theme(
             plot_title=element_text(size=9, face="bold", hjust=0.5),
             text=element_text(size=8),
             axis_text_x=element_text(colour="black", size=11),
             axis_text_y=element_text(colour="black", size=9)
         ) +
         # Custom subtitles positioned at midpoint of negative and positive x-values
         labs(subtitle=f"{sample_type2:>15}{' ' * 30}{sample_type1:<15}")  # Adjust spacing
        )

    # Save plot
    p.save(output_path, width=6, height=6, dpi=600)

    return p