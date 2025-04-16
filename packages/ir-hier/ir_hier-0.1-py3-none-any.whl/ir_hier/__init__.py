#initiator
#6 clustering(hierarchical)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

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
X = vectorizer.fit_transform(documents).toarray()

# Compute linkage matrix using Ward's method
linked = linkage(X, method='ward')

# Plot dendrogram
plt.figure(figsize=(10, 6))
dendrogram(linked, orientation='top', labels=np.arange(len(documents)), distance_sort='descending', show_leaf_counts=True)
plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Document Index")
plt.ylabel("Distance")
plt.tight_layout()
plt.show()

# Assign clusters
num_clusters = 3
labels = fcluster(linked, num_clusters, criterion='maxclust')

# Print clusters
for i in range(1, num_clusters + 1):
    print(f"\nCluster {i}:")
    for j, doc in enumerate(documents):
        if labels[j] == i:
            print("-", doc)
