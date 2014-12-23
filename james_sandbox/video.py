#import ImageGrab
#import time
#from collections import defaultdict
#import ImageTk
#import os
#import PIL.Image

import Tkinter
from Tkinter import *

class PixelRenderer(Tkinter.Tk):
  """
  This class is a software mockup of Physical LEDS mounted behind a TV.
  THe pixel layout is:

  -----------------------------
  |      |      |      |      |
  |______|______|______|______|
  |      |             |      |
  |______|_____________|______|
  |      |      |      |      |
  |______|______|______|______|


  """

  def __init__(self, parent):
    print "__init__"
    Tkinter.Tk.__init__(self, parent)
    self.parent = parent

    self.frame = Tkinter.Frame(self, width=1010, height=610, bg="black")
    self.frame.grid()

    self.top_left = Tkinter.Label(self.frame, text="TOPLEFT",
        width=25, height=5, fg="gray", bg="red")
    self.top_left.grid(row=0, column=0)

    self.top_left_center = Tkinter.Label(self.frame, text="TOPLEFTCENTER",
        width=25, height=5, fg="gray", bg="blue")
    self.top_left_center.grid(row=0, column=1)

    self.top_right_center = Tkinter.Label(self.frame, text="TOPRIGHTCENTER",
        width=25, height=5, fg="gray", bg="green")
    self.top_right_center.grid(row=0, column=2)

    self.top_right = Tkinter.Label(self.frame, text="TOPRIGHT",
        width=25, height=5, fg="gray", bg="yellow")
    self.top_right.grid(row=0, column=3)

    self.mid_left = Tkinter.Label(self.frame, text="MIDLEFT",
        width=25, height=5, fg="gray", bg="purple")
    self.mid_left.grid(row=1, column=0)

    self.mid_right = Tkinter.Label(self.frame, text="MIDRIGHT",
        width=25, height=5, fg="gray", bg="pink")
    self.mid_right.grid(row=1, column=3)

    self.bottom_left = Tkinter.Label(self.frame, text="BOTTOMLEFT",
        width=25, height=5, fg="gray", bg="red")
    self.bottom_left.grid(row=2, column=0)

    self.bottom_left_center = Tkinter.Label(self.frame, text="BOTTOMLEFTCENTER",
        width=25, height=5, fg="gray", bg="blue")
    self.bottom_left_center.grid(row=2, column=1)

    self.bottom_right_center = Tkinter.Label(self.frame, text="BOTTOMRIGHTCENTER",
        width=25, height=5, fg="gray", bg="green")
    self.bottom_right_center.grid(row=2, column=2)

    self.bottom_right = Tkinter.Label(self.frame, text="BOTTOMRIGHT",
        width=25, height=5, fg="gray", bg="yellow")
    self.bottom_right.grid(row=2, column=3)

    #self.top_right.configure(bg='#000000')


if __name__ == "__main__":
    app = PixelRenderer(None)
    app.title('TV Backlight Debugger')
    app.mainloop()

#time.clock()
#image = ImageGrab.grab()
#for y in range(0, 100, 10):
#    for x in range(0, 100, 10):
#        color = image.getpixel((x, y))
#print(time.clock())
