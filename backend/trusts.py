#somewhere to abstract trust getting
#will either fetch from server if article cached
#or     get keywords from article
#       query google with those keywords
#       return the result of the article urls (and other typical data eg article data) of those queries
#       check if any of those urls are in the database
#       the articles that aren't in the database need to be processed (ie find embeddings for non cached articles) and embeddings and data added to the database
#       for each of the items returned in the query, get the similarity of the articles, and select the max [n] similarity articles

#       also need to take into account how recent the article was?
