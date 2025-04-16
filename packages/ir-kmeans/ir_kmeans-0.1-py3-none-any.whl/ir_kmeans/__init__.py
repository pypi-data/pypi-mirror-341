#initiator
#6 clustering(kmeans)
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Sample documents
documents = [
    "Machine learning is the study of computer algorithms that improve through experience.",
    "Deep learning is a subset of machine learning.",
    "Natural language processing is a field of artificial intelligence.",
    "Computer vision is a field of study that enables computers to interpret the visual world.",
    "Reinforcement learning is a machine learning algorithm.",
    "Information retrieval is the process of obtaining information from collection.",
    "Text mining is the process of deriving high-quality information from text.",
    "Data clustering is the task of dividing a set of objects into groups.",
    "Hierarchical clustering builds a tree of clusters.",
    "K-means clustering is a method of vector quantization."
]

# Convert documents into TF-IDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# Perform K-means clustering
k = 3  # Number of clusters
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(X)

# Evaluate clustering results
silhouette_avg = silhouette_score(X, kmeans.labels_)
print("Silhouette Score:", silhouette_avg)

# Print clusters
for i in range(k):
    cluster_docs_indices = np.where(kmeans.labels_ == i)[0]
    cluster_docs = [documents[idx] for idx in cluster_docs_indices]

    print(f"\nCluster {i+1}:")
    for doc in cluster_docs:
        print("-", doc)
