#import ImageGrab
#import time
#from collections import defaultdict
#import ImageTk
#import os
#import PIL.Image
import struct

import Quartz.CoreGraphics as CG

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
    self._init_pixels()


    # TODO:
    """
    check refresh rate
    average pixels
    screen capture area/smart border dectector

    """

    #self.refresh_pixels()

  def _init_pixels(self):
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

  def refresh_pixels(self):

    self.cgimage_screen_capture()

    top_left_pixel = self.get_pixel(0,0)
    top_left_center_pixel = self.get_pixel(self.screen_capture_width/3*1, 0)
    top_right_center_pixel = self.get_pixel(self.screen_capture_width/3*2, 0)
    top_right_pixel = self.get_pixel(self.screen_capture_width-1, 0)

    mid_left_pixel = self.get_pixel(0, self.screen_capture_height/2)
    mid_right_pixel = self.get_pixel(self.screen_capture_width-1, self.screen_capture_height/2)

    bottom_left_pixel = self.get_pixel(0, self.screen_capture_height-1)
    bottom_left_center_pixel = self.get_pixel(self.screen_capture_width/3*1, self.screen_capture_height-1)
    bottom_right_center_pixel = self.get_pixel(self.screen_capture_width/3*2, self.screen_capture_height-1)
    bottom_right_pixel = self.get_pixel(self.screen_capture_width-1, self.screen_capture_height-1)

    self.top_left.configure(bg="#%s" % top_left_pixel)
    self.top_left_center.configure(bg="#%s" % top_left_center_pixel)
    self.top_right_center.configure(bg="#%s" % top_right_center_pixel)
    self.top_right.configure(bg="#%s" % top_right_pixel)

    self.mid_left.configure(bg="#%s" % mid_left_pixel)
    self.mid_right.configure(bg="#%s" % mid_right_pixel)

    self.bottom_left.configure(bg="#%s" % bottom_left_pixel)
    self.bottom_left_center.configure(bg="#%s" % bottom_left_center_pixel)
    self.bottom_right_center.configure(bg="#%s" % bottom_right_center_pixel)
    self.bottom_right.configure(bg="#%s" % bottom_right_pixel)

    self.after(30, self.refresh_pixels)

  def cgimage_screen_capture(self, region=None):
    """
    inputs
      region: Quartz.CoreGraphics CGRect
    """

    if region is None:
      region = CG.CGRectInfinite
    elif region.size.width % 2 > 0:
      raise ValueError("Capture region width: %s should be even to avoid warp"%region.size.width)

    image = CG.CGWindowListCreateImage(
        region,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault)

    image_get_data_provider = CG.CGImageGetDataProvider(image)
    self.screen_capture_byte_data = CG.CGDataProviderCopyData(image_get_data_provider)

    # Get width/height of image
    self.screen_capture_width = CG.CGImageGetWidth(image)
    self.screen_capture_height = CG.CGImageGetHeight(image)

  def get_pixel(self, x, y):
    """
    Get pixel value at given (x,y) screen coordinates

    Must call cgimage_screen_capture() first.
    """

    # Pixel data is unsigned char (8bit unsigned integer) (blue,green,red,alpha)
    data_format = 'BBB'

    # Calculate offset, based on http://www.markj.net/iphone-uiimage-pixel-color/
    offset = 4 * ((self.screen_capture_width*int(round(y))) + int(round(x)))

    # Unpack data from string into Python'y integers
    b, g, r = struct.unpack_from(data_format, self.screen_capture_byte_data, offset=offset)

    # Return BGRA as RGBA
    return struct.pack('BBB', *(r, g, b)).encode('hex')


if __name__ == "__main__":
  app = PixelRenderer(None)
  app.title('TV Backlight Debugger')
  app.mainloop()

