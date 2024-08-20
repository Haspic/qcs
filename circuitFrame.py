
from tkinter import *
from tkinter import ttk
from tkManagementFuncs import *

from dimensions import *


""" ===== ===== ===== DYNAMIC CANVAS ===== ===== ===== """


class DynamicButton(Button):

    def __init__(self, master, gate, command_tuple, bg, font, cursor, coor, **kwargs):

        # (line_n, gate_n)
        self.coor = coor
        # gate name
        self.name = gate

        # visuals
        self.color = bg
        self.font = font
        self.cursor = cursor

        self.binded = None
        self.command, self.args = command_tuple

        super().__init__(master=master, text=gate, cursor=cursor,
                         width=4, height=2, font=font, bg=bg, **kwargs)

        self.bind("<ButtonPress-1>", lambda _: self.command(*self.args))
        bindButtonHover(self, cl_leave=bg)

    def BIND(self, event, command):
        self.binded = (event, command)
        self.bind(event, lambda _: command(*self.args))


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
        return False

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
    def get_DynamicButton(master, prop):
        wid = DynamicButton(master=master,
                            gate=prop[0],
                            font=prop[1],
                            cursor=prop[2],
                            bg=prop[3],
                            coor=prop[4],
                            command_tuple=(prop[5], prop[6]))

        if prop[7] is not None:
            event, command = prop[7]
            wid.BIND(event, command)

        return wid

    @staticmethod
    def rm_func(masters: tuple, gate_n: int):
        for master in masters:
            master.rm_gate(gate_n)

    def right_click(self, masters: tuple, gate_n: int):
        master_targ, master_cont = masters

        gate_targ, gate_cont = master_targ.dynamic_content[gate_n], master_cont.dynamic_content[gate_n]

        def SAVE():
            # New position ('coor' property) for both gates (target and control)
            new_pos_targ = (int(box_targ_plc.get()), gate_n)
            new_pos_cont = (int(box_cont_plc.get()), gate_n)

            if new_pos_targ[0] != new_pos_cont[0]:

                # New masters
                new_master_targ = self.LINES[new_pos_targ[0]]
                new_master_cont = self.LINES[new_pos_cont[0]]

                # New masters argument
                new_masters_args = (new_master_targ, new_master_cont)

                # careful you are approaching ugly code, please do not interact with it too much

                if new_master_targ.can_add_gate(gate_n) or new_master_cont.can_add_gate(gate_n):

                    if new_master_targ.can_add_gate(gate_n) or new_pos_targ[0] == gate_targ.coor[0]:
                        # Move target from old master to new master
                        new_masters_targ = (master_targ, # old
                                            new_master_targ) # new
                        self.move_gate(gate_targ, new_masters_targ, new_pos_targ, (new_masters_args, gate_n))

                    if new_master_cont.can_add_gate(gate_n) or new_pos_cont[0] == gate_cont.coor[0]:
                        new_masters_cont = (master_cont, # old
                                            new_master_cont) # new
                        self.move_gate(gate_cont, new_masters_cont, new_pos_cont, (new_masters_args, gate_n))

            master.destroy()

        # NEW WINDOW
        master = Toplevel(self)
        master.resizable(False, False)
        master.title("Gate Editor")
        master.iconbitmap("assets/qubit.ico")
        master.protocol("WM_DELETE_WINDOW", master.destroy)

        # Buttons
        btn_save = Button(master, text="Save", command=SAVE, relief="groove")
        bindButtonHover(btn_save, cl_leave="#F0F0F0")

        # Labels
        lbl_targ_plc = Label(master, text="Target")
        lbl_cont_plc = Label(master, text="Control")

        # Combobox TARGET / GATE
        box_targ_plc = ttk.Combobox(master, width=5)
        box_targ_plc["values"] = tuple([i for i in range(self.size)])
        box_targ_plc['state'] = 'readonly'
        box_targ_plc.set(gate_targ.coor[0])

        # Combobox CONTROL / ACTIVATOR
        box_cont_plc = ttk.Combobox(master, width=5)
        box_cont_plc["values"] = tuple([i for i in range(self.size)])
        box_cont_plc['state'] = 'readonly'
        box_cont_plc.set(gate_cont.coor[0])

        # Placement
        lbl_targ_plc.grid(sticky=N, row=0, column=0, padx=5, pady=5)
        box_targ_plc.grid(sticky=N, row=0, column=1, padx=5, pady=5)
        lbl_cont_plc.grid(sticky=N, row=1, column=0, padx=5, pady=5)
        box_cont_plc.grid(sticky=N, row=1, column=1, padx=5, pady=5)
        btn_save.grid(sticky=N, row=2, column=0, columnspan=2, padx=5, pady=5)

    def move_gate(self, gate, masters: tuple, new_pos: tuple, new_args: tuple) -> None:
        """
        Moves a gate from a location to another (given in master frame object)

        :param gate: gate object to be moved
        :param masters: master frame objects (initial, final)
        :param new_pos: new position coordinated
        :param new_args: new modified arguments
        """
        master_orig, master_dest = masters

        line_n, gate_n = gate.coor

        prop = [gate.name, gate.font, gate.cursor, gate.color, new_pos, gate.command, new_args, gate.binded]

        self.rm_func((master_orig,), gate_n)
        wid = self.get_DynamicButton(master_dest, prop)
        master_dest.place_gate(gate_n, wid)



    def invert_func(self, masters: tuple, gate_n: int) -> None:
        """
        Inverts the position of a complex gate.

        :param masters: tuple of (target_master and control_master)
        :param gate_n: gate placement
        """

        master_targ, master_cont = masters

        # Retrieving DynamicButton objects
        gate_targ = master_targ.dynamic_content[gate_n]
        gate_cont = master_cont.dynamic_content[gate_n]

        args_masters, _ = gate_targ.args
        inverted_args = ((args_masters[1], args_masters[0]), gate_n)

        # Retrieving gate properties
        targ = [gate_targ.name, gate_targ.font, gate_targ.cursor, gate_targ.color, gate_cont.coor, gate_targ.command, inverted_args, gate_targ.binded]
        cont = [gate_cont.name, gate_cont.font, gate_cont.cursor, gate_cont.color, gate_targ.coor, gate_cont.command, inverted_args, gate_cont.binded]

        # Removing gate objects
        self.rm_func(masters, gate_n)

        # Recreating gate objects but with inverted properties
        wid_cont = self.get_DynamicButton(master_targ, cont)
        wid_targ = self.get_DynamicButton(master_cont, targ)

        # Place gates
        master_targ.place_gate(gate_n, wid_cont)
        master_cont.place_gate(gate_n, wid_targ)

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
                master_targ = self.LINES[line_n]
                master_cont = self.LINES[line_n + 1]

                if master_targ.can_add_gate(gate_n) and master_cont.can_add_gate(gate_n):

                    wid_targ = DynamicButton(master=master_targ,
                                             gate=gate.name,
                                             font=("Helvetica", 12, "bold"),
                                             cursor="pirate",
                                             bg=gate.color,
                                             coor=(line_n, gate_n),
                                             command_tuple=(self.rm_func, ((master_targ, master_cont), gate_n)))
                    wid_cont = DynamicButton(master=master_cont,
                                             gate="A",
                                             font=("Times", 13, "bold"),
                                             cursor="sb_v_double_arrow",
                                             bg="cornsilk3",
                                             coor=(line_n + 1, gate_n),
                                             command_tuple=(self.invert_func, ((master_targ, master_cont), gate_n)))
                    wid_cont.BIND("<Button-3>", self.right_click)

                    master_targ.place_gate(gate_n, wid_targ)
                    master_cont.place_gate(gate_n, wid_cont)

        else:
            master = self.LINES[line_n]
            wid = DynamicButton(master=master,
                                gate=gate.name,
                                font=("Helvetica", 12, "bold"),
                                cursor="pirate",
                                bg=gate.color,
                                coor=(line_n, gate_n),
                                command_tuple=(self.rm_func, ((master,), gate_n)))

            master.place_gate(gate_n, wid)
