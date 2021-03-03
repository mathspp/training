import numpy as np

def create_weight_matrix(nrows, ncols):
    return np.random.normal(loc=0, scale=1/(nrows*ncols), size=(nrows, ncols))

def create_bias_vector(length):
    return np.random.normal(loc=0, scale=1/length, size=(length, 1))

def leaky_relu(x, leaky_param=0.1):
    return np.maximum(x, x*leaky_param)


class Layer:
    def __init__(self, ins, outs, act_function):
        self.ins = ins
        self.outs = outs
        self.act_function = act_function

        self._W = create_weight_matrix(self.outs, self.ins)
        self._b = create_bias_vector(self.outs)
