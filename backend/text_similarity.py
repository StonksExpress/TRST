import tensorflow as tf
import tensorflow_hub as hub
import sklearn.metrics.pairwise as pw
import numpy as np
import nltk
import math
from scrape_analyse import scrapeAnalyse
from newspaper import Article
import data.data as dat
from urllib.parse import urlparse
from scipy import spatial
import random

class embeddings:
    mod_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
    #def __init__(self):
        #self.embed = hub.Module(self.mod_url)

    def USE_embedding(self,_documents):
        #takes multiple documents (ie a list of strings)
        #
        if isinstance(_documents, str): documents = [_documents]
        else: documents =_documents
        document_sentences = [document.strip().split('.') for document in documents]

        g = tf.Graph()
        with g.as_default():
            similarity_input_placeholder = tf.placeholder(dtype=tf.string, shape=[None])
            embed = hub.Module(self.mod_url)
            embedded_text = embed(similarity_input_placeholder)
            init_op = tf.group([tf.global_variables_initializer(),tf.tables_initializer()])
        g.finalize()

        session = tf.Session(graph = g)
        session.run(init_op)
        #finished init of model

        #old code
        # similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
        # similarity_message_encodings = embed(similarity_input_placeholder)
        # with tf.Session() as session:
        #   session.run(tf.global_variables_initializer())
        #   session.run(tf.tables_initializer())
        #   document_sentence_embeddings = [session.run(embed(sentences)) for sentences in document_sentences ]

        # document_sentence_embeddings = session.run(embedded_text, feed_dict={similarity_input_placeholder: document_sentences})

        # return document_sentence_embeddings

        return [session.run(embedded_text, feed_dict={similarity_input_placeholder: document}) for document in document_sentences]

def cosine_pair_embed_similarity(embeddings1, embeddings2):
    #return pw.cosine_similarity(embeddings1, embeddings2)

    arr_big, arr_small = (np.array(embeddings1),np.array(embeddings2)) if len(embeddings1) > len(embeddings2) else (np.array(embeddings2),np.array(embeddings1))
    # print(f"yeetus{np.shape(arr_small)}")
    # print("\n\n\n\n\n\n\n")
    similarities = [max( 1 - spatial.distance.cosine(big_embed, small_embed) for big_embed in arr_big) for small_embed in arr_small]
    # print(np.shape(similarities))
    # print("\n\n\n\n")
    print(np.shape(similarities))
    return np.mean(similarities)


def total_similarity(timestamp,embedding,embeddings,embeddings_times,sf_norm=1,sf_dropoff=0):
    #use kernel of size a day
    #convolve with points
    #scale with exponential
    #
        #k + k*s(-x)
    # for x in zip(embeddings,embeddings_times):
    #     print(f"\n\n\n\n\n\n\n{x}\n\n\n\n\n\n\n\n\n")
    zipped_and_sorted = sorted(zip(embeddings,embeddings_times), key=lambda x: x[1])
    results_similarity = [cosine_pair_embed_similarity(embedding,x[0]) for x in zipped_and_sorted]
    print(np.shape(results_similarity))
    out = (np.mean(results_similarity))
    # print("\n\nlmao\n\n\n\n\n\n")
    # print(len(results_similarity))
#     #time stuff
#     left = filter(lambda x: x[1] < timestamp, zipped_and_sorted)
#     right = zipped_and_sorted[len(list(left)):]
#     left_times = [x[1] for x in left]
#     right_times = [x[1] for x in right]
#     left_data = [x[0][len(left_times)] for x in left]
#     right_data = [x[0][len(right_times)] for x in right]
#     # left_data = results_similarity[:len(list(left))]
#     # right_data = results_similarity[len(list(left)):]
#     # print(np.shape(right_data))

#     left_time_diffs = [timestamp-x[1] for x in reversed(list(left))]
#     right_time_diffs = [x[1]-timestamp for x in right]

#     inter_right_time_diffs = [b-a for (a,b) in zip([timestamp] + right_times, right_times)]
#     inter_left_time_diffs = [b-a for (a,b) in zip(left_times + [timestamp], left_times[1:] + [timestamp])]
#     max_diff = max(inter_left_time_diffs + inter_right_time_diffs)

# #   scaling factor depending on density
#     #sf_norm=0.1
#     norm_scaling_left = [1-math.exp(sf_norm*max_diff/(x + 1)) for x in left_time_diffs]
#     norm_scaling_right = [1-math.exp(sf_norm*max_diff/(x + 1)) for x in right_time_diffs]
# #   scaling factor depending on distance from queried
#     #sf_dropoff=0.1
#     time_scaling_func = lambda x: math.exp(-sf_dropoff*x)
#     scaled_similarities = [x * y for x, y in zip(left_data+right_data,norm_scaling_left+norm_scaling_right)]
#     scaled_similarities = [x*time_scaling_func(y) for (x,y) in zip(scaled_similarities,left_time_diffs+right_time_diffs)]
        # print("lmao \n\n\n\n\n\n")
    #print(scaled_similarities)

    # TODO: return something
    print(out)
    return out
    # scaled similarities are the exponential curved and time density scaled values
    # results similarity is simply the max pairwise similarities between each document pair
def get_score(url):
    #check if present in db
        #return db value if true
    result = dat.Classification.retrieve(url)
    if(result is not None): return result.trust
    #else
    #
    # keywords = scrapeAnalyse(url, False, None)
    (text, keywords, date) = scrapeAnalyse(url, False, None)
    my_data = scrapeAnalyse(None, True, keywords)
    for x in my_data:
        print(f"\n\n\n\n{x}\n\n\n\n\n")
    #mydata is a list of dictionaries
    #   each dictionary contains 3 fields:
    #   -text
    #   -date
    #   -url
    embed_batch=[]
    for dict in my_data:
        doc_embed = dat.Document.retrieve(dict['url'])
        if (doc_embed is not None):
            dict['embed'] = doc_embed.vector
            dict['stored'] = True
        else:
            embed_batch.append(dict['text'])
            dict['stored'] = False
    embed_batch.append(text)
    embed_inst = embeddings()

    embeds = embed_inst.USE_embedding(embed_batch)
    for dict in my_data:
        if dict.get('embed') is None:
            dict['embed'] = embeds[0].copy()
            del embeds[0]


    for dict in my_data:
        if dict['stored'] is False:
            parsed_uri = urlparse(dict['url'])
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            dat.Document.new(domain,dict['url'],dict['date'],dict['embed'])

    searched_embeddings = [x['embed'] for x in my_data]
    searched_timestamps = [x['date'] for x in my_data]
    print(len(searched_embeddings))
    trust = total_similarity(date,embeds[0],searched_embeddings,searched_timestamps)

    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    dat.Document.new(domain,url,date,embeds[0])
    dat.Classification.new(domain,url,trust,date)
    return trust