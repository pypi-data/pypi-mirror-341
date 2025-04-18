#ORIGINAL
prep_table = pd.read_csv('prep_table_final.csv')
prep_table

prep_table['group'] = prep_table['group'].astype('category')
prep_table['group'] = prep_table['group'].cat.reorder_categories(['Zou_et_al_2023','Schutz_et_al_2023','Ji_et_al_2020','Barts'], ordered=True)

prep_table['V1'] = prep_table['V1'].astype('category')

custom_order = ['HSPA1_Mac','cDC2','LAMP3_cDC','ZFAT_pDC',
                'Th17','Treg_activated','Treg_naive_like','Tcm','Tn_CD4',
                'Teff_c','Teff_GZMK','Tex']

prep_table['V1'] = pd.Categorical(prep_table['V1'], categories=custom_order, ordered=True)


from plotnine import *

# Create a grouped barplot with plotnine
plot = (
    ggplot(prep_table, aes(x='V1', y='V2', fill='group'))
    + geom_col(position='dodge', width=0.8, color='black')
    + labs(title='Grouped Barplot with Plotnine', x='V1', y='V2')
    #+ theme(figure_size=(1, 1))
    + labs(x="", y="cell_type abundance coefficient", title="Cell type abundance validation with published cSCC datasets", subtitle="PL/Normal                                    cSCC")
    + theme_minimal()
    + theme(
            plot_title=element_text(size=11, face="bold", hjust = 0.5),
            plot_subtitle=element_text(size=6, face='italic', color='red', hjust=0.5),
            text=element_text(size=10),
            axis_text_x=element_text(colour="black", size=8, angle=0, hjust=0.5),
            axis_text_y=element_text(colour="black", size=11)
          )
    + coord_flip()
)

# Show the plot
print(plot)

