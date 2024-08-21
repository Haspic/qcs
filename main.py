
from tkinter import *
from tkinter import messagebox as mb

import itertools as itl

import matplotlib.pyplot as plt
import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

""" ===== ===== ===== SIMULATOR ===== ===== ===== """

from circuit import circuit
from gates import _0, _1, _I, _X, _Y, _Z, _CZ, _CY, _CX, _S, _H, _sqrt
from gates import kron, Gate

""" ===== ===== ===== DIMENSIONS ===== ===== ===== """

from dimensions import *

""" ===== ===== ===== TKINTER MANAGEMENT FUNCTIONS ===== ===== ===== """

from tkManagementFuncs import *

""" ===== ===== ===== TKINTER OBJECTS ===== ===== ===== """

from dragableWidget import DragableWidget
from circuitFrame import circuit_frame

""" ----- ----- ----- ----- ----- ----- """


class window(Tk):

    def QUIT(self):
        """ Quit function """
        # Quit tkinter window
        self.destroy()
        # Force quit python if any unexpected errors occurs
        exit()

    def update_plot(self, button_call=False) -> None:
        """
        Call after circuit change in order to update the plot accordingly (will only plot dynamically
        if self.dynamic_plotting is activated)

        :param button_call: force plot change (when using button call instead of dynamic plotting)
        """

        if self.dynamic_plotting.get() or button_call:

            CIRCUIT = self.FRAME_circuit.convert_to_simulator()
            probs = CIRCUIT.get_probabilities(self.measurement_states, percentage=True)
            self._set_plot(probs)

    def _set_plot(self, y_data):
        self.ax.clear()
        self.ax.barh(self.measurement_states, y_data, height=0.9)

        size = self.size
        self.ax.tick_params(axis='y', which='major', labelsize=6 + (6 - size))
        self.ax.margins(x=0, y=0)
        self.fig.subplots_adjust(left=0.1, right=0.95, top=0.99, bottom=0.05 * (1 + 1 / 7 * (7 - size)))

        self.ax.set_xticks([i * 10 for i in range(11)])
        self.ax.set_xticklabels([str(i * 10) for i in range(11)])

        self.plot_canva.draw()

    def _init_plot_(self):
        """ Initialize the plot """

        # Plot frame for plot placement
        plot_frame = Frame(self, width=plt_win_width, height=plt_win_height(self.size))

        self.fig, self.ax = plt.subplots()

        # Plot canva inserted in tkinter
        self.plot_canva = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.plot_canva.draw()

        plot_frame.place(x=plt_win_x, y=plt_win_y)
        self.plot_canva.get_tk_widget().place(x=0, y=0, width=plt_win_width, height=plt_win_height(self.size))

        self.fig.set_facecolor("#F0F0F0")
        self.ax.set_facecolor("#F0F0F0")

        # Initial update
        self.update_plot(button_call=True)

    def _init_circuit_(self, size: int) -> None:
        """
        Initialize circuit frame object and all dragable gates widgets.

        :param size: Size of the circuit
        """

        self.size = size
        # Initialize all possible measurement states (used for plots)
        self.measurement_states = ["".join(elt) for elt in itl.product("01", repeat=size)]

        # Change geometry accordingly to size chosen
        new_x = init_win_width + bd*2 + plt_win_width
        new_y = cir_y + bb + bd*2 + size*cir_line_height + 30
        self.geometry("{}x{}".format(new_x, new_y))

        self.FRAME_buttons.destroy()

        self.FRAME_circuit = circuit_frame(master=self, circuit_size=size)

        """ ----- ----- ----- BUTTONS ----- ----- ----- """

        self.dynamic_plotting = IntVar()
        btn_dynamic_plt = Checkbutton(self, text="Dynamic plotting",
                                      variable=self.dynamic_plotting,
                                      onvalue=1, offvalue=0, height=1, width=15)
        btn_dynamic_plt.place(x=new_x - 280, y=new_y - 40)

        btn_plot = Button(self, text="Get probabilities",
                          height=1, width=15, relief="groove",
                          command=lambda: self.update_plot(button_call=True))
        bindButtonHover(btn_plot, cl_leave="#F0F0F0")
        btn_plot.place(x=new_x - 145, y=new_y - 40)

        """ ----- ----- ----- DRAGABLE GATES WIDGETS ----- ----- ----- """

        # Identity
        I = DragableWidget(self, self.FRAME_circuit, grid=(0, 0, 0), gate_type="simple",
                                     gate="I", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="coral1")

        # Pauli matrices
        X = DragableWidget(self, self.FRAME_circuit, grid=(1, 0, 1), gate_type="simple",
                                     gate="X", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")
        Y = DragableWidget(self, self.FRAME_circuit, grid=(2, 0, 1), gate_type="simple",
                                     gate="Y", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")
        Z = DragableWidget(self, self.FRAME_circuit, grid=(1, 1, 1), gate_type="simple",
                                     gate="Z", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")

        # hadamard
        H = DragableWidget(self, self.FRAME_circuit, grid=(3, 0, 2), gate_type="simple",
                           gate="H", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="dark sea green")

        # phase gate
        S = DragableWidget(self, self.FRAME_circuit, grid=(3, 1, 2), gate_type="simple",
                           gate="S", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="sea green")

        # controlled gates
        CX = DragableWidget(self, self.FRAME_circuit, grid=(4, 0, 3), gate_type="complex",
                           gate="CX", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CY = DragableWidget(self, self.FRAME_circuit, grid=(5, 0, 3), gate_type="complex",
                           gate="CY", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CZ = DragableWidget(self, self.FRAME_circuit, grid=(6, 0, 3), gate_type="complex",
                           gate="CZ", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")


        CH = DragableWidget(self, self.FRAME_circuit, grid=(7, 0, 4), gate_type="complex",
                           gate="CH", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="light sea green")

        CS = DragableWidget(self, self.FRAME_circuit, grid=(8, 0, 4), gate_type="complex",
                           gate="CS", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="light sea green")

        self.FRAME_circuit.place(x=cir_x, y=cir_y)
        self._init_plot_()

    def __init__(self):
        """
        Main window object
        """
        super().__init__()

        self.lastWindow = "mainMenu"
        self.currently_editing = False

        """ ######################################## """
        """ ############### APP INIT ############### """
        """ ######################################## """

        self.geometry("{}x{}".format(init_win_width, init_win_height))
        # self.minsize(750, 500)
        self.resizable(False, False)
        self.title("Quantum Circuit Simulator")
        self.iconbitmap("assets/qubit.ico")
        self.protocol("WM_DELETE_WINDOW", self.QUIT)
        # self.configure(background="#1E1E1E")

        """ ############################################ """
        """ ############### MENUBAR INIT ############### """
        """ ############################################ """
        #
        # menuBar = Menu(self)
        #
        # # Help menubar
        # helpMenu = Menu(menuBar, tearoff=0)
        # helpMenu.add_command(label="Load info", command=PASS)
        # menuBar.add_cascade(label="Help", menu=helpMenu)
        #
        # self.config(menu=menuBar)

        """###########################################"""
        """############### FRAMES INIT ###############"""
        """###########################################"""

        FRAME_widgets = Frame(self,
                              width=wid_frame_width,
                              height=wid_frame_height,
                              bd=4,
                              relief='ridge')

        self.FRAME_buttons = Frame(self)

        """###########################################"""
        """############### LABELS INIT ###############"""
        """###########################################"""

        LABEL_circuit_size = Label(self, text="Select circuit size (qubit number)", font=("Helvetica", 11, "underline"))

        """#################################################"""
        """############### INPUT WIDGET INIT ###############"""
        """#################################################"""

        """ -------------------- BUTTONS -------------------- """

        # is not defined by loop as it created problems somehow
        BTN_1 = Button(self.FRAME_buttons, text="1", command=lambda: self._init_circuit_(1), width=10, relief="groove")
        BTN_2 = Button(self.FRAME_buttons, text="2", command=lambda: self._init_circuit_(2), width=10, relief="groove")
        BTN_3 = Button(self.FRAME_buttons, text="3", command=lambda: self._init_circuit_(3), width=10, relief="groove")
        BTN_4 = Button(self.FRAME_buttons, text="4", command=lambda: self._init_circuit_(4), width=10, relief="groove")
        BTN_5 = Button(self.FRAME_buttons, text="5", command=lambda: self._init_circuit_(5), width=10, relief="groove")
        BTN_6 = Button(self.FRAME_buttons, text="6", command=lambda: self._init_circuit_(6), width=10, relief="groove")

        CREATE_BUTTONS = [BTN_1, BTN_2, BTN_3, BTN_4, BTN_5, BTN_6]

        """##################################################"""
        """############### SLIDE WIDGETS INIT ###############"""
        """##################################################"""

        WIDGET_mainMenu = [(FRAME_widgets, "place", {"x": bb, "y": bb}),
                           (self.FRAME_buttons, "place", {"x": cir_x, "y": cir_y + bb*2}),
                           (LABEL_circuit_size, "place", {"x": cir_x, "y": cir_y})]

        # structure imported from other project, could have been simplified for the smaller scale of this one
        # but not necessary
        WIDGET_mainMenu += [(BUTTON, "pack", {"side": LEFT}) for i, BUTTON in enumerate(CREATE_BUTTONS)]
        self.SLIDE_WIDGETS = {"mainMenu": WIDGET_mainMenu}

        # Binding all buttons to hover method
        for slide_widgets in self.SLIDE_WIDGETS.values():
            bindButtons(slide_widgets, cl_leave="#F0F0F0")

        self.LOAD_slide("mainMenu", unload_previous=False)
        self.mainloop()

    def LOAD_slide(self, slide: str or list, unload_previous=True) -> None:
        """
        Load slide with given slide name or widget list

        :param slide: slide name or widget list
        :param unload_previous: boolean, unload previous slide or not?
        """
        if unload_previous:
            eraseFrame(self.SLIDE_WIDGETS[self.lastWindow])

        if type(slide) == list:
            buildFrame(slide)
        else:
            buildFrame(self.SLIDE_WIDGETS[slide])
            self.lastWindow = slide


if __name__ == "__main__":
    main = window()
