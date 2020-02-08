import tensorflow as tf
import tensorflow_hub as hub
mport sklearn.metrics.pairwise as pw

class embeddings:
    USE_mod_URL = "https://tfhub.dev/google/universal-sentence-encoder/2"
    def __init__(self):
        self.embed = hub.Module(module_url)

    def get_USE_embedding(self,_documents):
        #takes multiple documents (ie a list of strings)
        #
        if (isinstance(_documents, str)) documents = [_documents]
        else documents=_documents
        document_sentences = [document.strip().split('.') for document in documents

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


    def cosine_similarity():
