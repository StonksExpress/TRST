import tensorflow as tf
import tensorflow_hub as hub

class embeddings:
    USE_mod_URL = "https://tfhub.dev/google/universal-sentence-encoder/2"
    def __init__(self):
        self.embed = hub.Module(module_url)

    def get_USE_embedding(self,document):
        stripped = document.strip()
        sentences = stripped.split('.')
        similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
        similarity_message_encodings = embed(similarity_input_placeholder)
        with tf.Session() as session:
          session.run(tf.global_variables_initializer())
          session.run(tf.tables_initializer())
          sentence_embeddings = session.run(embed(messages))
          return sentence_embeddings

          
