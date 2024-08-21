
import numpy as np

from gates import _0, _1, _I
from gates import kron


class circuit(object):

    def __init__(self, circuit_size):
        self.size = circuit_size

        self.gates = []
        self.initial_state = np.zeros(circuit_size * 2)
        self.measurement_state = None

    """ ##### ##### ##### ##### ##### ##### """
    def set_initial_state(self, initial_state):
        self.initial_state = initial_state

    def _set_measurement_state(self, measurement_state):
        self.measurement_state = measurement_state

    def add_gate(self, gate, index: int or list or tuple) -> None:
        """
        Add a gate to the circuit.

        :param gate: gate object to be added
        :param index: index of the circuit line (from top to bottom)
        :return: None
        """

        if type(index) is int:
            # Simple gate case
            # Tensor product between all circuit lines with either identity matrix or with gate matrix

            # The gate matrix
            result = gate.get_mat()

            for i in range(self.size):
                # If qubit is before gate (from top to bottom)
                if i < index:
                    result = np.kron(_I.get_mat(), result)
                # If qubit is after gate (from top to bottom)
                elif i > index:
                    result = np.kron(result, _I.get_mat())

        elif type(index) in [list, tuple]:
            # Complex/controlled gate case

            # "activator" (usually but can be inverted)
            first_gates = gate.activators
            # "gate matrix"
            last_gates = [_I.get_mat(), gate.get_mat()]

            # If activator after actor, then invert the two matrix
            if index[0] > index[1]:
                first_gates, last_gates = last_gates, first_gates
                index = (index[1], index[0])

            result = np.zeros((2 ** self.size) ** 2, dtype=np.complex128).reshape(2 ** self.size, 2 ** self.size)

            for j in range(2):

                tensorProduct = first_gates[j]

                for i in range(self.size):
                    # If qubit is before gate (from top to bottom)
                    if i < index[0]:
                        tensorProduct = np.kron(_I.get_mat(), tensorProduct)
                    elif i == index[1]:
                        tensorProduct = np.kron(tensorProduct, last_gates[j])
                    # If qubit is after gate (from top to bottom)
                    elif i > index[0]:
                        tensorProduct = np.kron(tensorProduct, _I.get_mat())
                    elif i > index[1]:
                        tensorProduct = np.kron(tensorProduct, _I.get_mat())

                result += tensorProduct

        else:
            raise TypeError("Index must be an int, list or tuple")

        # Add final tensor product to dot product step
        self.gates.append(result)

    def get_state(self):

        result = self.measurement_state

        for gate in np.array(self.gates)[::-1]:
            result = np.dot(result, gate)

        result = np.dot(result, self.initial_state)
        return result

    def get_probabilities(self, measurement_states, percentage=False):
        """Make measurement of all possible state of the circuit and return probabilities of possible states"""

        # Careful you are approaching ugly code, please do not interact with it too much, or you will scare it away

        m_states = []

        # Convert from str to real gates
        for state in measurement_states:
            s = []
            for char in state:
                if char == "0":
                    s.append(_0)
                elif char == "1":
                    s.append(_1)
            m_states.append(s)

        # Make measurement for each measurement state
        probabilities = [self.make_measurement(kron(*state)) for state in m_states]

        if percentage:
            probabilities = [prob * 100 for prob in probabilities]

        return probabilities

    def make_measurement(self, measurement_state):
        """ Retrieve probability for a given measurement state """
        self._set_measurement_state(measurement_state)
        result = self.get_state()
        return np.abs(result) ** 2
