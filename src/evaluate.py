from sklearn.feature_extraction.text import CountVectorizer
from nltk import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm
import numpy as np


class Evaluate:
    def __init__(self):
        pass

    def content_based(self, summary, full_text):
        sentences = sent_tokenize(full_text)

        vectorizer = CountVectorizer().fit(sentences)
        full_text_vector = vectorizer.transform([full_text])
        summary_vector = vectorizer.transform([summary])

        score = cosine_similarity(full_text_vector, summary_vector)[0][0]

        return score

    def semantic_based(self, summary, full_text):
        try:
            summary_sentences = sent_tokenize(summary)
            full_text_sentences = sent_tokenize(full_text)

            vectorizer = CountVectorizer(ngram_range=(1, 3)).fit(full_text_sentences)
            smr_matrix = vectorizer.transform(summary_sentences).T.toarray()
            full_text_matrix = vectorizer.transform(full_text_sentences).T.toarray()
            U0, S0, VT0 = np.linalg.svd(full_text_matrix)
            U1, S1, VT1 = np.linalg.svd(smr_matrix)

            vectors0 = [(np.dot(S0, U0[0, :]), np.dot(S0, U0[i, :])) for i in range(len(U0))]
            vectors1 = [(np.dot(S1, U1[0, :]), np.dot(S1, U1[i, :])) for i in range(len(U1))]
            angles = [np.arccos(np.dot(a, b) / (norm(a, 2) * norm(b, 2))) for a in vectors0 for b in vectors1]

            return abs(1 - float(angles[1]) / float(pi / 2))
        except:
            print("Bug with semantic based evaluation")
            return 0.5

