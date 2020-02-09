import tensorflow as tf
import tensorflow_hub as hub
import sklearn.metrics.pairwise as pw
import numpy as np
import nltk
import math
from newspaper import Article
import data.data as dat
from urllib.parse import urlparse

class embeddings:
    USE_mod_URL = "https://tfhub.dev/google/universal-sentence-encoder/2"
    def __init__(self):
        self.embed = hub.Module(module_url)

    def USE_embedding(self,_documents):
        #takes multiple documents (ie a list of strings)
        #
        if isinstance(_documents, str): documents = [_documents]
        else: documents =_documents
        document_sentences = [document.strip().split('.') for document in documents]

        g = tf.Graph():
            similarity_input_placeholder = tf.placeholder(dtype=tf.string, shape=[None])
            embedded_text = self.embed(similarity_input_placeholder)
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

        document_sentence_embeddings = session.run(embedded_text, feed_dict={text_input: document_sentences})
        return document_sentence_embeddings

def cosine_pair_embed_similarity(embeddings1, embeddings2):
    #return pw.cosine_similarity(embeddings1, embeddings2)

    arr_big, arr_small = (np.array(embeddings1),np.array(embeddings2)) if len(embeddings1) > len(embeddings2) else (np.array(embeddings2),np.array(embeddings1))
    similarities = [max(arr_big,key=lambda big_embed: 1 - spatial.distance.cosine(big_embed, small_embed)) for small_embed in arr_small]

def total_similarity(timestamp,embedding,embeddings,embeddings_times,sf_norm=0.1,sf_dropoff=0.1):
    #use kernel of size a day
    #convolve with points
    #scale with exponential
    #
        #k + k*s(-x)
    zipped_and_sorted = sorted(zip(embeddings,embeddings_times), key=lambda x: x[1])
    results_similarity = [cosine_pair_embed_similarity(embedding,x[0]) for x in zipped_and_sorted]

    #time stuff
    left = filter(zipped_and_sorted, lambda x: x[1] < timestamp)
    right = zipped_and_sorted[len(left):]
    left_times = [x[1] for x in left]
    left_data = [x[0] for x in left]
    right_data = [x[0] for x in right]
    right_times = [x[1] for x in right]

    left_time_diffs = [timestamp-x[1] for x in reversed(left)]
    right_time_diffs = [x[1]-timestamp for x in right]

    inter_right_time_diffs = [b-a for (a,b) in zip(right_times.insert(0,timestamp),right_times.insert(0,timestamp)[1:])]
    inter_left_time_diffs = [b-a for (a,b) in zip(left_times.append(timestamp),left_times.append(timestamp)[1:])]
    max_diff = max(inter_left_time_diffs + inter_right_time_diffs)

#   scaling factor depending on density
    #sf_norm=0.1
    norm_scaling_left = [1-math.exp(sf*max_diff/x) for x in left_time_diffs]
    norm_scaling_right = [1-math.exp(sf*max_diff/x) for x in right_time_diffs]

#   scaling factor depending on distance from queried
    #sf_dropoff=0.1
    time_scaling_func = lambda x: math.exp(-sf_dropoff*x)
    scaled_similarities = [x*y for (x,y) in zip(left_data+right_data,norm_scaling_left+norm_scaling_right)]
    scaled_similarities = [x*time_scaling_func(y) for (x,y) in zip(scaled_similarities,left_time_diffs+right_time_diffs)]

    # TODO: return something
    # scaled similarities are the exponential curved and time density scaled values
    # results similarity is simply the max pairwise similarities between each document pair
def get_score(url):
    #check if present in db
        #return db value if true
    result = dat.Classification.retrieve(url)
    if(results is not None): return result.trust
    #else
    #
    # keywords = scrapeAnalyse(url, False, None)
    text,keywords,date = scrapeAnalyse(url, False, None)
    my_data = scrapeAnalyse(None, True, keywords)
    #mydata is a list of dictionaries
    #   each dictionary contains 3 fields:
    #   -text
    #   -date
    #   -url
    embed_batch=[]
    for dict in my_data:
        doc_embed = dat.document.retrieve(dict['url'])
        if (doc_embed is not None):
            dict['embed'] = doc_embed.vector
            dict['stored'] = True
        else:
            embed_batch.append(dict['text'])
            dict['stored'] = False
    embed_batch.append(text)

    embeddings = USE_embedding(embed_batch)
    for dict in my_data:
        if dict['embed'].get() is None:
            dict['embed'] = embeddings[0]
            embeddings.remove(0)


    for dict in my_data:
        if dict['stored'] is False:
            parsed_uri = urlparse(dict['url'])
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            dat.document.new(domain,dict['url'],dict['time'],dict['embed'])


    searched_embeddings = [x['embed'] for x in my_data]
    searched_timestamps = [x['date'] for x in my_data]
    trust = total_similarity(date,embeddings[0],searched_embeddings,searched_timestamps)

    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    dat.document.new(domain,url,date,embeddings[0])
    dat.Classification.new(domain,url,trust,date)
