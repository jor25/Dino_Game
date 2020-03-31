# Using numpy to manually implement neural networks. Needed to remove tensorflow due to performance slowdowns on CPU.
# 3/29/20
# Resources
# Manual implementation of Neural network:
# https://github.com/TheAILearner/Training-Snake-Game-With-Genetic-Algorithm
import numpy as np

# Global Weight configurations
NUM_INPUTS = 10                         # Number of inputs
NUM_HID_1 = 20                          # Number of nodes in hidden layer 1
NUM_HID_2 = 20                          # Number of nodes in hidden layer 2
NUM_OUT = 4                             # Number of outputs
W1_SHAPE = (NUM_HID_1, NUM_INPUTS)      # Weight Matrix 1 = (20,10)
W2_SHAPE = (NUM_HID_2, NUM_HID_1)       # Weight Matrix 2 = (20,20)
W3_SHAPE = (NUM_OUT, NUM_HID_2)         # Weight Matrix 3 = (4,20)


def get_network_arch(individual):
    '''
    Function that takes in the weights of a specific individual and converts them to the correct model architecture.
    :param individual: The weights of a specific individual, 1d numpy array
    :return: Corrected Model architecture
    '''
    W1 = individual[0:W1_SHAPE[0] * W1_SHAPE[1]]
    W2 = individual[W1_SHAPE[0] * W1_SHAPE[1]:W2_SHAPE[0] * W2_SHAPE[1] + W1_SHAPE[0] * W1_SHAPE[1]]
    W3 = individual[W2_SHAPE[0] * W2_SHAPE[1] + W1_SHAPE[0] * W1_SHAPE[1]:]

    return W1.reshape(W1_SHAPE[0], W1_SHAPE[1]),\
           W2.reshape(W2_SHAPE[0], W2_SHAPE[1]),\
           W3.reshape(W3_SHAPE[0], W3_SHAPE[1])


def softmax(z):
    s = np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)
    return s


def sigmoid(z):
    s = 1 / (1 + np.exp(-z))
    return s


def relu(z):
    return np.maximum(0, z)


def sigmoid_backward(dA, Z):
    sig = sigmoid(Z)
    return dA * sig * (1 - sig)


def relu_backward(dA, Z):
    dZ = np.array(dA, copy = True)
    dZ[Z <= 0] = 0
    return dZ

# This is where I'll make predictions
def forward_propagation(State, ind_weight):
    '''
    Function used to make predictions given a state and the specific weight values.
    :param State: Numpy array of 0's and 1's
    :param ind_weight: Numpy array of weight values between -1 and 1
    :return:
    '''
    W1, W2, W3 = get_network_arch(ind_weight)

    Z1 = np.matmul(W1, State.T)
    A1 = np.tanh(Z1)
    Z2 = np.matmul(W2, A1)
    A2 = np.tanh(Z2)
    Z3 = np.matmul(W3, A2)
    A3 = softmax(Z3)
    return A3

def save_weights_as_json(weights, file_path):
    pass
