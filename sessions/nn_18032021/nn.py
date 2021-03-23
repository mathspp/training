from abc import ABC, abstractmethod
import numpy as np

def create_weight_matrix(nrows, ncols):
    return np.random.normal(0, 1/(nrows*ncols), (nrows, ncols))

def create_bias_vector(length):
    return create_weight_matrix(length, 1)

class ActivationFunction(ABC):
    @abstractmethod     # decorator
    def f(self, x):
        pass

    @abstractmethod
    def df(self, x):
        pass

class LeakyReLU(ActivationFunction):
    def __init__(self, alpha=0.1):
        self.alpha = alpha

    def f(self, x):
        return np.maximum(self.alpha*x, x)

    def df(self, x):
        return np.maximum(self.alpha, x > 0)

class LossFunction(ABC):
    @abstractmethod
    def loss(self, out, target):
        pass

    @abstractmethod
    def dloss(self, out, target):
        pass

class MSELoss(LossFunction):
    def loss(self, out, target):
        return np.mean((out - target)**2)

    def dloss(self, out, target):
        return 2*(out - target)/out.size

class Layer:
    def __init__(self, ins, outs, act_function):
        self.ins = ins
        self.outs = outs
        self.W = create_weight_matrix(outs, ins)
        self.b = create_bias_vector(outs)
        self.act_function = act_function

    def forward_pass(self, x):
        return self.act_function.f(np.dot(self.W, x) + self.b)

class NeuralNetwork:
    def __init__(self, layers, loss_function, lr):
        self.layers = layers
        self.loss_function = loss_function
        self.lr = lr

    def forward_pass(self, x):
        out = x
        for layer in self.layers:
            out = layer.forward_pass(out)
        return out

    def train(self, x, target):
        """Use backpropagation to train the neural network."""

        xs = [x]
        for layer in self.layers:
            xs.append(layer.forward_pass(xs[-1]))

        dx = self.loss_function.dloss(xs.pop(), target)
        for layer, x in zip(self.layers[::-1], xs[::-1]):
            y = np.dot(layer.W, x) + layer.b
            db = layer.act_function.df(y) * dx
            dW = np.dot(db, x.T)
            dx = np.dot(layer.W.T, db)
            # Update parameters
            layer.W -= self.lr*dW
            layer.b -= self.lr*db


if __name__ == "__main__":
    layers = [
        Layer(3, 4, LeakyReLU()),
        Layer(4, 4, LeakyReLU()),
        Layer(4, 2, LeakyReLU()),
    ]
    net = NeuralNetwork(layers, MSELoss(), 0.001)

    z = np.ones((2, 1))

    loss = 0
    xs = []
    for _ in range(100):
        x = np.random.normal(size=(3, 1))
        out = net.forward_pass(x)
        loss += net.loss_function.loss(out, z)
        xs.append(x)
    print(loss)

    for _ in range(10000):
        x = np.random.normal(size=(3, 1))
        net.train(x, z)

    loss = 0
    for x in xs:
        out = net.forward_pass(x)
        loss += net.loss_function.loss(out, z)
    print(loss)
