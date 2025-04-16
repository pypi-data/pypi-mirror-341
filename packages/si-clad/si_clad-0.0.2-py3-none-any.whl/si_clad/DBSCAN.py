import numpy as np


class DBSCAN_AD:
    """DBSCAN-based anomaly detection with Euclidean distance"""
    def __init__(self, eps, min_pts):
        """
        Initialize the DBSCAN instance with epsilon (neighborhood radius)
        and minimum number of points required to form a core point.
        """
        self.eps = eps
        self.min_pts = min_pts

    def euclidean_distance(self, point1, point2):
        """
        Compute the Euclidean distance between two points.
        """
        return np.linalg.norm(point1 - point2)

    def compute_neighborhoods(self):
        """
        Compute the neighborhood for each point in the dataset and mark 
        core points based on the eps and min_pts parameters.
        """
        self.neighborhoods = []  
        self.core_points = []    

        for point in self.X:
            distances = [self.euclidean_distance(point, other) for other in self.X]
            neighbors = [idx for idx, d in enumerate(distances) if d <= self.eps]
            self.neighborhoods.append(neighbors)
            self.core_points.append(len(neighbors) >= self.min_pts)

        return self.neighborhoods, self.core_points

    def expand_cluster(self, point_index, cluster_id, clusters):
        """
        Expand a cluster starting from a core point. New neighbors are added to
        the cluster if they are reachable from the current core points.
        """
        stack = [point_index]
        clusters[point_index] = cluster_id

        while stack:
            current_index = stack.pop()
            if self.core_points[current_index]:
                for neighbor in self.neighborhoods[current_index]:
                    if clusters[neighbor] == -1:  # If point is unassigned (noise)
                        clusters[neighbor] = cluster_id
                        stack.append(neighbor)
        return clusters

    def fit(self, X):
        """
        Fit the DBSCAN model on the dataset X and return the cluster labels
        along with the computed neighborhoods.
        """
        self.X = X
        n_points = X.shape[0]
        clusters = [-1] * n_points

        self.compute_neighborhoods()

        cluster_id = 0
        for point_index in range(n_points):
            if clusters[point_index] != -1 or not self.core_points[point_index]:
                continue
            clusters = self.expand_cluster(point_index, cluster_id, clusters)
            cluster_id += 1
        outliers_set = [i for i in range(n_points) if clusters[i] == -1]
        return outliers_set, self.neighborhoods
