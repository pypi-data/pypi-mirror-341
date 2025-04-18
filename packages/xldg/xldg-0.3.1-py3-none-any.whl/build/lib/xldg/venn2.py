# from matplotlib_venn import venn2

# class Venn2_Config:  
#     def __init__(self, label1: str, label2: str, title: str = None, size: int = 16, dpi: int = 600, x: int = 10, y: int = 10):
#         return

# # TODO: test and improve
# def build_ven2_diagram_of_xl_sites(save_path: str, xls_list1: 'CrossLinkDataset', xls_list2: 'CrossLinkDataset', config: 'Venn2_Config') -> None:
#     self.config = copy.deepcopy(config)
#     plt.figure(figsize=(10, 10), dpi=600)
    
#     set1 = set([str(sublist) for sublist in xls_list1])
#     set2 = set([str(sublist) for sublist in xls_list2])
#     venn = venn2([set1, set2], (label1, label2))

#     # Customize colors
#     venn.get_patch_by_id('10').set_color('#9AE66E') # pastel green
#     venn.get_patch_by_id('01').set_color('#FAF278') # pastel yellow
#     venn.get_patch_by_id('11').set_color('#87D5F8') # pastel blue

#     # Label the regions with the number of elements
#     for subset in ('10', '01', '11'):
#         if venn.get_label_by_id(subset):
#             venn.get_label_by_id(subset).set_text(f'{venn.get_label_by_id(subset).get_text()}')

#     # Customize font size
#     for text in venn.set_labels:
#         text.set_fontsize(size)

#     for text in venn.subset_labels:
#         if text:  # Check if the subset label is not None
#             text.set_fontsize(size)
#     if title != None:
#         plt.title(title).set_fontsize(18)

#     plt.savefig(save_path)
#     print(f'Venn2 diagram saved to {save_path}')