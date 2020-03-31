# Using numpy to manually implement neural networks. Needed to remove tensorflow due to performance slowdowns on CPU.
# 3/29/20
# Resources
# Manual implementation of Neural network:
# https://github.com/TheAILearner/Training-Snake-Game-With-Genetic-Algorithm

from configs import *
from os import listdir
from os.path import isfile, join

def get_network_arch(individual):
    '''
    Function that takes in the weights of a specific individual and converts them to the correct model architecture.
    :param individual: The weights of a specific individual, 1d numpy array
    :return: Corrected Model architecture
    '''
    # Weight Matrix 1, the flattened first section of the weights list
    w_matrix_1 = individual[0:W1_SHAPE[0] * W1_SHAPE[1]]
    # Weight Matrix 2, the flattened second section of the weights list
    w_matrix_2 = individual[W1_SHAPE[0] * W1_SHAPE[1]:W2_SHAPE[0] * W2_SHAPE[1] + W1_SHAPE[0] * W1_SHAPE[1]]
    # Weight Matrix 3, the flattened third section of the weights list
    w_matrix_3 = individual[W2_SHAPE[0] * W2_SHAPE[1] + W1_SHAPE[0] * W1_SHAPE[1]:]

    return w_matrix_1.reshape(W1_SHAPE[0], W1_SHAPE[1]),\
           w_matrix_2.reshape(W2_SHAPE[0], W2_SHAPE[1]),\
           w_matrix_3.reshape(W3_SHAPE[0], W3_SHAPE[1])


def softmax(z):
    # Softmax activation layer
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
    w_matrix_1, w_matrix_2, w_matrix_3 = get_network_arch(ind_weight)

    Z1 = np.matmul(w_matrix_1, State.T)
    A1 = np.tanh(Z1)
    Z2 = np.matmul(w_matrix_2, A1)
    A2 = np.tanh(Z2)
    Z3 = np.matmul(w_matrix_3, A2)
    A3 = softmax(Z3)
    return A3


def save_weights_as_csv(weights, file_name, file_path="weight_files/numpy_weight_files"):
    '''
    Save the weights of any given model from the dino brains to a csv file.
    :param weights: Dino brain weights
    :param file_name: Description of dino weights
    :param file_path: Path to saving directory
    :return:
    '''
    print("Saving File: {}/{}.csv".format(file_path, file_name))
    np.savetxt("{}/{}.csv".format(file_path, file_name), weights, delimiter=",")


def load_saved_weight_csv(file_name, file_path="weight_files/numpy_weight_files"):
    '''
    Load the weights of any given csv file from a file directory and return the weights to a potential brain.
    :param file_name: Name of the file with the .csv extension
    :param file_path: Path to the file
    :return: numpy array of weights
    '''
    # Numpy read in the weight files - separate by comma
    weights = np.loadtxt("{}/{}".format(file_path, file_name), delimiter=",")
    print("Loaded File: {}/{}".format(file_path, file_name))
    return weights


def load_all_networks(file_path='weight_files/numpy_weight_files'):
    '''
    Function that takes a file path and looks for all the files in there to initialize previous generation dinos.
    Updates the global brain argument directly.
    :param file_path: string path to file
    :return: N/A
    '''
    all_weights = [f for f in listdir(file_path) if isfile(join(file_path, f))]     # Get all csv weight files

    for id, weight in enumerate(all_weights):
        DINO_BRAINS[id] = load_saved_weight_csv(weight)                # Use all the previous saved dinos
