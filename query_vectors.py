import tensorflow as tf
import tensorflow_hub as hub
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math


def s2v(text, embed):
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        message_embeddings = session.run(embed(text))
    return message_embeddings


def ang_sim(sim):
    sim = (1 - np.arccos(sim) / math.pi)
    return sim


if __name__ == "__main__":
    sentences = ["could you tell me the most popular musician in America?", "who is the most popular musician in America?",
                 "when are the Lakers playing?", "Who does Lebron James play for?"]

    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
    # Import the Universal Sentence Encoder's TF Hub module
    model_USE = hub.Module(module_url)
    v = s2v(sentences, model_USE)
    s1 = v[0]
    s2 = v[1]
    s3 = v[2]
    s4 = v[3]
    print(v)
    print("Length of the sentence vectors is {}".format(len(s1)))
    print()

    dst_1_2 = distance.cosine(s1, s2)
    dst_1_3 = distance.cosine(s1, s3)
    dst_2_3 = distance.cosine(s2, s3)

    sim_1_2 = cosine_similarity([s1], [s2])
    sim_1_3 = cosine_similarity([s1], [s3])
    sim_2_3 = cosine_similarity([s2], [s3])
    sim_3_4 = cosine_similarity([s3], [s4])

    asim_1_2 = ang_sim(sim_1_2)
    asim_1_3 = ang_sim(sim_1_3)
    asim_2_3 = ang_sim(sim_2_3)
    asim_3_4 = ang_sim(sim_3_4)

    print("Distance between Sentence: \"{}\" and Sentence: \"{}\" = {}".format(sentences[0], sentences[1], dst_1_2))
    print("Distance between Sentence: \"{}\" and Sentence: \"{}\" = {}".format(sentences[0], sentences[2], dst_1_3))
    print()
    print("Cosine similarity between Sentence: \"{}\" and Sentence: \"{}\" = {}".format(sentences[0], sentences[1], sim_1_2))
    print("Cosine similarity between Sentence: \"{}\" and Sentence: \"{}\" = {}".format(sentences[0], sentences[2], sim_1_3))
    print("Cosine similarity between Sentence: \"{}\" and Sentence: \"{}\" = {}".format(sentences[2], sentences[3], sim_3_4))
    print()
    print("Angular distance between Sentence: \"{}\" and Sentence: \"{}\" = {}".format(sentences[0], sentences[1], asim_1_2))
    print("Angular distance between Sentence: \"{}\" and Sentence: \"{}\" = {}".format(sentences[0], sentences[2], asim_1_3))
    print("Angular distance between Sentence: \"{}\" and Sentence: \"{}\" = {}".format(sentences[2], sentences[3], asim_3_4))

