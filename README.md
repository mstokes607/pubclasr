# pubclasr
Exploring ways to analyze and classify pubmed scientific abstracts using python
# requirements
Requires python 2.7 with:
1. numpy
2. pandas
3. matplotlib
4. networkx
# functionality
The processXml function (in process.py) is used to import pubmed abstract data (in XML file format) and return a pandas dataframe with key abstract content such as Title, Journal, Abstract, Authors, and Affiliations extracted into separate variables. The function id_abstracts can take a list of organization names stored as character strings and appends variables to the dataframe of abstracts indicating whether the name was included as an Affiliation.

The function create_edges (in graph_util.py) takes an organization name along with abstract data processed with id_abstracts to create edge data for a networkx graph indicating how many abstracts contained the org name of interest along with others from the list. Essentially, it tracks the extent to which one organization is collaborating with others on the list.
# example
## research objective
To calculate the number of times that Evidera (the company I work for) collaborated with big pharma companies on research studies during the last 5 years. A collaboration is defined as having the Evidera affiliation listed along with one of the organizations from the list of big pharma. 
## the data
A list of abstracts (in XML file format) containing the affiliation "Evidera" (search string: "Evidera[Affiliation]") was generated using PubMed. The abstracts were then filtered to include only those containing Abstract text and a publication date within the last 5 years. The example data file is saved as "pubmed_result.xml". 

Note: In order for the processXml function to work, it is important to only include abstracts that contain Abstract text.
## code
    # excerpt from main.py
    from pubclasr import process
    from pubclasr import graph_util

    # load the raw data
    filename = '~/pubclasr/pubmed_result.xml'
    data = process.processXml(filename)
    
    # id abstracts with pharma companies in abstract affiliations
    pharma_lst = ['pfizer','novartis','roche ','sanofi','merck','gilead','johnson and johnson', 'johnson & johnson', 'glaxo', 
              'gsk', 'takeda', 'astrazeneca', 'bristol-myers']
              
    pharma = process.id_abstracts(data, pharma_lst, anyflag=1)
    subset = pharma[pharma['any']==1]

    # clean up where two vars referenced the same organization
    condition = (subset['glaxo'] == 1) | (subset['gsk'] == 1)
    subset['glaxosmithkline'] = np.where(condition, 1, 0) 
    condition2 = (subset['johnson and johnson'] == 1) | (subset['johnson & johnson'])
    subset['j&j'] = np.where(condition2, 1, 0) 
    subset = subset.drop(['glaxo','gsk', 'johnson and johnson', 'johnson & johnson'], axis=1)
    pharma_lst = [e for e in pharma_lst if e not in ('gsk', 'glaxo', 'johnson and johnson', 'johnson & johnson')]
    pharma_lst.append('glaxosmithkline')
    pharma_lst.append('j&j')

    evi_data = subset[pharma_lst].sum()
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
        
    create_graph(evi_data.index.values, evi_edges)
 ## output   
 **Figure.** Number of evidera pubs with big pharma (last 5 years)
![alt text](https://github.com/mstokes607/pubclasr/blob/master/pubclasr/evi_graph.png)
