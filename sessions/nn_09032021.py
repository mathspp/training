from abc import ABC, abstractmethod
import numpy as np

def create_weight_matrix(nrows, ncols):
    return np.random.normal(loc=0, scale=1/(nrows*ncols), size=(nrows, ncols))

def create_bias_vector(length):
    return create_weight_matrix(length, 1)

class LossFunction(ABC):
    @abstractmethod
    def loss(self, values, target):
        pass

    @abstractmethod
    def dloss(self, values, target):
        pass

class MSELoss(LossFunction):
    def loss(self, values, target):
        return np.mean((values - target)**2)

    def dloss(self, values, target):
        return 2/values.size*(values - target)

class ActivationFunction(ABC):
    @abstractmethod
    def f(self, values):
        pass

    @abstractmethod
    def df(self, values):
        pass

class LeakyReLU(ActivationFunction):
    def __init__(self, alpha=0.1):
        self.alpha = alpha

    def f(self, x):
        return np.maximum(x, self.alpha*x)

    def df(self, x):
        return np.maximum(x > 0, self.alpha)

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
        out = self.act_function.f(self.b + np.dot(self.W, x))
        return out

class Network:
    """A chain of compatible layers."""
    def __init__(self, layers, loss, lr):
        self.layers = layers
        self.loss_function = loss
        self.lr = lr

        for l1, l2 in zip(layers[:-1], layers[1:]):
            if l1.outs != l2.ins:
                raise Exception("Layers should match.")

    def propagate(self, x):
        out = x
        for layer in self.layers:
            out = layer.propagate(out)
        return out

    def train(self, x, t):
        # Propagate x while accumulating intermediate steps
        xs = [x]
        for layer in self.layers:
            xs.append(layer.propagate(xs[-1]))

        dx = self.loss_function.dloss(xs.pop(), t)
        for layer, x in zip(self.layers[::-1], xs[::-1]):
            y = layer.b + np.dot(layer.W, x)
            db = layer.act_function.df(y) * dx
            dW = np.dot(db, x.T)
            dx = np.dot(layer.W.T, db)

            layer.b -= self.lr * db
            layer.W -= self.lr * dW

    def loss(self, values, target):
        return self.loss_function.loss(values, target)


if __name__ == "__main__":
    layers = [
        Layer(4, 2, LeakyReLU()),
        Layer(2, 5, LeakyReLU()),
        Layer(5, 1, LeakyReLU()),
    ]
    net = Network(layers, MSELoss(), 0.001)
    x = np.random.normal(size=(4, 1))
    target = np.zeros(shape=(1,1))

    out = net.propagate(x)
    print(net.loss(out, target))
    net.train(x, target)

    N = 100
    test_inputs = []
    for n in range(N):
        test_inputs.append(
            np.random.uniform(-1, 1, (4, 1))
        )

    loss = 0
    for test_input in test_inputs:
        out = net.propagate(test_input)
        loss += net.loss(out, target)
    print(loss)

    for _ in range(10_000):
        net.train(
            np.random.uniform(-1, 1, (4, 1)), target
        )

    loss = 0
    for test_input in test_inputs:
        out = net.propagate(test_input)
        loss += net.loss(out, target)
    print(loss)
