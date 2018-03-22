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

Graph_util module has a function create_edges that takes an organization name along with abstract data processed with id_abstracts to create edge data for a networkx graph indicating how many abstracts contained the org name of interest along with others from the list. Essentially, it tracks the extent to which one organization is collaborating with others in the list.
