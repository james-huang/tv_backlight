#import ImageGrab
#import time
#from collections import defaultdict
#import ImageTk
#import os
#import PIL.Image
import struct
import glob
import serial
import signal
from time import sleep, time

ARDUINO_PORT = glob.glob("/dev/tty.usbmodem*")[0]
ARDUINO_BAUD_RATE = 9600

import Quartz.CoreGraphics as CG

import Tkinter
from Tkinter import *

class PixelRenderer(Tkinter.Tk):
  """
  This class is a software mockup of Physical LEDS mounted behind a TV.
  The pixel layout is:

  -----------------------------
  |      |      |      |      |
  |______|______|______|______|
  |      |             |      |
  |______|_____________|______|
  |      |      |      |      |
  |______|______|______|______|


  """

  FRAME_RATE_CHECK_INTERVAL_MS = 10*1000
  BORDER_DETECTION_START_BUFFER_MS = 500 #10*1000 #time to wait for a movie to launch
  BORDER_DETECTION_INTERVAL_MS = 10*1000#1000 #10*1000
  BORDER_DETECTION_MAX_TIMES = 8 #20 #times to run border detection at start of movie

  # VLC centers videos vertically slightly differently to shiftit.
  DEBUG_VERTICAL_SHIFT = 0

  def __init__(self, parent):
    print "__init__"
    # TODO (james) : run video.py without tkinter GUI
    # give optional debug flag to turn on GUI?
    Tkinter.Tk.__init__(self, parent)
    self.parent = parent

    self.frame = Tkinter.Frame(self, width=1010, height=610, bg="black")
    self.frame.grid()
    self._init_pixels()
    self.debug_display = Tkinter.Label(self.frame, text="DEBUG DISPLAY",
        width=50, height=5, fg="gray", bg="black")
    self.debug_display.grid(row=1, column=1, columnspan=2)

    self.border_detection_count = 0

    self.arduino_serial = serial.Serial(
      ARDUINO_PORT,
      baudrate=ARDUINO_BAUD_RATE,
      stopbits=serial.STOPBITS_ONE,
      timeout=1,
    )
    print "when a serial port is open the arduino runs reset. sleep 3 sec before sending commands"
    sleep(3)

    """
    screen capture area/smart border dectector (use smallest/mode of border to avoid outliers)
    average pixels
    """

    self.check_refresh_rate_start_seconds = time()
    self.refresh_pixels_count = 0
    self.after(self.FRAME_RATE_CHECK_INTERVAL_MS, self._check_refresh_rate)

    self.cgimage_screen_capture()

    # these bounds are inclusive, and can be indexed
    # TODO this feels hack, clean this up, maybe move border detection to daemon thread
    if False: # TODO: figure out resolution when plugged into TV
      self.left_bound = 0
      self.right_bound = 2879
      self.top_bound = 300
      self.bottom_bound = 1499
    else:
      self.left_bound = 0
      self.right_bound = self.screen_capture_width - 1
      self.top_bound = 0
      self.bottom_bound = self.screen_capture_height - 1
      self.after(self.BORDER_DETECTION_INTERVAL_MS, self.detect_border)

    self.refresh_pixels()

  def _check_refresh_rate(self):
    current_time_seconds = time()
    elapsed_time_seconds = current_time_seconds - self.check_refresh_rate_start_seconds
    refresh_rate = self.refresh_pixels_count / elapsed_time_seconds
    # self.debug_display.configure(text="%s Hz"%refresh_rate)

    self.refresh_pixels_count = 0
    self.check_refresh_rate_start_seconds = current_time_seconds
    self.after(self.FRAME_RATE_CHECK_INTERVAL_MS, self._check_refresh_rate)

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

    s8, top_left_pixel = self.get_pixel(self.left_bound, self.top_bound)
    s7, top_left_center_pixel = self.get_pixel(self.left_bound + (self.right_bound - self.left_bound + 1)/3*1, self.top_bound)
    s6, top_right_center_pixel = self.get_pixel(self.left_bound + (self.right_bound - self.left_bound + 1)/3*2, self.top_bound)
    s5, top_right_pixel = self.get_pixel(self.right_bound, self.top_bound)

    s9, mid_left_pixel = self.get_pixel(self.left_bound, self.top_bound + (self.bottom_bound - self.top_bound + 1)/2)
    s4, mid_right_pixel = self.get_pixel(self.right_bound, self.top_bound + (self.bottom_bound - self.top_bound + 1)/2)

    s0, bottom_left_pixel = self.get_pixel(self.left_bound, self.bottom_bound)
    s1, bottom_left_center_pixel = self.get_pixel(self.left_bound + (self.right_bound - self.left_bound + 1)/3*1, self.bottom_bound)
    s2, bottom_right_center_pixel = self.get_pixel(self.left_bound + (self.right_bound - self.left_bound + 1)/3*2, self.bottom_bound)
    s3, bottom_right_pixel = self.get_pixel(self.right_bound, self.bottom_bound)

    self.top_left.configure(bg="#%s" % top_left_pixel, text=top_left_pixel)
    self.top_left_center.configure(bg="#%s" % top_left_center_pixel, text=top_left_center_pixel)
    self.top_right_center.configure(bg="#%s" % top_right_center_pixel, text=top_right_center_pixel)
    self.top_right.configure(bg="#%s" % top_right_pixel, text=top_right_pixel)

    self.mid_left.configure(bg="#%s" % mid_left_pixel, text=mid_left_pixel)
    self.mid_right.configure(bg="#%s" % mid_right_pixel, text=mid_right_pixel)

    self.bottom_left.configure(bg="#%s" % bottom_left_pixel, text=bottom_left_pixel)
    self.bottom_left_center.configure(bg="#%s" % bottom_left_center_pixel, text=bottom_left_center_pixel)
    self.bottom_right_center.configure(bg="#%s" % bottom_right_center_pixel, text=bottom_right_center_pixel)
    self.bottom_right.configure(bg="#%s" % bottom_right_pixel, text=bottom_right_pixel)

    serial_info = s0 + s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 + "\xff\xff\xff\xff"
    #print "serial_info: ", serial_info
    # print "0 %s"% ' '.join([str(ord(s)) for s in s0])
    # print "1 %s"% ' '.join([str(ord(s)) for s in s1])
    # print "2 %s"% ' '.join([str(ord(s)) for s in s2])
    # print "3 %s"% ' '.join([str(ord(s)) for s in s3])
    # print "4 %s"% ' '.join([str(ord(s)) for s in s4])
    # print "5 %s"% ' '.join([str(ord(s)) for s in s5])
    # print "6 %s"% ' '.join([str(ord(s)) for s in s6])
    # print "7 %s"% ' '.join([str(ord(s)) for s in s7])
    # print "8 %s"% ' '.join([str(ord(s)) for s in s8])
    # print "9 %s"% ' '.join([str(ord(s)) for s in s9])
    self.arduino_serial.write(serial_info)

    self.refresh_pixels_count += 1
    #self.refresh_pixels()
    self.after(30, self.refresh_pixels)# used to be 1
    """
    TODO (james) : i wonder if we can bumpt this down somehow
    maybe ecoding RGB into a single int 4 byte value 0RGB
    (255)RGB indicating last pixel group and flush buffer
    """

  def normalize_pixel(self, pixel_value):
    """
    TODO (james) : screen pixel values dont always correspond to arduino
    pixel values. there might be an out of box library to fix this, otherwise
    need to calibrate pixels manually

    """
    pass

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
    # the tkinter pixels want a RRGGBB hex value string
    # the arduino wants RGB char string
    tkinter_rgb_values = struct.pack('BBB', *(r, g, b)).encode('hex')
    arduino_rgb_values = chr(b) + chr(g) + chr(r) + chr(0)
    return arduino_rgb_values, tkinter_rgb_values

  def detect_border(self):
    """
    When run, this takes the screen, and finds the location of the black bounding box for a video.
    Make sure to set BORDER_DETECTION_START_BUFFER_MS such that refresh_pixels() and
    cgimage_screen_capture() has been called at least once.
    """

    row = self.screen_capture_height / 2
    # find bounding box left side
    for col in xrange(self.screen_capture_width):
      _, tmp_pixel = self.get_pixel(col, row)
      if tmp_pixel != "000000":
        self.left_bound = col
        break

    # find bounding box right side
    for col in xrange(self.screen_capture_width - 1, -1, -1):
      _, tmp_pixel = self.get_pixel(col, row)
      if tmp_pixel != "000000":
        self.right_bound = col
        break

    col = self.screen_capture_width / 2
    # find bounding box top
    for row in xrange(self.screen_capture_height):
      _, tmp_pixel = self.get_pixel(col, row)
      if tmp_pixel != "000000":
        self.top_bound = row
        break

    # find bounding box bottom
    for row in xrange(self.screen_capture_height - 1, -1, -1):
      _, tmp_pixel = self.get_pixel(col, row)
      if tmp_pixel != "000000":
        self.bottom_bound = row
        break

    self.debug_display.configure(text="left_bound:%s right_bound:%s top_bound:%s bottom_bound:%s"%
        (self.left_bound, self.right_bound, self.top_bound, self.bottom_bound))

    self.border_detection_count += 1
    print "self.border_detection_count: ", self.border_detection_count
    print "left_bound:%s right_bound:%s top_bound:%s bottom_bound:%s"%(self.left_bound, self.right_bound, self.top_bound, self.bottom_bound)

    if self.border_detection_count < self.BORDER_DETECTION_MAX_TIMES:
      self.after(self.BORDER_DETECTION_INTERVAL_MS, self.detect_border)

if __name__ == "__main__":
  app = PixelRenderer(None)
  app.title('TV Backlight Debugger')
  app.mainloop()

