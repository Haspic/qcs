
from tkinter import *
from tkinter import messagebox as mb


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

    def _init_circuit_(self, size):

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

        # controlled gates
        CX = DragableWidget(self, FRAME_circuit, grid=(3, 0, 2), gate_type="complex",
                           gate="CX", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CY = DragableWidget(self, FRAME_circuit, grid=(4, 0, 2), gate_type="complex",
                           gate="CY", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CZ = DragableWidget(self, FRAME_circuit, grid=(5, 0, 2), gate_type="complex",
                           gate="CZ", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        # hadamard
        H = DragableWidget(self, FRAME_circuit, grid=(6, 0, 3), gate_type="simple",
                           gate="H", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="dark sea green")

        # phase gate
        S = DragableWidget(self, FRAME_circuit, grid=(7, 0, 3), gate_type="simple",
                           gate="S", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="sea green")

        FRAME_circuit.pack(side=TOP)

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

        self.FRAME_buttons = Frame(self)

        """###########################################"""
        """############### LABELS INIT ###############"""
        """###########################################"""

        LABEL_circuit_size = Label(self.FRAME_buttons, text="Select circuit size (qubit number)", font=("Helvetica", 11, ""))
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

        CREATE_BUTTONS = [BTN_1, BTN_2, BTN_3, BTN_4, BTN_5]

        # BUTTON_LOAD = Button(FRAME_mainMenu, text="Load rocket", command=PASS, width=20, relief="groove")
        # BUTTON_BUILD = Button(FRAME_mainMenu, text="Build rocket", command=PASS, width=20, relief="groove")
        # BUTTON_SIM = Button(FRAME_mainMenu, text="Single simulation", command=lambda: self.LOAD_slide("singleSimulation"), width=20, relief="groove")
        # BUTTON_MONTECARLO = Button(FRAME_mainMenu, text="Monte Carlo simulations", command=lambda: self.LOAD_slide("monteCarloSimulation"), width=20, relief="groove")
        # BUTTON_QUIT = Button(FRAME_mainMenu, text="Quit", command=self.QUIT, width=20, relief="groove")

        """##################################################"""
        """############### SLIDE WIDGETS INIT ###############"""
        """##################################################"""

        WIDGET_mainMenu = [(FRAME_widgets, "pack", {"side": TOP, "pady": 20}),
                           (self.FRAME_buttons, "pack", {"side": TOP, "pady": 20}),
                           (LABEL_circuit_size, "pack", {"side": TOP, "pady": 20})]

        WIDGET_mainMenu += [(BUTTON, "pack", {"side": LEFT, "padx": 20}) for BUTTON in CREATE_BUTTONS]

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
