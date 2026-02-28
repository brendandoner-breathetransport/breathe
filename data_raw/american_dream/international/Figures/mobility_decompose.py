import numpy as np

def mobility_decompose(res):
    """
    Decomposes mobility data from a matrix.
    
    Args:
        res: A 2D array/matrix where:
             - res[:,1] contains mobility values (column index 1)
             - res[:,2] and res[:,3] contain additional decomposition data
    
    Returns:
        vec: A numpy array of length 3 with decomposed mobility values
    """
    vec = np.zeros(3)
    
    # First component: percentage change from first to last row in column 1
    vec[0] = 100 * res[0, 1] / res[0, 1] - 100 * res[-1, 1] / res[0, 1]
    
    # Temporary calculations for columns 2 and 3
    tmp1 = (100 * res[0, 2] / res[0, 2] - 100 * res[-1, 2] / res[0, 2])
    tmp2 = (100 * res[0, 3] / res[0, 3] - 100 * res[-1, 3] / res[0, 3])
    
    # Weighted decomposition based on tmp1 and tmp2
    vec[1] = tmp1 * vec[0] / (tmp1 + tmp2)
    vec[2] = tmp2 * vec[0] / (tmp1 + tmp2)
    
    return vec