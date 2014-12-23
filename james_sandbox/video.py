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

    self.frame = Tkinter.Frame(self, width=1000, height=800, bg="black")
    self.frame.grid()


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
