import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd
import os
os.environ['LOKY_MAX_CPU_COUNT'] = '4'  
iris = load_iris()
X = iris.data
y = iris.target
wcss = []  
sil_scores = []  
for i in range(2, 11): 
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(X)
    sil_score = silhouette_score(X, kmeans.labels_)
    sil_scores.append(sil_score)
    wcss.append(kmeans.inertia_)
plt.figure(figsize=(8, 6))
plt.plot(range(2, 11), sil_scores, marker='o', color='b')
plt.title('Silhouette Scores for Different Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()
optimal_k = sil_scores.index(max(sil_scores)) + 2  
print(f"Optimal number of clusters (from Silhouette Analysis): {optimal_k}")
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', max_iter=300, n_init=10, random_state=42)
y_kmeans = kmeans.fit_predict(X)
plt.figure(figsize=(8, 6))
for i in range(optimal_k):
    plt.scatter(X[y_kmeans == i, 0], X[y_kmeans == i, 1], s=100, label=f'Cluster {i+1}')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='yellow', label='Centroids', marker='X')
plt.title('K-Means Clustering (Iris dataset)')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.legend()
plt.show()
centroids = pd.DataFrame(kmeans.cluster_centers_, columns=iris.feature_names)
print("\nCluster Centroids:")
print(centroids)
cluster_df = pd.DataFrame(X, columns=iris.feature_names)
cluster_df['Cluster'] = y_kmeans
cluster_means = cluster_df.groupby('Cluster').mean()
print("\nCluster-wise Feature Means:")
print(cluster_means)
sil_score = silhouette_score(X, y_kmeans)
print(f"\nSilhouette Score for the optimal clustering: {sil_score:.2f}")
