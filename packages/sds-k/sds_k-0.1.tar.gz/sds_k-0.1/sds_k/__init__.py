# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
import pandas as pd

os.environ['LOKY_MAX_CPU_COUNT'] = '4'  
iris = load_iris()
X = iris.data
y = iris.target
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)


plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS (Within-cluster sum of squares)')
plt.show()
optimal_k = 3  
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', max_iter=300, n_init=10, random_state=42)
y_kmeans = kmeans.fit_predict(X)
print(f"Optimal number of clusters (from Elbow Method): {optimal_k}")

plt.figure(figsize=(8, 6))
plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0, 1], s=100, c='red', label='Cluster 1')
plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1, 1], s=100, c='blue', label='Cluster 2')
plt.scatter(X[y_kmeans == 2, 0], X[y_kmeans == 2, 1], s=100, c='green', label='Cluster 3')

plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='yellow', label='Centroids')

plt.title('K-Means Clustering (Iris dataset)')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.legend()
plt.show()

sil_score = silhouette_score(X, y_kmeans)
print(f"Silhouette Score: {sil_score:.2f}")

centroids = pd.DataFrame(kmeans.cluster_centers_, columns=iris.feature_names)

print("\nCluster Centroids:")
print(centroids)

cluster_df = pd.DataFrame(X, columns=iris.feature_names)
cluster_df['Cluster'] = y_kmeans
cluster_means = cluster_df.groupby('Cluster').mean()


print("\nCluster-wise Feature Means:")
print(cluster_means)
