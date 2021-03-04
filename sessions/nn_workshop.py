import numpy as np

def create_weight_matrix(nrows, ncols):
    return np.random.normal(loc=0, scale=1/(nrows*ncols), size=(nrows, ncols))

def create_bias_vector(length):
    return create_weight_matrix(length, 1)

def leaky_relu(x, alpha=0.1):
    return np.maximum(x, alpha*x)

def mse_loss(values, target):
    """Mean Squared Error loss function."""
    return np.mean(
        (values - target)**2
    )

class Layer:
    """Object to model a layer of connections in a network."""

    def __init__(self, ins, outs, act_function):
        """Initialising a layer with `ins` inputs and `outs` outputs."""
        self.ins = ins
        self.outs = outs
        self.W = create_weight_matrix(outs, ins)
        self.b = create_bias_vector(outs)
        self.act_function = act_function

    def propagate(self, x):
        """Propagates the info from a set of neurons to the next set of neurons."""
        return self.act_function(self.b + np.dot(self.W, x))

class Network:
    """A chain of compatible layers."""
    def __init__(self, layers, loss):
        self.layers = layers
        self.loss_function = loss

        for l1, l2 in zip(layers[:-1], layers[1:]):
            if l1.outs != l2.ins:
                raise Exception("Layers should match.")

    def propagate(self, x):
        out = x
        for layer in self.layers:
            out = layer.propagate(out)
        return out

    def loss(self, values, target):
        return self.loss_function(values, target)


if __name__ == "__main__":
    layers = [
        Layer(4, 2, leaky_relu),
        Layer(2, 5, leaky_relu),
        Layer(5, 1, leaky_relu),
    ]
    net = Network(layers, mse_loss)
    x = np.random.normal(size=(4, 1))
    target = np.zeros(shape=(1,1))

    out = net.propagate(x)
    print(net.loss(out, target))
