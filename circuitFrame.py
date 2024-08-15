
from tkinter import *
from tkManagementFuncs import *

from dimensions import *


""" ===== ===== ===== DYNAMIC CANVAS ===== ===== ===== """

class DynamicCanvas(Canvas):

    def __init__(self, master, **kwargs):
        """
        Dynamic canvas for line animation (switch from line to square)

        :param master: tkinter master element
        :param kwargs: parameters to be passed on to tkinter Canvas widget
        """
        super().__init__(master=master, **kwargs)

        self.state = "line" # 'line' or 'rect'

        # Initialize canvas as a line
        self.makeLine()

    def reset(self):
        """ Reset canvas to line if not already """
        if self.state == "rect":
            self.empty()
            self.makeLine()

    def empty(self):
        """ Clear canvas """
        self.delete("all")

    def makeLine(self):
        """ Switch to line """
        self.create_line(0, 28, 65, 28, width=1)
        self.state = "line"

    def makeRect(self):
        """ Switch to square """
        self.empty()
        self.create_rectangle(5, 5, 55, 55, width=1, dash=(3, 1))
        self.state = "rect"


""" ===== ===== ===== QUBIT SUBFRAME ===== ===== ===== """


class qubit_subframe(Frame):

    def up(self):
        """ Up animation """
        self.configure(relief='raised')

    def down(self):
        """ Down animation """
        self.configure(relief='flat')
        self.reset_dynamic_gates()

    def __init__(self, **kwargs):
        """
        Dynamic frame for qubit/line handling within circuit_frame

        :param kwargs: parameters to be passed on to tkinter Canvas widget
        """
        super().__init__(**kwargs)

        # Pre-allocate space for all possible gate locations with dynamic canvas
        self.dynamic_content = [DynamicCanvas(self, width=gate_size, height=gate_size) for _ in range(circuit_gate_width)]

        for i, canva in enumerate(self.dynamic_content):
            canva.grid(sticky=N, column=i, row=0)

    def reset_dynamic_gates(self):
        """ Reset all dynamic canvas within this line """
        for gate in self.dynamic_content:
            if isinstance(gate, DynamicCanvas):
                gate.reset()

    def set_dynamic_gate(self, gate_number: None or int) -> None:
        """
        Resets all activated canvas and activates the specified gate canvas (animation)

        :param gate_number: gate location to animate
        """
        self.reset_dynamic_gates()

        # If given gate number is None, then we simply reset the canvas (mouse outside of frame)
        if gate_number is not None:
            c = self.dynamic_content[gate_number]

            if isinstance(c, DynamicCanvas):
                c.makeRect()

    def rm_gate(self, selected_gate: int) -> None:
        """
        Self remove function given to gate widgets once placed on qubit/line frame

        :param selected_gate: gate number to widget to destroy
        """
        # Destroy widget
        self.dynamic_content[selected_gate].destroy()
        # Replace widget
        self.dynamic_content[selected_gate] = DynamicCanvas(self, width=gate_size, height=gate_size)
        self.dynamic_content[selected_gate].grid(sticky=N, column=selected_gate, row=0)

    def add_gate(self, gate_number: int, gate_name: str) -> None:
        """
        Adds a gate widget to given location if empty (dynamic canvas)

        :param gate_number: gate number
        :param gate_name: gate name
        """

        # Creates gate widget
        wid_gate = Button(self, text=gate_name, width=4, height=2,
                          font=("Helvetica", 12, "bold"), bg="cornsilk3", cursor="pirate")
        wid_gate.bind("<ButtonPress-1>", lambda event: self.rm_gate(gate_number))
        bindButtonHover(wid_gate, cl_le="cornsilk3")

        # Reset animations
        self.reset_dynamic_gates()

        # Check for other gate at same location
        c = self.dynamic_content[gate_number]

        if isinstance(c, DynamicCanvas):
            c.destroy()

            self.dynamic_content[gate_number] = wid_gate
            wid_gate.grid(sticky=W, column=gate_number, row=0, padx=5, pady=0)


""" ===== ===== ===== CIRCUIT FRAME ===== ===== ===== """


class circuit_frame(Frame):


    def _init_size_(self, circuit_size: int) -> list:
        """
        Initialize the circuit subframe with the specified number of qubits

        :param circuit_size: size of circuit (in qubits/lines)
        :return: list of line frames (qubit_lines objects)
        """

        LINES = [] # QUBITS

        # Initialize all sub-frames (1 per qubit)
        for i in range(circuit_size):
            SUBFRAME = qubit_subframe(master=self,
                                  width=self.line_width,
                                  height=self.line_height,
                                  bd=bd,
                                  relief='flat')
            LINES.append(SUBFRAME)

        return LINES

    def __init__(self,
                 circuit_size: int,
                 relief = "ridge",
                 bd = bd,
                 **kwargs):
        """
        Circuit frame, composed of 'circuit_size' amount of qubits

        :param circuit_size: circuit size (qubits amount)
        :param relief: relief of frame
        :param bd: border width
        :param kwargs: parameters to be passed on to tkinter Frame widget
        """

        # Initialize size of frame
        self.line_width = cir_width - 2*bd
        self.line_height = cir_line_height

        width = self.line_width
        height = self.line_height * circuit_size

        super().__init__(relief=relief, bd=bd, width=width, height=height, **kwargs)

        # Initialize sub-frames (qubit lines)
        self.LINES = self._init_size_(circuit_size)

    def pack(self, **kwargs):
        """
        Packing function (packs all sub-frames as well)

        :param kwargs: parameters to be passed on to tkinter Frame.pack() method
        """

        # Pack sub-frames
        for i, line in enumerate(self.LINES):
            line.pack(side=TOP, fill=X, expand=True)
            # line.grid(sticky=W, column=0, row=i)

        # control line to avoid collapse of sub-frames on themselves once filled
        control_line1 = Frame(self, width=self.line_width)
        control_line1.pack(side=TOP, fill=X, expand=True)
        # control_line1.grid(sticky=N, column=0, row=len(self.LINES), columnspan=2)

        # control_line2 = Frame(self, height=self.line_height + 40)
        # control_line2.pack(side=LEFT, fill=Y, expand=True)
        # control_line2.grid(sticky=W, column=1, row=0, rowspan=len(self.LINES))

        # main frame packing
        super().pack(**kwargs)

    def minimize(self):
        """ Minimize all qubits/lines animations """
        for line in self.LINES:
            line.down()

    def highlight(self, line_n: int, gate_n: int) -> None:
        """
        Highlight animation for given line and gate

        :param line_n: line number
        :param gate_n: gate number
        """
        for i, line in enumerate(self.LINES):
            if i == line_n:
                line.up()
                line.set_dynamic_gate(gate_n)
            else:
                line.down()

    def add_gate(self, selected_line: int, selected_gate: int, gate_name: str):
        """
        Add gate widget to specified line and gate

        :param selected_line: line number
        :param selected_gate: gate number
        :param gate_name: gate name
        :return:
        """
        master = self.LINES[selected_line]
        master.add_gate(selected_gate, gate_name)

