
from tkinter import *
from tkManagementFuncs import *

from dimensions import *


""" ===== ===== ===== DYNAMIC CANVAS ===== ===== ===== """


class DynamicButton(Button):

    def __init__(self, master, gate, command, bg, **kwargs):

        self.gate = gate
        self.color = bg

        super().__init__(master=master, text=gate,
                         width=4, height=2,
                         bg=bg, **kwargs)

        self.bind("<ButtonPress-1>", command)
        bindButtonHover(self, cl_leave=bg)


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
        self.create_line(0, gate_height/2, gate_width, gate_height/2, width=1)
        self.state = "line"

    def makeRect(self):
        """ Switch to square """
        self.empty()
        self.create_rectangle(0+2, 0+2, gate_width-2, gate_height-2, width=1, dash=(3, 1))
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
        self.dynamic_content = [DynamicCanvas(self, width=gate_width, height=gate_height, bd=0) for _ in range(gate_n_per_line)]

        for i, canva in enumerate(self.dynamic_content):
            canva.place(x=-2 + gate_width * i, y=-2)

    def __getitem__(self, item):
        return self.dynamic_content[item]

    def __str__(self):
        return str([type(elt) for elt in self.dynamic_content])

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

    def rm_gate(self, gate_n: int) -> None:
        """
        Self remove function given to gate widgets once placed on qubit/line frame

        :param gate_n: gate number to widget to destroy
        """
        # Destroy widget
        self.dynamic_content[gate_n].destroy()

        # Replace widget
        self.dynamic_content[gate_n] = DynamicCanvas(self, width=gate_width, height=gate_height, bd=0)
        self.dynamic_content[gate_n].place(x=-2 + gate_width * gate_n, y=-2)

    def can_add_gate(self, gate_n: int) -> bool:
        """
        Check if given location is free for gate placement

        :param gate_n: gate location

        :return: Boolean, can the gate be placed at given location?
        """
        if isinstance(self.dynamic_content[gate_n], DynamicCanvas):
            return True

    def place_gate(self, gate_n: int, wid_gate) -> None:
        """
        Adds a gate widget to given empty location (DynamicCanvas).
        Cannot overwrite an existing gate widget.

        :param gate_n: gate number
        :param kwargs: parameters to be passed on DynamicButton widget
        """

        # Reset animations
        self.reset_dynamic_gates()

        # Check for other gate at same location
        c = self.dynamic_content[gate_n]

        if isinstance(c, DynamicCanvas):
            c.destroy()
            del self.dynamic_content[gate_n]

            self.dynamic_content.insert(gate_n, wid_gate)
            wid_gate.place(x=-2 + gate_width * gate_n, y=-2)


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
                                      width=cir_line_width,
                                      height=cir_line_height,
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

        self.size = circuit_size

        super().__init__(relief=relief, bd=bd, width=cir_frame_width, height=cir_frame_height(circuit_size), **kwargs)

        # Initialize sub-frames (qubit lines)
        self.LINES = self._init_size_(circuit_size)

    def place(self, **kwargs):
        """
        Packing function (packs all sub-frames as well)

        :param kwargs: parameters to be passed on to tkinter Frame.pack() method
        """

        # Pack sub-frames
        for i, line in enumerate(self.LINES):
            line.place(x=0, y=cir_line_height * i)
            # line.pack(side=TOP, fill=X, expand=True)
            # line.grid(sticky=W, column=0, row=i)

        # control line to avoid collapse of sub-frames on themselves once filled
        # control_line1 = Frame(self, width=self.line_width)
        # control_line1.place(side=TOP, fill=X, expand=True)
        # control_line1.grid(sticky=N, column=0, row=len(self.LINES), columnspan=2)

        # control_line2 = Frame(self, height=self.line_height + 40)
        # control_line2.pack(side=LEFT, fill=Y, expand=True)
        # control_line2.grid(sticky=W, column=1, row=0, rowspan=len(self.LINES))

        # main frame packing
        # super().pack(**kwargs)
        super().place(**kwargs)

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

    @staticmethod
    def rm_func(masters: tuple, gates_n: tuple):
        for i, master in enumerate(masters):
            master.rm_gate(gates_n[i])

    def right_click(self, event):

        master = Toplevel(self)
        master.resizable(False, False)
        master.title("Gate Editor")
        master.iconbitmap("assets/qubit.ico")
        master.protocol("WM_DELETE_WINDOW", master.destroy)

        lbl_gate_plc = Label(master, text="Gate placement")
        lbl_acti_plc = Label(master, text="Activator placement")

        entry_gate_plc = Entry(master)
        entry_acti_plc = Entry(master)

        lbl_gate_plc.pack(side=TOP, fill=X, expand=True, padx=5)
        entry_gate_plc.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        lbl_acti_plc.pack(side=TOP, fill=X, expand=True, padx=5)
        entry_acti_plc.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)

    def invert_func(self, masters: tuple, gates_n: tuple):
        master_l1, master_l2 = masters
        gate_l1_n, gate_l2_n = gates_n

        gate_l1_name, gate_l2_name = master_l1.dynamic_content[gate_l1_n].gate, master_l2.dynamic_content[gate_l2_n].gate
        gate_l1_color = master_l1.dynamic_content[gate_l1_n].color

        self.rm_func(masters, gates_n)

        wid_l1 = DynamicButton(master=master_l1, gate=gate_l2_name, font=("Helvetica", 12, "bold"), cursor="sb_v_double_arrow", bg="cornsilk3",
                               command=lambda event: self.invert_func((master_l2, master_l1), (gate_l2_n, gate_l1_n)))
        wid_l2 = DynamicButton(master=master_l2, gate=gate_l1_name, font=("Times", 13, "bold"), cursor="pirate", bg=gate_l1_color,
                               command=lambda event: self.rm_func((master_l2, master_l1), (gate_l2_n, gate_l1_n)))
        wid_l1.bind("<Button-3>", self.right_click)

        master_l1.place_gate(gate_l1_n, wid_l1)
        master_l2.place_gate(gate_l2_n, wid_l2)

    def add_gate_to_circuit(self, line_n: int, gate_n: int, gate):
        """
        Add gate widget to specified line and gate

        :param line_n: line number
        :param gate_n: gate number
        :param gate: gate dragableButton object
        :return:
        """

        if gate.type == "complex":

            if line_n == len(self.LINES) - 1:
                pass

            else:
                master_l1 = self.LINES[line_n]
                master_l2 = self.LINES[line_n + 1]

                if master_l1.can_add_gate(gate_n) and master_l2.can_add_gate(gate_n):

                    wid_l1 = DynamicButton(master=master_l1, gate=gate.name, font=("Helvetica", 12, "bold"), cursor="pirate", bg=gate.color,
                                           command=lambda event: self.rm_func((master_l1, master_l2), (gate_n, gate_n)))
                    wid_l2 = DynamicButton(master=master_l2, gate="A", font=("Times", 13, "bold"), cursor="sb_v_double_arrow", bg="cornsilk3",
                                           command=lambda event: self.invert_func((master_l1, master_l2), (gate_n, gate_n)))
                    wid_l2.bind("<Button-3>", self.right_click)

                    master_l1.place_gate(gate_n, wid_l1)
                    master_l2.place_gate(gate_n, wid_l2)

        else:
            master = self.LINES[line_n]
            wid = DynamicButton(master=master, gate=gate.name, font=("Helvetica", 12, "bold"), cursor="pirate", bg=gate.color,
                                command=lambda event: self.rm_func((master,), (gate_n,)))

            master.place_gate(gate_n, wid)
