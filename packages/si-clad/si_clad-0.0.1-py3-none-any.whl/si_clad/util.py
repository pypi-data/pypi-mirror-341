import numpy as np
from mpmath import mp

mp.dps = 500
def pivot_with_specified_interval(z_interval, etaj, etajTy, cov, tn_mu):
    tn_sigma = np.sqrt(np.dot(np.dot(etaj.T, cov), etaj))[0][0]

    numerator = 0
    denominator = 0

    for each_interval in z_interval:
        al = each_interval[0]
        ar = each_interval[1]

        #print(al, etajTy, ar
        denominator = denominator + mp.ncdf((ar - tn_mu)/tn_sigma) - mp.ncdf((al - tn_mu)/tn_sigma)

        if etajTy >= ar:
            numerator = numerator + mp.ncdf((ar - tn_mu)/tn_sigma) - mp.ncdf((al - tn_mu)/tn_sigma)
        elif (etajTy >= al) and (etajTy < ar):
            numerator = numerator + mp.ncdf((etajTy - tn_mu)/tn_sigma) - mp.ncdf((al - tn_mu)/tn_sigma)
    if denominator != 0:
        return float(numerator/denominator)
    else:
        return None

def vec(A):
  vec = A.reshape(-1, order='F')
  return vec.reshape(-1,1)

def unvec(vecA, n, d):
  return vecA.reshape(n, d, order='F')

def solve_quadratic_inequality(a, b, c,seed = 0):
    """ ax^2 + bx +c <= 0 """
    if abs(a) < 1e-8:
        a = 0
    if abs(b) < 1e-8:
        b = 0
    if abs(c) < 1e-8:
        c = 0
    if a == 0:
        # print(f"b: {b}")
        if b > 0:
            # return [(-np.inf, -c / b)]
            return [(-np.inf, np.around(-c / b, 8))]
        elif b == 0:
            # print(f"c: {c}")
            if c <= 0:
                return [(-np.inf, np.inf)]
            else:
                print('Error bx + c', seed)
                return 
        else:
            return [(np.around(-c / b, 8), np.inf)]
    delta = b*b - 4*a*c
    if delta < 0:
        if a < 0:
            return [(-np.inf, np.inf)]
        else:
            print("Error to find interval. ")
    # print("delta:", delta)
    # print(f"2a: {2*a}")
    x1 = (- b - np.sqrt(delta)) / (2*a)
    x2 = (- b + np.sqrt(delta)) / (2*a)
    # if x1 > x2:
    #     x1, x2 = x2, x1  
    x1 = np.around(x1, 8)
    x2 = np.around(x2, 8)
    if a < 0:
        return [(-np.inf, x2),(x1, np.inf)]
    return [(x1,x2)]


def interval_intersection(a, b):
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        a_start, a_end = a[i]
        b_start, b_end = b[j]
        
        # Calculate the potential intersection
        start = max(a_start, b_start)
        end = min(a_end, b_end)
        
        # If the interval is valid, add to results
        if start < end:
            result.append((start, end))
        
        # Move the pointer which ends first
        if a_end < b_end:
            i += 1
        else:
            j += 1
    return result
def interval_union(a, b):
    # Merge the two sorted interval lists into one sorted list
    merged = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i][0] < b[j][0]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    # Add any remaining intervals from a or b
    merged.extend(a[i:])
    merged.extend(b[j:])
    
    # Merge overlapping intervals
    if not merged:
        return []
    
    result = [merged[0]]
    for current in merged[1:]:
        last = result[-1]
        if current[0] < last[1]:
            # Overlapping or adjacent, merge them
            new_start = last[0]
            new_end = max(last[1], current[1])
            result[-1] = (new_start, new_end)
        else:
            result.append(current)
    return result
def compute_estimated_covariance(X, minusO):
    covX = np.cov(X[minusO,:], rowvar=False)  
    # Construct Cov(vec(X)) using Kronecker product
    Sigma = np.kron(np.eye(X.shape[0]), covX)
    return Sigma