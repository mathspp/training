import numpy as np

def create_weight_matrix(nrows, ncols):
    return np.random.normal(0, 1/(nrows*ncols), (nrows, ncols))

def create_bias_vector(length):
    return create_weight_matrix(length, 1)

def leaky_relu(x, alpha=0.1):
    return np.maximum(alpha*x, x)

class Layer:
    def __init__(self, ins, outs, act_function):
        self.ins = ins
        self.outs = outs
        self.W = create_weight_matrix(outs, ins)
        self.b = create_bias_vector(outs)
        self.act_function = act_function

    def forward_pass(self, x):
        return self.act_function(np.dot(self.W, x) + self.b)

class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers

    def forward_pass(self, x):
        out = x
        for layer in self.layers:
            out = layer.forward_pass(out)
        return out


if __name__ == "__main__":
    layer1 = Layer(16, 10, leaky_relu)
    layer2 = Layer(10, 5, leaky_relu)
    layer3 = Layer(5, 15, leaky_relu)
    layer4 = Layer(15, 1, leaky_relu)
    layers = [layer1, layer2, layer3, layer4]
    net = NeuralNetwork(layers)

    inp = create_bias_vector(16)
    print(net.forward_pass(inp))
