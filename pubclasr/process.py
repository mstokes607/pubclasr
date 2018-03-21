import xml.etree.cElementTree as et
import pandas as pd
import numpy as np

def processXml(filename):
    tree = et.parse(filename)
        
    # PMID
    lst1 = tree.findall('PubmedArticle/MedlineCitation')
    pmids = [item.find('PMID').text for item in lst1]

    # Title
    lst2 = tree.findall('PubmedArticle/MedlineCitation/Article')
    titles = [item.find('ArticleTitle').text for item in lst2]

    # Journal
    lst3 = tree.findall('PubmedArticle/MedlineCitation/Article/Journal')
    journals = [item.find('Title').text for item in lst3]

    # Abstract Text
    lst4 = tree.findall('PubmedArticle/MedlineCitation/Article/Abstract')
    abstracts = [[other_item.text for other_item in item.findall('AbstractText')] for item in lst4]

    # Affiliation
    lst5 = tree.findall('PubmedArticle/MedlineCitation/Article/AuthorList')
    affiliations = [[other_item.text.lower() for other_item in item.findall('Author/AffiliationInfo/Affiliation')] for item in lst5] 
    
    affil_str = [" ".join(item) for item in affiliations]
    
    data = pd.DataFrame({'pmid': pmids, 'journal':journals, 'affiliation_lst':affiliations, 'affiliations':affil_str,
                         'title':titles, 'abstract':abstracts})
    
    return data
    
# create empty dataframe of vars indicating whether a pharma company was listed in the affiliations of an abstract
def id_abstracts(data_to_id, co_lst, anyflag=None): 
    moredata = np.array([np.zeros(len(data_to_id))]*len(co_lst)).T 
    df_ = pd.DataFrame(moredata, index=data_to_id.index, columns=co_lst)
    if anyflag == 1: df_['any'] = 0

    # identify which abstracts contained a pharma company affiliation
    affil_lst = data_to_id['affiliations'].tolist()
    for co in co_lst:
        for item in affil_lst:
            if co in item: 
                df_.iloc[affil_lst.index(item) , co_lst.index(co)] = 1 # flag for company
                if anyflag == 1 : df_.iloc[affil_lst.index(item), len(co_lst)] = 1 # flag for any
    
    # merge affiliation indicators with abstract data
    data_to_id = data_to_id.join(df_)
    return data_to_id