"""
Experiment with a teacher-student model with the MNIST data.
"""

from nn import NeuralNetwork, Layer, LeakyReLU, Sigmoid, CrossEntropyLoss, MSELoss
from mnist import to_col, load_data, train, test

def train_student(student, teacher, train_data):
    """Train a student network to behave like the teacher network."""

    for i, train_row in enumerate(train_data):
        if not i%1000:
            print(i)

        x = to_col(train_row[1:])
        teacher_out = teacher.forward_pass(x)
        student.train(x, teacher_out)

if __name__ == "__main__":
    teacher_layers = [
        Layer(784, 16, LeakyReLU()),
        Layer(16, 16, LeakyReLU()),
        Layer(16, 10, LeakyReLU()),
    ]
    teacher_net = NeuralNetwork(teacher_layers, CrossEntropyLoss(), 0.001)
    
    train_data = load_data("mnistdata/mnist_train.csv", delimiter=",", dtype=int)
    train(teacher_net, train_data)

    test_data = load_data("mnistdata/mnist_test.csv", delimiter=",", dtype=int)
    accuracy = test(teacher_net, test_data)
    print(f"Accuracy of the teacher net is {100*accuracy:.2f}")

    student_layers = [
        Layer(784, 10, Sigmoid()),
    ]
    student_net = NeuralNetwork(student_layers, MSELoss(), 0.005)

    train_student(student_net, teacher_net, train_data)

    student_accuracy = test(student_net, test_data)
    print(f"Accuracy of the student net is {100*accuracy:.2f}")
