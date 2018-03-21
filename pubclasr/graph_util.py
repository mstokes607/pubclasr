import pandas as pd
import numpy as np

'''
Creates edge data corresponding to consulting company pubs that were linked to a pharma company

inputs consultco_name: text string
        pharma_lst: list of pharma companies used to identify pubs linked to pharma
        consultco_pubs_data: summary dataframe of abstract counts where consulting company worked with a pharma co

output edge_data: list of tuples denoting links between the consulting company and pharma along with number of abstracts
                   provided as the weight (e.g., [(evi,pfizer,2),(evi,novartis,1),...]        
'''

def create_edges(consultco_name, consultco_pubs_data):

    # explore creation of weighted edge data for network graph using summary data
    edge_data = [(consultco_name, pharma, int(consultco_pubs_data.values[list(consultco_pubs_data.index).index(pharma)])) 
                for pharma in consultco_pubs_data.index 
                    if consultco_pubs_data.values[list(consultco_pubs_data.index).index(pharma)] >= 1]
                    
    return edge_data
