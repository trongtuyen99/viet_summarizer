import numpy as np
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class Vectorizer:
    """
        vectorize list of sentence
        using: bow, tfidf, w2v
        return row vector
    """

    def __init__(self, w2v_path=r".\data\vi.vec"):

        self.count_vectorizer = CountVectorizer(ngram_range=(1, 3))
        self.tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        self.w2v = KeyedVectors.load_word2vec_format(w2v_path)

    def vectorize(self, sentences, mode="w2v"):

        if mode == "count":
            return self.count_vectorizer.fit_transform(sentences).toarray()
        elif mode == "tfidf":
            return self.tfidf_vectorizer.fit_transform(sentences).toarray()
        else:  # default
            X = []
            for sentence in sentences:
                words = sentence.split(" ")
                sentence_vec = np.zeros(100)
                for word in words:
                    if word in self.w2v.vocab:
                        sentence_vec += self.w2v[word]
                X.append(sentence_vec)

            return np.array(X)


if __name__ == '__main__':
    with open('data/vi.vec', 'rb') as reader:
        print(reader.read()[:10])
