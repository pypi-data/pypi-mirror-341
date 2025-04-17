def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

documents = [
    "This is the first document.",
    "This document is the second document.",
    "And this is the third one.",
    "Is this the first document?",
    "This is the last document."
]

last_document = documents[-1]
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

k = 2

if tfidf_matrix.shape[0] >= k:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)

    clusters = kmeans.fit_predict(tfidf_matrix)
    silhouette_score_value = silhouette_score(tfidf_matrix, clusters)
    print("Silhouette Score:", silhouette_score_value)
else:
    print("Error: Number of clusters exceeds the number of documents.")

    '''
    print(code)