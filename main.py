
from tkinter import *
from tkinter import messagebox as mb

import itertools as itl

import matplotlib.pyplot as plt
import random

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
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

    def _init_plot_(self, size):

        plot_frame = Frame(self, width=plt_win_width, height=plt_win_height(size))

        fig, ax = plt.subplots()

        plot_canva = FigureCanvasTkAgg(fig, master=plot_frame)
        plot_canva.draw()

        plot_frame.place(x=plt_win_x, y=plt_win_y)
        plot_canva.get_tk_widget().place(x=0, y=0, width=plt_win_width, height=plt_win_height(size))

        measurement_states = ["".join(elt) for elt in itl.product("01", repeat=size)]
        ax.barh(measurement_states, [random.random()*100 for _ in measurement_states],
                height=0.9)

        fig.subplots_adjust(left=0.1, right=0.95, top=0.99, bottom=0.05 * (1 + 1 / 7 * (7 - size)))

        ax.tick_params(axis='y', which='major', labelsize=6 + (6 - size))
        ax.margins(x=0, y=0)

        ax.set_xticks([i * 10 for i in range(11)])
        ax.set_xticklabels([str(i * 10) for i in range(11)])

        # labels = ax.get_yticklabels()
        # plt.setp(labels, rotation=0, horizontalalignment='right')

    def _init_circuit_(self, size):

        self.geometry("{}x{}".format(init_win_width + bd*2 + plt_win_width, cir_y + bb + bd*2 + size*cir_line_height))
        self.FRAME_buttons.destroy()

        FRAME_circuit = circuit_frame(master=self, circuit_size=size)

        # GATES #

        # Identity
        I = DragableWidget(self, FRAME_circuit, grid=(0, 0, 0), gate_type="simple",
                                     gate="I", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="coral1")

        # Pauli matrices
        X = DragableWidget(self, FRAME_circuit, grid=(1, 0, 1), gate_type="simple",
                                     gate="X", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")
        Y = DragableWidget(self, FRAME_circuit, grid=(2, 0, 1), gate_type="simple",
                                     gate="Y", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")
        Z = DragableWidget(self, FRAME_circuit, grid=(1, 1, 1), gate_type="simple",
                                     gate="Z", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")

        # hadamard
        H = DragableWidget(self, FRAME_circuit, grid=(3, 0, 2), gate_type="simple",
                           gate="H", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="dark sea green")

        # phase gate
        S = DragableWidget(self, FRAME_circuit, grid=(3, 1, 2), gate_type="simple",
                           gate="S", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="sea green")

        # controlled gates
        CX = DragableWidget(self, FRAME_circuit, grid=(4, 0, 3), gate_type="complex",
                           gate="CX", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CY = DragableWidget(self, FRAME_circuit, grid=(5, 0, 3), gate_type="complex",
                           gate="CY", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CZ = DragableWidget(self, FRAME_circuit, grid=(6, 0, 3), gate_type="complex",
                           gate="CZ", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")


        CH = DragableWidget(self, FRAME_circuit, grid=(7, 0, 4), gate_type="complex",
                           gate="CH", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="light sea green")

        CS = DragableWidget(self, FRAME_circuit, grid=(8, 0, 4), gate_type="complex",
                           gate="CS", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="light sea green")

        # # custom activator gate
        # CUSTOM = DragableWidget(self, FRAME_circuit, grid=(6, 0, 3), gate_type="complex",
        #                         gate="?", width=4, height=2,
        #                         font=("Helvetica", 12, "bold"), bg="azure")

        FRAME_circuit.place(x=cir_x, y=cir_y)
        self._init_plot_(size)

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
        # LABEL_built_status = Label(FRAME_mainMenu, text="Rocket not built", font=("Helvetica", 9, "italic bold"), fg="orange red")

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

        # BUTTON_LOAD = Button(FRAME_mainMenu, text="Load rocket", command=PASS, width=20, relief="groove")
        # BUTTON_BUILD = Button(FRAME_mainMenu, text="Build rocket", command=PASS, width=20, relief="groove")
        # BUTTON_SIM = Button(FRAME_mainMenu, text="Single simulation", command=lambda: self.LOAD_slide("singleSimulation"), width=20, relief="groove")
        # BUTTON_MONTECARLO = Button(FRAME_mainMenu, text="Monte Carlo simulations", command=lambda: self.LOAD_slide("monteCarloSimulation"), width=20, relief="groove")
        # BUTTON_QUIT = Button(FRAME_mainMenu, text="Quit", command=self.QUIT, width=20, relief="groove")

        """##################################################"""
        """############### SLIDE WIDGETS INIT ###############"""
        """##################################################"""

        WIDGET_mainMenu = [(FRAME_widgets, "place", {"x": bb, "y": bb}),
                           (self.FRAME_buttons, "place", {"x": cir_x, "y": cir_y + bb*2}),
                           (LABEL_circuit_size, "place", {"x": cir_x, "y": cir_y})]

        WIDGET_mainMenu += [(BUTTON, "pack", {"side": LEFT}) for i, BUTTON in enumerate(CREATE_BUTTONS)]

        # WIDGET_singleSimulation = [(BUTTON_BACK, "pack", {"expand": True})]
        # WIDGET_monteCarloSimulation = [(BUTTON_BACK, "pack", {"expand": True})]

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
