import numpy as np
from . import util
from . import parametric

class InvalidOutlierSetError(Exception):
    pass

class InvalidOutlierIndexError(Exception):
    pass

def SI_CLAD(X, Sigma, minpts, eps, O, j = None):
    n = X.shape[0]
    d = X.shape[1]
    if not isinstance(X, np.ndarray) or X.ndim != 2:
        raise ValueError("X must be a 2D numpy array")

    if Sigma.shape != (n*d, n*d):
        raise ValueError(f"Sigma must have shape ({n*d}, {n*d})")

    if not (isinstance(minpts, int) and minpts > 0):
        raise ValueError("minpts must be a positive integer")

    if not (isinstance(eps, (int, float)) and eps > 0):
        raise ValueError("eps must be a positive number")

    if j is not None and not (0 <= j < n):
        raise InvalidOutlierIndexError(f"j = {j} is out of bounds for X with n = {n}")

    
    if len(O) == 0 or len(O) == n:
        raise InvalidOutlierSetError(
            f"No valid outliers detected: {len(O)} outliers found. "
            )

    if j is not None and j not in O:
        raise InvalidOutlierIndexError(
            f"Index j={j} is not an outlier. Valid outlier indices: {O}."
        )
    if j is None:
        j = np.random.choice(O)
    #contruct eta and sign
    minusO = [i for i in range(n) if i not in O]
    eT_minusO = np.zeros((1, n))
    eT_minusO[:,minusO] = 1
    x = util.vec(X)
    I_d = np.identity(d)
    eT_mean_minusO = np.kron(I_d, eT_minusO)/(n - len(O))
    e_j = np.zeros((1, n))
    e_j[:,j] = 1
    temp = np.kron(I_d, e_j) - eT_mean_minusO
    Xj_meanXminusO = np.dot(temp, x)
    S_obs = np.sign(Xj_meanXminusO) #sign
    etaT = np.dot(S_obs.T, temp)/d
    eta = np.transpose(etaT)
    etaTx = np.dot(etaT, x) #test statistic
    
    etaT_Sigma_eta=np.dot(np.dot(eta.T, Sigma), eta)
    #there is an slight difference in the notation here: X = az + c (instead of X = a + bz)
    a = np.dot(np.dot(Sigma, eta), np.linalg.inv(etaT_Sigma_eta))
    c = np.dot(np.identity(int(n*d)) - np.dot(a,eta.T), x)
    #compute truncated region Z
    truncated_region = parametric.run_parametric(j, n, d, O, S_obs, minpts, eps, a, c)
    cdf = util.pivot_with_specified_interval(truncated_region, eta, etaTx[0][0] , Sigma, 0)
    selective_p_value = 2 * min(cdf, 1 - cdf)
    return selective_p_value

