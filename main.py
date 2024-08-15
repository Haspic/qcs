
from tkinter import *
from tkinter import ttk

from tkinter import messagebox as mb


""" ===== ===== ===== DIMENSIONS ===== ===== ===== """


rb = 20  # border - border
bd = 4   # borders width

win_width = 900
win_height = 600

wid_height = 150
wid_width = win_width - 2*rb

cir_height = win_height - wid_height - 3*rb
cir_width = wid_width
cir_line_height = 70

gate_size = 56

circuit_size = 4
circuit_gate_width = 14


""" ===== ===== ===== TKINTER MANAGEMENT FUNCTIONS ===== ===== ===== """


def PASS():
    pass

def bindButtons(slide_widgets):
    for widget, method, kwargs in slide_widgets:
        if isinstance(widget, Button):
            bindButtonHover(widget)

def bindButtonHover(button, cl_en="gold", cl_le="steelblue3"):
    """Configure given button, in order for it to change color when the mouse hovers over it"""
    # mouse hover
    button.bind("<Enter>", lambda i: button.config(bg=cl_en))  # #999999
    # mouse leaves hover
    button.bind("<Leave>", lambda i: button.config(bg=cl_le))  # #F0F0F0

def buildFrame(frame_widgets):
    """Builds frame from given widget list (order matters)"""
    for widget, method, kwargs in frame_widgets:

        match method:

            case "pack":
                widget.pack(**kwargs)
            case "grid":
                widget.grid(**kwargs)
            case "place":
                widget.place(**kwargs)

def eraseFrame(frame_widgets):
    """Erase frame from given widget list"""
    for widget, method, kwargs in frame_widgets:

        match method:

            case "pack":
                widget.pack_forget()
            case "grid":
                widget.grid_forget()
            case "place":
                widget.place_forget()


""" ===== ===== ===== TKINTER OBJECTS ===== ===== ===== """


class DragableWidget(Button):

    def _reset_position(self):
        self.place(x=self.x_init, y=self.y_init)

    def __init__(self, circuit_frame, grid, gate, bg, **kwargs):

        super().__init__(text=gate, bg=bg, **kwargs)

        self.gate = gate
        self.circuit = circuit_frame

        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease>", self.on_drop)
        bindButtonHover(self, cl_le=bg)

        # ----- #

        self.x_init = 20 + rb + grid[0] * 60 + grid[2] * 20
        self.y_init = 20 + rb + grid[1] * 60

        self.x_offset = -10
        self.y_offset = -10

        # ----- #

        self.selected_line = None
        self.selected_gate = None
        self.LOCKED = True

        self.configure(cursor="pencil")
        self._reset_position()

    def on_drag(self, event):

        # Mouse position
        X = self.master.winfo_pointerx() - self.master.winfo_rootx()
        Y = self.master.winfo_pointery() - self.master.winfo_rooty()

        self.place(x = X + self.x_offset, y = Y + self.y_offset)

        # Is located in X drag-n-drop area ?
        if rb < X < win_width - rb:

            IN = False

            # For all existing lines (qubits)
            for i in range(circuit_size):

                top = rb*2 + wid_height + cir_line_height * i
                btm = top + cir_line_height

                # Is located in Y drag-n-drop area ?
                if top <= Y < btm:

                    self.selected_gate = int((X - rb) // (cir_width / circuit_gate_width))

                    IN = True
                    for j, line in enumerate(self.circuit.LINES):
                        if i == j:
                            self.selected_line = j

                            line.up()
                            line.set_dynamic_gate(self.selected_gate)

                        else:
                            line.down()



            # Not in Y drag-n-drop area
            if not IN:
                for line in self.circuit.LINES:
                    self.selected_line = None
                    self.selected_gate = None
                    line.down()

        # Not in X drag-n-drop area
        else:
            for line in self.circuit.LINES:
                self.selected_line = None
                self.selected_gate = None
                line.down()

    def on_drop(self, event):

        if self.selected_line is not None:
            self.circuit.add_gate(self.selected_line, self.selected_gate, self.gate)

        for line in self.circuit.LINES:
            line.configure(relief='flat')

        self._reset_position()
        self.selected_line = None


""" ----- ----- ----- ----- ----- ----- """


class DynamicCanvas(Canvas):

    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.state = "line" # 'line' or 'rect'
        self.makeLine()

    def reset(self):
        if self.state == "rect":
            self.empty()
            self.makeLine()

    def empty(self):
        self.delete("all")

    def makeLine(self):
        self.create_line(0, 28, 65, 28, width=1)
        self.state = "line"

    def makeRect(self):
        self.empty()
        self.create_rectangle(5, 5, 55, 55, width=1, dash=(3, 1))
        self.state = "rect"


""" ----- ----- ----- ----- ----- ----- """


class qubit_line(Frame):

    def up(self):
        self.configure(relief='raised')

    def down(self):
        self.configure(relief='flat')
        self.reset_dynamic_gate()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dynamic_content = [DynamicCanvas(self, width=gate_size, height=gate_size) for _ in range(circuit_gate_width)]

        for i, canva in enumerate(self.dynamic_content):
            canva.grid(sticky=N, column=i, row=0)

    def reset_dynamic_gate(self):
        for gate in self.dynamic_content:
            if isinstance(gate, DynamicCanvas):
                gate.reset()

    def set_dynamic_gate(self, gate_number):

        self.reset_dynamic_gate()

        if gate_number is not None:
            c = self.dynamic_content[gate_number]

            if isinstance(c, DynamicCanvas):
                c.makeRect()

    def rm_gate(self, widget, selected_gate):
        widget.destroy()
        self.dynamic_content[selected_gate] = DynamicCanvas(self, width=gate_size, height=gate_size)
        self.dynamic_content[selected_gate].grid(sticky=N, column=selected_gate, row=0)

    def add_gate(self, wid_gate, gate_number):

        self.reset_dynamic_gate()
        c = self.dynamic_content[gate_number]

        if isinstance(c, DynamicCanvas):
            c.destroy()

            self.dynamic_content[gate_number] = wid_gate
            wid_gate.grid(sticky=W, column=gate_number, row=0, padx=5, pady=0)

""" ----- ----- ----- ----- ----- ----- """


class circuit_subframe(Frame):


    def _init_size_(self, circuit_size):

        LINES = [] # QUBITS

        # Initialize all sub-frames (1 per qubit)
        for i in range(circuit_size):

            SUBFRAME = qubit_line(master=self,
                                  width=self.line_width,
                                  height=self.line_height,
                                  bd=bd,
                                  relief='flat')

            LINES.append(SUBFRAME)

        return LINES

    def __init__(self, circuit_size, relief="ridge", bd=bd, **kwargs):

        self.line_width = cir_width - 2*bd
        self.line_height = cir_line_height

        width = self.line_width
        height = self.line_height * circuit_size

        super().__init__(relief=relief, bd=bd, width=width, height=height, **kwargs)
        self.LINES = self._init_size_(circuit_size)

    def pack(self, **kwargs):

        for line in self.LINES:
            line.pack(side=TOP, fill=X, expand=True)

        # control line such that when all lines are filled, the frames
        # do not collapse on middle (because we are using pack for the gates)

        control_line = Frame(self, width=self.line_width)
        control_line.pack(side=TOP, fill=X, expand=True)

        super().pack(**kwargs)

    def add_gate(self, selected_line, selected_gate, gate_name):

        master = self.LINES[selected_line]

        wid_gate = Button(master, text=gate_name, width=4, height=2,
                          font=("Helvetica", 12, "bold"), bg="cornsilk3", cursor="pirate")
        bindButtonHover(wid_gate, cl_le="cornsilk3")
        wid_gate.bind("<ButtonPress-1>", lambda event: master.rm_gate(wid_gate, selected_gate))

        master.add_gate(wid_gate, selected_gate)

""" ----- ----- ----- ----- ----- ----- """


class window(Tk):

    def QUIT(self):
        """Quit program when pressing quit button"""

        # if self.currently_editing:
        #     ANSWER = mb.askyesno("Quit", "You are currently in edition mode,\nare you sure you want to quit?")
        # else:
        #     ANSWER = True
        #
        # if ANSWER:

        # Quit tkinter window
        self.destroy()
        # Force quit python if any unexpected errors occurs
        exit()

    def __init__(self):
        super().__init__()

        self.lastWindow = "mainMenu"
        self.currently_editing = False

        """ ######################################## """
        """ ############### APP INIT ############### """
        """ ######################################## """

        self.geometry("{}x{}".format(win_width, win_height))
        # self.minsize(750, 500)
        self.resizable(False, False)
        self.title("Quantum Circuit Simulator")
        self.iconbitmap("assets/qubit.ico")
        self.protocol("WM_DELETE_WINDOW", self.QUIT)
        # self.configure(background="#1E1E1E")

        """ ############################################ """
        """ ############### MENUBAR INIT ############### """
        """ ############################################ """

        menuBar = Menu(self)

        # Help menubar
        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Load info", command=PASS)
        menuBar.add_cascade(label="Help", menu=helpMenu)

        self.config(menu=menuBar)

        """###########################################"""
        """############### FRAMES INIT ###############"""
        """###########################################"""

        FRAME_widgets = Frame(self,
                              width=wid_width,
                              height=wid_height,
                              bd=4,
                              relief='ridge')

        FRAME_circuit = circuit_subframe(master=self, circuit_size=circuit_size)

        """###########################################"""
        """############### LABELS INIT ###############"""
        """###########################################"""

        # MAIN SLIDE #

        # LABEL_load_status = Label(FRAME_mainMenu, text="No rocket loaded", font=("Helvetica", 9, "italic bold"), fg="orange red")
        # LABEL_built_status = Label(FRAME_mainMenu, text="Rocket not built", font=("Helvetica", 9, "italic bold"), fg="orange red")

        """#################################################"""
        """############### INPUT WIDGET INIT ###############"""
        """#################################################"""

        """ -------------------- BUTTONS -------------------- """

        # GATES #

        X = DragableWidget(FRAME_circuit, grid=(0, 0, 0),
                                     master=self, gate="X", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")

        Y = DragableWidget(FRAME_circuit, grid=(1, 0, 0),
                                     master=self, gate="Y", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")

        Z = DragableWidget(FRAME_circuit, grid=(0, 1, 0),
                                     master=self, gate="Z", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")

        CX = DragableWidget(FRAME_circuit, grid=(2, 0, 1),
                           master=self, gate="CX", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CY = DragableWidget(FRAME_circuit, grid=(3, 0, 1),
                           master=self, gate="CY", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CZ = DragableWidget(FRAME_circuit, grid=(2, 1, 1),
                           master=self, gate="CZ", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        H = DragableWidget(FRAME_circuit, grid=(4, 0, 2),
                           master=self, gate="H", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="dark sea green")

        # MAIN SLIDE #

        # BUTTON_CREATE = Button(FRAME_mainMenu, text="Create rocket", command=PASS, width=20, relief="groove")
        # BUTTON_LOAD = Button(FRAME_mainMenu, text="Load rocket", command=PASS, width=20, relief="groove")
        # BUTTON_BUILD = Button(FRAME_mainMenu, text="Build rocket", command=PASS, width=20, relief="groove")
        # BUTTON_SIM = Button(FRAME_mainMenu, text="Single simulation", command=lambda: self.LOAD_slide("singleSimulation"), width=20, relief="groove")
        # BUTTON_MONTECARLO = Button(FRAME_mainMenu, text="Monte Carlo simulations", command=lambda: self.LOAD_slide("monteCarloSimulation"), width=20, relief="groove")
        # BUTTON_QUIT = Button(FRAME_mainMenu, text="Quit", command=self.QUIT, width=20, relief="groove")

        """##################################################"""
        """############### SLIDE WIDGETS INIT ###############"""
        """##################################################"""

        WIDGET_mainMenu = [(FRAME_widgets, "pack", {"side": TOP, "pady": 20}),
                           (FRAME_circuit, "pack", {"side": TOP})]

        # WIDGET_singleSimulation = [(BUTTON_BACK, "pack", {"expand": True})]

        # WIDGET_monteCarloSimulation = [(BUTTON_BACK, "pack", {"expand": True})]

        self.SLIDE_WIDGETS = {"mainMenu": WIDGET_mainMenu}

        # Binding all buttons to hover method
        for slide_widgets in self.SLIDE_WIDGETS.values():
            bindButtons(slide_widgets)

        self.LOAD_slide("mainMenu", unload_previous=False)
        self.mainloop()

    def LOAD_slide(self, slide, unload_previous=True):
        if unload_previous:
            eraseFrame(self.SLIDE_WIDGETS[self.lastWindow])

        if type(slide) == list:
            buildFrame(slide)
        else:
            buildFrame(self.SLIDE_WIDGETS[slide])
            self.lastWindow = slide


main = window()
