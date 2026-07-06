import re
import math
from typing import List, Dict, Tuple

# Simple list of English stopwords to filter out noisy terms
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',
    "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
    'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
    'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
    "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',
    "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
    "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
    "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
    "wouldn't"
}

def tokenize(text: str) -> List[str]:
    """Lowercase, strip non-alphanumeric characters, and split into words."""
    text = text.lower()
    # Replace non-alphanumeric characters with spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = text.split()
    return [w for w in words if w not in STOPWORDS]

class TFIDFRetriever:
    def __init__(self, corpus: List[Dict]):
        """
        Initialize retriever with a corpus of emails.
        Each document in corpus should have 'id', 'incoming_body', and 'historical_reply'.
        """
        self.corpus = corpus
        self.documents = [doc["incoming_body"] + " " + doc.get("subject", "") for doc in corpus]
        self.vocab = set()
        self.idf = {}
        self.doc_vectors = []
        
        self._build_index()

    def _build_index(self):
        """Construct the vocabulary, compute IDFs, and vectorize all documents."""
        N = len(self.documents)
        if N == 0:
            return

        # 1. Tokenize all docs and gather vocabulary
        tokenized_docs = [tokenize(doc) for doc in self.documents]
        for tokens in tokenized_docs:
            self.vocab.update(tokens)

        self.vocab = sorted(list(self.vocab))
        vocab_index = {word: idx for idx, word in enumerate(self.vocab)}

        # 2. Compute document frequency (DF) for each word
        df = {word: 0 for word in self.vocab}
        for tokens in tokenized_docs:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                if token in df:
                    df[token] += 1

        # 3. Compute inverse document frequency (IDF) using standard smooth formulation
        for word, count in df.items():
            self.idf[word] = math.log((N + 1) / (count + 1)) + 1.0

        # 4. Generate TF-IDF vectors for all documents
        for tokens in tokenized_docs:
            vector = self._vectorize_tokens(tokens, vocab_index)
            self.doc_vectors.append(vector)

    def _vectorize_tokens(self, tokens: List[str], vocab_index: Dict[str, int]) -> Dict[int, float]:
        """Convert a list of tokens to a sparse TF-IDF vector."""
        tf = {}
        for t in tokens:
            if t in vocab_index:
                tf[t] = tf.get(t, 0) + 1

        vector = {}
        for token, count in tf.items():
            idx = vocab_index[token]
            # TF score normalized by total words
            tf_score = count / max(1, len(tokens))
            vector[idx] = tf_score * self.idf[token]
        return vector

    def _cosine_similarity(self, vec1: Dict[int, float], vec2: Dict[int, float]) -> float:
        """Compute the cosine similarity between two sparse vectors."""
        if not vec1 or not vec2:
            return 0.0

        # Dot product
        dot_product = 0.0
        for idx, val in vec1.items():
            if idx in vec2:
                dot_product += val * vec2[idx]

        # Magnitudes
        mag1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        mag2 = math.sqrt(sum(val ** 2 for val in vec2.values()))

        if mag1 == 0.0 or mag2 == 0.0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def retrieve(self, query: str, k: int = 2) -> List[Tuple[Dict, float]]:
        """
        Given a query string, retrieve the top K most similar documents.
        Returns a list of tuples containing (document, similarity_score).
        """
        query_tokens = tokenize(query)
        vocab_index = {word: idx for idx, word in enumerate(self.vocab)}
        query_vector = self._vectorize_tokens(query_tokens, vocab_index)

        scores = []
        for doc, doc_vector in zip(self.corpus, self.doc_vectors):
            score = self._cosine_similarity(query_vector, doc_vector)
            scores.append((doc, score))

        # Sort by similarity score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]
