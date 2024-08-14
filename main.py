
from tkinter import *
from tkinter import ttk

from tkinter import messagebox as mb


""" ===== ===== ===== ===== ===== ===== """


def PASS():
    pass


def bindButtons(slide_widgets):
    for widget, method, kwargs in slide_widgets:
        if isinstance(widget, Button):
            bindButtonHover(widget)

def bindButtonHover(button):
    """Configure given button, in order for it to change color when the mouse hovers over it"""
    # mouse hover
    button.bind("<Enter>", lambda i: button.config(bg="gold"))  # #999999
    # mouse leaves hover
    button.bind("<Leave>", lambda i: button.config(bg="steelblue3"))  # #F0F0F0

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


""" ===== ===== ===== ===== ===== ===== """

class DragableWidget(Button):

    def __init__(self, circuit_frame, **kwargs):
        super().__init__(**kwargs)

        self.circuit = circuit_frame

        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease>", self.on_drop)

        # ----- #

        self.w = 35 * (self.winfo_width() / 2)
        self.h = 35 * (self.winfo_height() / 2)

        # ----- #

        self.LOCKED = False
        self.configure(cursor="pencil")

    def on_drag(self, event):
        # if not self.LOCKED:
        #     X, Y = self.master.winfo_pointerx() - self.master.winfo_rootx(), self.master.winfo_pointery() - self.root.winfo_rooty()  # mouse position
        #     self.x = X - (200 + self.w)  # 200 for y offset, 30 for middle of button
        #     self.y = Y - self.h  # 20 for middle of button
        #     self.place(x=self.x, y=self.y)
        # print(event.x, event.y)

        # Mouse position
        X = self.master.winfo_pointerx() - self.master.winfo_rootx()
        Y = self.master.winfo_pointery() - self.master.winfo_rooty()

        self.place(x = X - 10, y = Y - 10)

        # Located in drag-n-drop area
        if 50 < X < 850:

            if 255 <= Y < 330: # L1
                for i, line in enumerate(self.circuit.LINES):
                    if i == 0:
                        line.configure(relief='raised')
                    else:
                        line.configure(relief='flat')

            elif 330 <= Y < 405: # L2
                for i, line in enumerate(self.circuit.LINES):
                    if i == 1:
                        line.configure(relief='raised')
                    else:
                        line.configure(relief='flat')

            elif 405 <= Y < 480: # L3
                for i, line in enumerate(self.circuit.LINES):
                    if i == 2:
                        line.configure(relief='raised')
                    else:
                        line.configure(relief='flat')

            elif 480 <= Y < 555: # L4
                for i, line in enumerate(self.circuit.LINES):
                    if i == 3:
                        line.configure(relief='raised')
                    else:
                        line.configure(relief='flat')

            else:
                for line in self.circuit.LINES:
                    line.configure(relief='flat')
        else:
            for line in self.circuit.LINES:
                line.configure(relief='flat')


    def on_drop(self, event):
        # if not self.LOCKED:
        #     X, Y = self.master.winfo_pointerx() - self.master.winfo_rootx(), self.master.winfo_pointery() - self.master.winfo_rooty()
        #     self.x = X - (200 + self.w)
        #     self.y = Y - self.h
        #     self.place(x=self.x, y=self.y)

        #     main.update_paths()
        #
        # else:
        #     main.queue_state(self.NAME)

        for line in self.circuit.LINES:
            line.configure(relief='flat')

        self.place(x=35, y=33)


""" ===== ===== ===== ===== ===== ===== """

class qubit_line(Frame):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class circuit_subframe(Frame):


    def _init_size_(self, circuit_size):

        LINES = [] # QUBITS

        # Initialize all sub-frames (1 per qubit)
        for i in range(circuit_size):

            SUBFRAME = qubit_line(master=self,
                                  width=self.line_width,
                                  height=self.line_height,
                                  bd=4,
                                  relief='flat')

            LINES.append(SUBFRAME)

        return LINES

    def __init__(self, circuit_size, relief="ridge", bd=4, **kwargs):

        self.line_width = 300
        self.line_height = 65

        width = self.line_width
        height = self.line_height * circuit_size

        super().__init__(relief=relief, bd=bd, width=width, height=height, **kwargs)
        self.LINES = self._init_size_(circuit_size)

    def pack(self, **kwargs):

        for line in self.LINES:
            line.pack(side=TOP, fill=X, expand=True)

        super().pack(**kwargs)


""" ===== ===== ===== ===== ===== ===== """


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

        self.geometry("900x600")
        # self.minsize(750, 500)
        self.resizable(True, True)
        self.title("Quantum Circuit Simulator")
        self.iconbitmap("assets/qubit.ico")
        self.protocol("WM_DELETE_WINDOW", self.QUIT)
        # self.configure(background="#1E1E1E")

        """ ############################################ """
        """ ############### MENUBAR INIT ############### """
        """ ############################################ """

        menuBar = Menu(self)

        # Rocket menubar
        rocketMenu = Menu(menuBar, tearoff=0)
        rocketMenu.add_command(label="Create", command=PASS)
        rocketMenu.add_command(label="Load", command=PASS)
        rocketMenu.add_command(label="Quit", command=self.QUIT)
        menuBar.add_cascade(label="Rocket", menu=rocketMenu)

        # Help menubar
        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Load info", command=PASS)
        menuBar.add_cascade(label="Help", menu=helpMenu)

        self.config(menu=menuBar)

        """###########################################"""
        """############### FRAMES INIT ###############"""
        """###########################################"""

        FRAME_widgets = Frame(self,
                              width=860,
                              height=200,
                              bd=4,
                              relief='ridge')

        FRAME_circuit = circuit_subframe(master=self, circuit_size=4)

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

        # TESTS #

        TEST_BUTTON = DragableWidget(FRAME_circuit, master=self, text="H",
                                     command=lambda: PASS, width=4, height=2,
                                     font=("Helvetica", 12, "bold"), bg="steelblue3")


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
                           (FRAME_circuit, "pack", {"side": TOP, "pady": 20}),
                           (TEST_BUTTON, "place", {"x": 35, "y": 33})]

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
