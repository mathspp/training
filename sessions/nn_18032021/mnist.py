#import csv
import numpy as np
from nn import NeuralNetwork, Layer, LeakyReLU, MSELoss

def load_data(path):
    with open(path, "r") as f:
        contents = f.read()
    # list comprehension
    rows = contents.split("\n")[:-1]
    data = [list(map(int, row.split(","))) for row in rows]
    return np.array(data)
    #return np.genfromtxt(path, delimiter=',')

def test(net, data):
    """Test the network on the rows of the data."""

    correct = 0
    for i, row in enumerate(data):
        if i % 1000 == 0:
            print(i)
        digit = row[0]
        x = row[1:].reshape((784, 1))
        out = net.forward_pass(x)
        if digit == np.argmax(out):
            correct += 1
    return correct/data.shape[0]

def train_student(teacher, student, data):
    """Traverse the data and teach the student to act like the teacher."""

    for i, row in enumerate(data):
        if i % 1000 == 0:
            print(i)
        digit = row[0]
        x = row[1:].reshape((784, 1))
        t = teacher.forward_pass(x)
        student.train(x, t)

def train(net, data):
    """Train the network on the rows of the data."""
    # Precompute the target column vectors.
    ts = {}
    for digit in range(10):
        t = np.zeros((10, 1))
        t[digit] = 1
        ts[digit] = t

    for i, row in enumerate(data):
        if i % 1000 == 0:
            print(i)
        digit = row[0]
        x = row[1:].reshape((784, 1))
        net.train(x, ts[digit])

if __name__ == "__main__":
    layers = [
        Layer(784, 16, LeakyReLU()),
        Layer(16, 16, LeakyReLU()),
        Layer(16, 10, LeakyReLU()),
    ]
    net = NeuralNetwork(layers, MSELoss(), 0.001)
    # CrossEntropyLoss ← um pouco mais chato
    # Sigmoid ← wikipedia

    print("Loading data...")
    train_data = load_data("mnistdata/mnist_train.csv")
    print("Done.")

    print("Training network...")
    train(net, train_data)
    print("Done.")

    print("Loading data...")
    test_data = load_data("mnistdata/mnist_test.csv")
    print("Done.")

    print("Testing network...")
    accuracy = test(net, test_data)
    print(round(100*accuracy, 2))

    student = NeuralNetwork(
        [Layer(784, 10, LeakyReLU())], MSELoss(), 0.005
    )

    print("Training the student...")
    train_student(net, student, train_data)
    print("Done.")

    accuracy = test(student, test_data)
    print(round(100*accuracy, 2))
