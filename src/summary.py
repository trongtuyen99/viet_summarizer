import networkx as nx
import numpy as np
from nltk import sent_tokenize
from preprocess import Preprocessor
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.metrics.pairwise import cosine_similarity
from vectorize import Vectorizer


class Summarizer():
    def __init__(self, w2v_path=r".\data\vi.vec"):
        self.clearner = Preprocessor()
        self.vectorizer = Vectorizer(w2v_path)

    def summarize(self, paragraph, mode="clustering", keep_sentences=5):
        origin_sentence = sent_tokenize(paragraph)
        sentences = self.clearner.preprocessing(paragraph)
        sent_vectors = self.vectorizer.vectorize(sentences)  # row vector

        if mode == "clustering":
            kmeans = KMeans(n_clusters=keep_sentences)
            kmeans = kmeans.fit(sent_vectors)
            avg = []
            for j in range(keep_sentences):
                idx = np.where(kmeans.labels_ == j)[0]
                avg.append(np.mean(idx))
            closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, sent_vectors)
            # top_sentences = sorted(range(n_clusters), key=lambda k: avg[k])
            top_sentences = sorted(closest)

        elif mode == "lsa":
            # input: column vector
            sent_vectors_t = sent_vectors.T
            U, S, VT = np.linalg.svd(sent_vectors_t)
            saliency_vec = np.dot(np.square(S), np.square(VT))
            top_sentences = saliency_vec.argsort()[-keep_sentences:][::-1]
            top_sentences.sort()

        else:
            sim_mat = np.zeros([len(sentences), len(sentences)])
            for i in range(len(sentences)):
                for j in range(len(sentences)):
                    if i != j:
                        sim_mat[i][j] = cosine_similarity(sent_vectors[i].reshape(1, -1),
                                                          sent_vectors[j].reshape(1, -1))[0][0]

            nx_graph = nx.from_numpy_array(sim_mat)
            scores = list(nx.pagerank(nx_graph).values())
            top_sentences = np.argsort(scores)[-keep_sentences:][::-1]
            top_sentences.sort()
        summary = " ".join([origin_sentence[i] for i in top_sentences])
        return summary, top_sentences
