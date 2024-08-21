
from tkinter import *
from tkinter import font as tkFont
from tkManagementFuncs import bindButtonHover

from dimensions import *

""" ----- ----- ----- ----- ----- ----- """


class twinButton(Button):

    def __init__(self, master, x, y, **kwargs):

        super().__init__(master=master, text="A", **kwargs)

        # ----- #

        self.x_offset = 0
        self.y_offset = 60

        X = x + self.x_offset
        Y = y + self.y_offset

        # ----- #

        self.place(x=X, y=Y)

    def follow(self, x, y):
        self.place(x = x + self.x_offset, y = y + self.y_offset)


""" ----- ----- ----- ----- ----- ----- """


class DragableWidget(Button):

    def _reset_position(self):
        self.place(x=self.x_init, y=self.y_init)
        if self.type == "complex":
            self.twin.follow(self.x_init, self.y_init)

    def __init__(self,
                 master,
                 circuit_frame,
                 grid: tuple,
                 gate: str,
                 gate_type: str,
                 bg: str,
                 **kwargs):
        """
        Dragable gate widget.

        :param circuit_frame: tkinter master element (circuit_subframe class)
        :param grid: tuple of grid position within gate widget frame (column, row, group)
        :param gate: gate name
        :param gate_type: simple or complex (simple -> X, H.. complex -> CX, CZ..)
        :param bg: background color of gate widget
        :param kwargs: keyword arguments passed to tkinter Button widget
        """

        # tkinter Button widget
        super().__init__(master=master, text=gate, bg=bg, **kwargs)

        self.name = gate
        self.type = gate_type
        self.color = bg
        self.circuit = circuit_frame

        # bind dragging to drag functions
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease>", self.on_drop)
        bindButtonHover(self, cl_leave=bg)

        # ----- #

        self.x_init = 20 + bb + grid[0] * 60 + grid[2] * 20
        self.y_init = 20 + bb + grid[1] * 60

        self.x_offset = -10
        self.y_offset = -10

        # ----- #

        # If complex gate, add a twin activation gate
        if self.type == 'complex':
            del kwargs["font"]
            self.twin = twinButton(master=master, x=self.x_init, y=self.y_init,
                                   font=("Times", 13, "bold"), **kwargs)

        # ----- #

        self.selected_line = None
        self.selected_gate = None
        self.LOCKED = True

        self.configure(cursor="pencil")

        # Initialize widget position
        self._reset_position()

    def on_drag(self, event) -> None:
        """
        Dragging function, moves the widget's position to the mouse and activate
        appropriate visual animation on the qubits/lines subframes.

        :param event: bound event
        """

        # Mouse position
        X = self.master.winfo_pointerx() - self.master.winfo_rootx()
        Y = self.master.winfo_pointery() - self.master.winfo_rooty()

        X += self.x_offset
        Y += self.y_offset

        # Move widget
        self.place(x=X, y=Y)
        if self.type == "complex":
            self.twin.follow(X, Y)

        # Is located in X drag-n-drop area ?
        if (cir_x + bd) < X < (init_win_width - bb - 2*bd):

            IN = False

            # For all existing lines (qubits)
            for i in range(self.circuit.size):

                top = cir_y + bd + (i * cir_line_height)
                btm = top + cir_line_height

                # Is located in Y drag-n-drop area ?
                if top <= Y < btm:

                    # Which gate is it selecting ?
                    self.selected_gate = int((X - bb) // (cir_line_width / gate_n_per_line))
                    self.selected_line = i
                    IN = True

                    self.circuit.highlight(i, self.selected_gate)

            # Not in Y drag-n-drop area
            if not IN:
                self.selected_line = None
                self.selected_gate = None
                self.circuit.minimize()

        # Not in X drag-n-drop area
        else:
            self.selected_line = None
            self.selected_gate = None
            self.circuit.minimize()

    def on_drop(self, event) -> None:
        """
        Dropping function, calls for gate addition at appropriate location if not outside of range,
        and resets position of the widget.

        :param event: bound event
        """

        # If a line is selected (otherwise outside the frame)
        if self.selected_line is not None:
            self.circuit.add_gate_to_circuit(self.selected_line, self.selected_gate, self)

        self.circuit.minimize()
        self._reset_position()

        self.selected_line = None
