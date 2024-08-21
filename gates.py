
import numpy as np

""" ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### """

def kron(*mat):
    """Kronecker product of N number of matrices"""

    if type(mat[0]) == Gate:
        product = mat[0].get_mat()
    else:
        product = mat[0]

    for i in range(1, len(mat)):
        if type(mat[i]) == Gate:
            product = np.kron(product, mat[i].get_mat())
        else:
            product = np.kron(product, mat[i])

    return product


""" ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### """


class Gate(object):

    def __init__(self, mat: np.ndarray, activators=None, name=None):
        self.mat = mat
        self.activators = activators

        self.name = name

    def get_mat(self):
        return self.mat.copy()


""" ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### """

# 0 and 1 bits
_0 = Gate(np.array([1, 0]), name="0")
_1 = Gate(np.array([0, 1]), name="1")

# Identity matrix
_I = Gate(np.array([[1, 0],
                    [0, 1]]))

# Pauli matrices
_X = Gate(np.array([[0, 1],
                    [1, 0]]))
_Y = Gate(np.array([[0, -1j],
                    [1j, 0]]))
_Z = Gate(np.array([[1, 0],
                    [0, -1]]))

# phase gate
_S = Gate(np.array([[1, 0],
                    [0, 1j]]))
# square root of X
_sqrt = Gate(1/2 * np.array([[1+1j, 1-1j],
                             [1-1j, 1+1j]]))
# Hadamard
_H = Gate(1/np.sqrt(2) * np.array([[1, 1],
                                   [1, -1]]))

# CNOT / controlled-X gate
_CX = Gate(np.array([[0, 1],   # X gate
                     [1, 0]]),
           np.array([[[1, 0],  # |0> <0| activator
                      [0, 0]],
                     [[0, 0],  # |1> <1| activator
                      [0, 1]]]))
# controlled-Y
_CY = Gate(np.array([[0, -1j], # Y gate
                    [1j, 0]]),
           np.array([[[1, 0],  # |0> <0| activator
                      [0, 0]],
                     [[0, 0],  # |1> <1| activator
                      [0, 1]]]))
# controlled-Z
_CZ = Gate(np.array([[1, 0],   # Z gate
                    [0, -1]]),
           np.array([[[1, 0],  # |0> <0| activator
                      [0, 0]],
                     [[0, 0],  # |1> <1| activator
                      [0, 1]]]))
# controlled-H
_CH = Gate(1/np.sqrt(2) * np.array([[1, 1],  # H gate
                                   [1, -1]]),
           np.array([[[1, 0],  # |0> <0| activator
                      [0, 0]],
                     [[0, 0],  # |1> <1| activator
                      [0, 1]]]))
# controlled-S
_CS = Gate(np.array([[1, 0],   # S gate
                    [0, 1j]]),
           np.array([[[1, 0],  # |0> <0| activator
                      [0, 0]],
                     [[0, 0],  # |1> <1| activator
                      [0, 1]]]))

gates = {
    "0": _0,
    "1": _1,

    "I": _I,

    "X": _X,
    "Y": _Y,
    "Z": _Z,

    "S": _S,
    "H": _H,

    "CX": _CX,
    "CY": _CY,
    "CZ": _CZ,
    "CH": _CH,
    "CS": _CS,

    "sqrt": _sqrt,
}
