from plotnine import *


file_path_ = '/data/BCI-SingleCell/Ankit/SCVI_sanofi_analysis/celltype_abundance_plots_for_all_TME_subcompartments/'


### FOR B CELLS

prep_table = pd.read_csv(f'{file_path_}Bcells_abundance_plot_final.csv', index_col=None)
prep_table



p1 = (ggplot(prep_table, aes(x='V2', y='V1', color='V1', size='sig_p')) +
      geom_point() +
      geom_vline(xintercept=0) +
      scale_color_manual(values=prep_table['colors'].tolist()) +
      labs(x="cell_type abundance coefficient", y="", title="Bcell types",  subtitle="PL               cSCC") +
      scale_size_manual(values=[2, 3.5, 5.5, 6.5, 8]) +
      #scale_color_discrete(guide=False) +
      xlim(-0.22, 0.2) +
      geom_segment(aes(y='V1', yend='V1', x='Y', xend='V2'), size=0.4) +
      theme_bw() +
      theme(panel_grid_major=None, panel_grid_minor=None) +
      theme(figure_size=(2.2, 2)) +
      theme(legend_position='none') +
      #ggtitle("Normal          cSCC") +
      theme(
            plot_title=element_text(size=7, face="bold", hjust = 0.5),
            plot_subtitle=element_text(size=6, face='italic', color='red', hjust=0.5),
            text=element_text(size=4),
            axis_text_x=element_text(colour="black", size=6),
            axis_text_y=element_text(colour="black", size=7)
          )
     )

print(p1)