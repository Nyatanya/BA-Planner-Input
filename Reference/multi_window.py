from tkinter import Toplevel, Canvas, Tk, Button, Label
from collections.abc import Callable
from typing import TypeVar
from sys import platform

class FloatingWindow():
    def __init__(self) -> None:
        self.window = Toplevel()
        if platform == "darwin":
            self.window.overrideredirect(1)
            self.window.overrideredirect(0)
        else:
            self.window.overrideredirect(1)

        self.label = Label(self.window)
        self.label.pack(fill="both", expand=True)

        self.label.bind('<Configure>', self.label_resize)
        self.label.bind("<ButtonPress-1>", self.drag_start)
        self.label.bind("<ButtonRelease-1>", self.drag_stop)
        self.label.bind("<B1-Motion>", self.drag_motion)

    def get(self) -> Toplevel:
        return self.window

    def label_resize(self, event):
        width = event.width
        height = event.height

    def drag_start(self, event):
        self.x = event.x
        self.y = event.y

    def drag_stop(self, event):
        self.x = None
        self.y = None

    def drag_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry('+%d+%d' % (x, y))

class Coordinate2D:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.xy = (x, y)
        self.yx = (y, x)

class ScannerWidget:
    def __init__(self, x: int, y: int, h: int = 100, w: int = 100, pad: int = 20) -> None:
        self.win1 = Toplevel()
        self.win2 = Toplevel()
        self.win3 = Toplevel()
        self.win4 = Toplevel()

        self.win1.geometry('%dx%d+%d+%d' % (w-pad, pad, x+pad, y))
        self.win2.geometry('%dx%d+%d+%d' % (w-(2*pad), pad, x+pad, y+h-pad))
        self.win3.geometry('%dx%d+%d+%d' % (pad, h-pad, x, y+pad))
        self.win4.geometry('%dx%d+%d+%d' % (pad, h-(2*pad), x+w-pad, y+pad))

        self._do4win(self._win_prep)

        self.left_top = Coordinate2D(x, y)

    def _move(self, win: Toplevel, x: int, y: int) -> None:
        win.geometry('+%d+%d' % (win.winfo_x() + x, win.winfo_y() + y))

    def _do4win(self, method: Callable[[], TypeVar("T")] = None, *args) -> None:
        method(self.win1, *args)
        method(self.win2, *args)
        method(self.win3, *args)
        method(self.win4, *args)

    def _win_prep(self, win) -> None:
        if platform == "darwin":
            win.overrideredirect(1)
            win.overrideredirect(0)
        else:
            win.overrideredirect(1)

        label = Label(win)
        label.pack(fill="both", expand=True)

        label.bind('<Configure>', self._label_resize)
        label.bind("<ButtonPress-1>", self._drag_start)
        label.bind("<ButtonRelease-1>", self._drag_stop)
        label.bind("<B1-Motion>", self._drag_motion)
    
    def _label_resize(self, event):
        width = event.width
        height = event.height

    def _drag_start(self, event):
        self.x = event.x
        self.y = event.y

    def _drag_stop(self, event):
        self.x = None
        self.y = None

    def _drag_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self._do4win(self._move, deltax, deltay)

    def move(self, x: int, y: int) -> None:
        self._do4win(self._move, x, y)
    
    def position(self, x: int, y: int) -> None:
        x -= self.left_top.x
        y -= self.left_top.y
        self._do4win(self._move, x, y)

    def position_from_center(self, x: int, y: int) -> None:
        x = x - self.win2.winfo_x + (self.win2.winfo_width() / 2)
        y = y - self.win4.winfo_x + (self.win4.winfo_width() / 2)
        self._do4win(self._move, x, y)

def get_all_window():
    print('Root')
    print(ROOT.winfo_x(), ' and ', ROOT.winfo_y(), '\n')
    for k, v in ROOT.children.items():
        if isinstance(v, Toplevel):
            print(k,' and ', v)
            print(v.winfo_x(), ' and ', v.winfo_y())
            print(v.winfo_width(), ' and ', v.winfo_height(), '\n')
    
HEIGHT = 300
WIDTH = 500

ROOT = Tk()
ROOT.title("Python Guides")
canvas = Canvas(ROOT, height=HEIGHT, width=WIDTH)
canvas.pack()

button = Button(ROOT, text="Click ME", bg='White', fg='Black',
                              command=lambda: get_all_window())

a = ScannerWidget(500, 400)

button.pack()
ROOT.mainloop()