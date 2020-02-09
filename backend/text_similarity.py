import tensorflow as tf
import tensorflow_hub as hub
import sklearn.metrics.pairwise as pw
import numpy as np
import nltk
import math
from newspaper import Article

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
    #else
    #
