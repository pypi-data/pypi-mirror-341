################################################################
################## Load python packages ###########################
################################################################
import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from scipy.stats import mannwhitneyu
import random

import warnings
warnings.filterwarnings('ignore')

pd.set_option("display.max_columns", 500)

pd.set_option("display.max_rows", 500)


################################################################
################## TO RUN R PACKAGES ###########################
################################################################

def colurs_file_update(mc, annotation ='annotation'):
    """
    mc: dataframe 
    annotation: cell_type labelling colummn in mc dataframe
    
    """
    
    # Read the text file into a DataFrame
    colours = 'colours_Barts_clusters_updated.txt'
    col_path = f"/data/home/hmy327/sanofi_Liu_scvi_labelling/colors_files/{colours}"
    col_mc = pd.read_table(col_path,)
    
    mc[annotation] = mc[annotation].astype(str)
    col_mc[annotation] = col_mc[annotation].astype(str)
    
    # Filter cell types that are not in col_mc['annotation']
    cell_types = list(np.unique(mc.annotation))
    
    #create list of col_mc.annotation
    all_cell_types = list(np.unique(col_mc.annotation))
    
    #creating list of these unique cell_types
    list3 = [cell_type for cell_type in cell_types if cell_type not in all_cell_types]
    print(list3)
    
    # Function to generate unique hex colors
    def generate_unique_colors(num_colors):
        colors = set()
        while len(colors) < num_colors:
            colors.add('#{:06x}'.format(random.randint(0, 256**3-1)))
        return list(colors)

    if list3:
        
        # Generate unique hex colors for each cell type in list3
        unique_colors = generate_unique_colors(len(list3))

        # Filter out colors that are not present in other_df['hex_colors']
        unique_colors_filtered = [color for color in unique_colors if color not in col_mc['annotation'].tolist()]

        # Create DataFrame with list3 cell types and unique colors if any
        while not unique_colors_filtered:
            print("No unique colors available. Generating new colors...")
            unique_colors = generate_unique_colors(len(list3))
            unique_colors_filtered = [color for color in unique_colors if color not in col_mc['annotation'].tolist()]

        data = {'annotation': list3[:len(unique_colors_filtered)], 'colors': unique_colors_filtered}
        new_col_df = pd.DataFrame(data)
        #print(new_col_df)

        # now add merge this df with col_mc
        col_mc = pd.concat([col_mc, new_col_df])
        print(col_mc)

        #now save this new col_mc df and replace the existing one
        col_mc.to_csv(col_path, sep='\t', index=False)
        
    else:
        print('there are no new cell_types in mc.annotation')

    
    
    
    

#calculating cell type abundance in prep_table
def zurr_cell_type_abundance(mc,
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
    colours = 'colours_Barts_clusters_updated.txt'
    col_path = f"/data/home/hmy327/sanofi_Liu_scvi_labelling/colors_files/{colours}"
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



# from plotnine import *


# # Assuming prep_table and colors_mc_1 are your DataFrames
# # Also, make sure 'sig_p', 'V1', 'V2', and 'Y' columns exist in prep_table

# p1 = (ggplot(prep_table, aes(x='V2', y='V1', color='V1', size='sig_p')) +
#       geom_point() +
#       geom_vline(xintercept=0) +
#       scale_color_manual(values=prep_table['colors'].tolist()) +
#       labs(x="cell_type abundance coefficient", y="", title="Barts Lymphoid cell types",  subtitle="PL                             cSCC") +
#       scale_size_manual(values=[2, 3.5, 5.5, 6.5, 8]) +
#       #scale_color_discrete(guide=False) +
#       xlim(-0.57, 0.32) +
#       geom_segment(aes(y='V1', yend='V1', x='Y', xend='V2'), size=0.4) +
#       theme_bw() +
#       theme(panel_grid_major=None, panel_grid_minor=None) +
#       theme(figure_size=(3, 4)) +
#       theme(legend_position='none') +
#       #ggtitle("Normal          cSCC") +
#       theme(
#             plot_title=element_text(size=7, face="bold", hjust = 0.5),
#             plot_subtitle=element_text(size=6, face='italic', color='red', hjust=0.5),
#             text=element_text(size=6),
#             axis_text_x=element_text(colour="black", size=6),
#             axis_text_y=element_text(colour="black", size=7)
#           )
#      )

# print(p1)
