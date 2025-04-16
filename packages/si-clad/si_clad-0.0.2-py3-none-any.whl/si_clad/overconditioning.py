import numpy as np
import numpy as np
from . import util


def compute_z_interval(j_test, n, d, eps, neps, a, c, minusO, x_zk):
    # Reshape a and c to (n, d) for easier indexing
    a_2d = a.reshape(n, d, order='F')
    c_2d = c.reshape(n, d, order='F')
    b = eps * eps
    trunc_interval = [(-np.inf, np.inf)]

    #compute Z_u
    for j in range(n):
        # Compute differences for all i
        diff_a = a_2d[j] - a_2d  # Shape: (n, d)
        diff_c = c_2d[j] - c_2d  # Shape: (n, d)
        
        neps_j = set(neps[j])
        
        for i in range(n):
            if i != j:
                p = np.sum(diff_a[i] ** 2)  # ||a_j - a_i||^2
                q = 2 * np.dot(diff_a[i], diff_c[i])  # 2*(a_j - a_i)^T (c_j - c_i)
                t = np.sum(diff_c[i] ** 2) - b  # ||c_j - c_i||^2 - b
                
                if i in neps_j:
                    # ||x_j - x_i||^2 <= b
                    res = util.solve_quadratic_inequality(p, q, t)
                else:
                    # ||x_j - x_i||^2 >= b
                    res = util.solve_quadratic_inequality(-p, -q, -t)
                
                if res != "No solution":
                    trunc_interval = util.interval_intersection(trunc_interval, res)
    #compute Z_v
    I_d = np.identity(d)
    eT_minusO = np.zeros((1, n))
    eT_minusO[:, minusO] = 1
    eT_mean_minusO = np.kron(I_d, eT_minusO) / len(minusO)
    
    e_j = np.zeros((1, n))
    e_j[:, j_test] = 1
    temp = np.kron(I_d, e_j) - eT_mean_minusO
    
    Xj_meanXminusO = temp @ x_zk
    S = np.sign(Xj_meanXminusO)
    B = np.multiply(S, temp)
    Ba = np.dot(B, a)
    Bc = np.dot(B, c)
    
    for j in range (Ba.shape[0]):
        res = util.solve_quadratic_inequality(0, -Ba[j][0], -Bc[j][0])
        trunc_interval = util.interval_intersection(trunc_interval,res)
    return trunc_interval, S