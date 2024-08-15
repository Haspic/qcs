
from tkinter import Button
from tkManagementFuncs import bindButtonHover
from dimensions import *


class DragableWidget(Button):

    def _reset_position(self):
        self.place(x=self.x_init, y=self.y_init)

    def __init__(self,
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
        super().__init__(text=gate, bg=bg, **kwargs)

        self.gate = gate
        self.circuit = circuit_frame

        # bind dragging to drag functions
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

        # Move widget
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

                    # Which gate is it selecting ?
                    self.selected_gate = int((X - rb) // (cir_width / circuit_gate_width))
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
            self.circuit.add_gate(self.selected_line, self.selected_gate, self.gate)

        self.circuit.minimize()
        self._reset_position()

        self.selected_line = None

