import numpy as np
import numpy as np
from . import DBSCAN
from . import util
from . import overconditioning


def run_parametric_dbscan(j, n, d, minpts, eps, a, c, z_min = -20, z_max = 20):
    zk = z_min
    list_zk = [zk]
    list_setofOutliers = []
    list_sign = []
    while zk < z_max:
        x_zk = a*zk + c
        X_zk = util.unvec(x_zk, n, d)
        setofOutliers, neps_zk = DBSCAN.DBSCAN_AD(eps, minpts).fit(X_zk)
        minusO_zk = [i for i in range(n) if i not in setofOutliers]
        list_setofOutliers.append(setofOutliers)
        intersection, S = overconditioning.compute_z_interval(j, n, d, eps, neps_zk, a, c, minusO_zk, x_zk)
        list_sign.append(S)
        for each_interval in intersection:
            if each_interval[0] <= zk <= each_interval[1]:
                next_zk = each_interval[1]
                break
        zk = next_zk + 0.0001        
        if zk < z_max:
            list_zk.append(zk)
        else:
            list_zk.append(z_max)
    return list_zk, list_setofOutliers, list_sign

def run_parametric(j, n, d, O, S_obs, minpts, eps, a, c):
    list_zk, list_setofOutliers, list_sign = run_parametric_dbscan(j, n, d, minpts, eps, a, c)
    z_interval = []
    for i in range(len(list_setofOutliers)):
        if np.array_equal(np.sort(list_setofOutliers[i]), np.sort(O)) and np.array_equal(list_sign[i], S_obs):
            z_interval.append([list_zk[i], list_zk[i + 1] - 0.0001])
        
    new_z_interval = []
    for each_interval in z_interval:
        if len(new_z_interval) == 0:
            new_z_interval.append(each_interval)
        else:
            sub = each_interval[0] - new_z_interval[-1][1]
            if abs(sub) <= 0.0001:
                new_z_interval[-1][1] = each_interval[1]
            else:
                new_z_interval.append(each_interval)
    return new_z_interval
