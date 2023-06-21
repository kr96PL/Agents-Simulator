import numpy as np

def kmeans(data, k, max_iterations=100):
    # Inicjalizacja centroidów
    centroids = data[np.random.choice(range(len(data)), size=k, replace=False)]
    
    for _ in range(max_iterations):
        # Przypisanie punktów do najbliższych centroidów
        clusters = [[] for _ in range(k)]
        
        for point in data:
            distances = [np.linalg.norm(point - centroid) for centroid in centroids]
            cluster_index = np.argmin(distances)
            clusters[cluster_index].append(point)
        
        # Aktualizacja centroidów
        new_centroids = []
        
        for cluster in clusters:
            new_centroids.append(np.mean(cluster, axis=0))
        
        # Sprawdzenie warunku zakończenia
        if np.all(centroids == new_centroids):
            break
        
        centroids = new_centroids
    
    return centroids, clusters