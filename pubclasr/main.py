from pubclasr import process
from pubclasr import graph_util

import pandas as pd
import numpy as np

import networkx as nx
import matplotlib.pyplot as plt

# process the raw text abstract file -> dataframe of abstract texts, titles, and journal info is returned
filename = '/Users/nathmorissette/miniconda2/envs/pubclasr/pubclasr/pubmed_result.xml'
data = process.processXml(filename)

# id abstracts with pharma companies in abstract affiliations
pharma_lst = ['pfizer','novartis','roche ','sanofi','merck','gilead','johnson and johnson','glaxo', 'takeda', 'astrazeneca',
              'bristol-myers']
              
pharma = process.id_abstracts(data, pharma_lst, anyflag=1)
subset = pharma[pharma['any']==1]
print 'pharma pubs'
print subset[pharma_lst].sum()
print '\n'

co_lst = ['evidera']      
evi = process.id_abstracts(subset, co_lst, anyflag=0)
evi = evi[evi['evidera']==1]
print 'subset pharma pubs with evidera'
print evi[pharma_lst].sum()
print '\n'

evi_data = evi[pharma_lst].sum()
evi_edges = graph_util.create_edges('evi', evi_data)

# Create the Graph data - circular graph with consulting company at the center
# Edge weights correspond to number of publications
def create_graph(node_data, edge_data):
    G = nx.Graph()
    G.add_nodes_from(node_data)
    G.add_weighted_edges_from(edge_data)
    pos = nx.circular_layout(G, scale=0.05)
    pos[edge_data[0][0]] = np.array([0, 0]) # puts the consulting company at the center

    # Graph with edge and node labels
    color_map = list()
    for node in G.nodes: # color code the consulting group and pharma nodes separately
        if node == edge_data[0][0] : color_map.append('#ADD8E6')
        else : color_map.append('#F8F8F8')
    nx.draw(G,pos, node_size=400, node_color=color_map, with_labels=True, font_size=8)
    edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels, font_size=8)
    plt.show()
    
create_graph(list(evi_data.index), evi_edges)