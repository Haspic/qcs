
from tkinter import Button


def PASS():
    pass

def bindButtons(slide_widgets: list, **kwargs) -> None:
    """ Binds all buttons given in widget list """
    for widget, _, _ in slide_widgets:
        if isinstance(widget, Button):
            bindButtonHover(widget, **kwargs)

def bindButtonHover(button, cl_enter="gold", cl_leave="steelblue3") -> None:
    """ Configure given button, in order for it to change color when the mouse hovers over it """
    # mouse hover
    button.bind("<Enter>", lambda i: button.config(bg=cl_enter))  # #999999
    # mouse leaves hover
    button.bind("<Leave>", lambda i: button.config(bg=cl_leave))  # #F0F0F0

def buildFrame(frame_widgets: list) -> None:
    """ Builds frame from given widget list (order matters) """
    for widget, method, kwargs in frame_widgets:

        match method:

            case "pack":
                widget.pack(**kwargs)
            case "grid":
                widget.grid(**kwargs)
            case "place":
                widget.place(**kwargs)

def eraseFrame(frame_widgets: list) -> None:
    """ Erase frame from given widget list """
    for widget, method, kwargs in frame_widgets:

        match method:

            case "pack":
                widget.pack_forget()
            case "grid":
                widget.grid_forget()
            case "place":
                widget.place_forget()
