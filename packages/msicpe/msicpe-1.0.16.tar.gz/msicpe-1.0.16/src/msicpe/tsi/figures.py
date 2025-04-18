import numpy as np

# from plotly import express as px
# from plotly import subplots as splt
# import pandas   


def add_legend(fig,legend):
    item_map={f'{i}':key for i, key in enumerate(legend)}
    fig.for_each_annotation(lambda a: a.update(text=item_map[a.text.split("=")[1]]))