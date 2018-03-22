# pubclasr
Exploring ways to analyze and classify pubmed scientific abstracts using python
# requirements
Requires python 2.7 with:
1. numpy
2. pandas
3. matplotlib
4. networkx
# functionality
Process module has a function (processXml) used to import pubmed abstract data (in XML file format) and return a pandas dataframe with key abstract content such as Title, Journal, Abstract, Authors, and Affiliations extracted into separate variables. id_abstracts takes a list of organization names stored as character strings and appends variables to the dataframe of abstracts indicating whether the name was included as an Affiliation.

Graph_util module has a function create_edges that takes an organization name along with abstract data processed with id_abstracts to create edge data for a networkx graph indicating how many abstracts contained the org name of interest along with others from the list. Essentially, it tracks the extent to which one organization is collaborating with others on the list.
# example
## research question
To understand how many times the company that I work for (Evidera) collaborated with big pharma companies on research studies during the last 5 years. A collaboration is defined as having the Evidera affiliation listed along with one of the orgs from the list of big pharma. 
## the data
A list of abstracts (in XML file format) containing the affiliation "Evidera" (search string: "Evidera[Affiliation]") was generated using PubMed. The abstracts were filtered to include only those containing Abstract text and a publication date within the last 5 years. The example data file is saved as "pubmed_result.xml". 

Note: only including abstracts that contain Abstract text is important, else the processXml function will not work.
## code
def foo():
    if not bar:
        return True

