import numpy as np
import scipy.stats as stats
def generate(n, d, delta, true_outliers=None):
    """Generate synthetic data"""
    M = np.zeros((n, d))
    U = np.identity(n)
    V = np.identity(d)
    if true_outliers is None:
        true_outlier_size = n//3
        true_outliers = np.random.choice(np.array(range(n)), size=true_outlier_size, replace=False)
    M[true_outliers] += delta
    X = M + stats.matrix_normal.rvs(mean=np.zeros((n, d)), rowcov=U, colcov=V)
    Sigma = np.kron(V,U)
    return X, Sigma, true_outliers