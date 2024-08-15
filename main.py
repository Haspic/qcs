
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

        FRAME_circuit = circuit_frame(master=self, circuit_size=circuit_size)

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

        X = DragableWidget(FRAME_circuit, grid=(0, 0, 0), gate_type="simple",
                                     master=self, gate="X", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")

        Y = DragableWidget(FRAME_circuit, grid=(1, 0, 0), gate_type="simple",
                                     master=self, gate="Y", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")

        Z = DragableWidget(FRAME_circuit, grid=(0, 1, 0), gate_type="simple",
                                     master=self, gate="Z", width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")

        CX = DragableWidget(FRAME_circuit, grid=(2, 0, 1), gate_type="complex",
                           master=self, gate="CX", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CY = DragableWidget(FRAME_circuit, grid=(3, 0, 1), gate_type="complex",
                           master=self, gate="CY", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        CZ = DragableWidget(FRAME_circuit, grid=(2, 1, 1), gate_type="complex",
                           master=self, gate="CZ", width=4, height=2,
                           font=("Helvetica", 12, "bold"), bg="steelblue1")

        H = DragableWidget(FRAME_circuit, grid=(4, 0, 2), gate_type="simple",
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


main = window()
