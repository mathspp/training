import numpy as np

def createWeightMatrix(nrows, ncols):
    return np.zeros((nrows, ncols))

def createBiasVector(length):
    return np.zeros((length, 1))
