import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, Size
from matplotlib.axes import Axes
import numpy as np

from colorviewer import *

class ColorPicker(object):

    def __init__(self, ax, cview_args = { }, display_args = { }, colormap = [ ]):

        cview_ax = Axes(ax.get_figure(), ax.get_position(original = True))
        cmap_ax = Axes(ax.get_figure(), ax.get_position(original = True))

        self.ax = ax
        self.cview = ColorViewer(cview_ax, **cview_args)
        self.colormap = MapDisplay(cmap_ax, self.cview, **display_args)
        for name, color in colormap:
            self.colormap.add_item(name, color)

        divider = make_axes_locatable(ax)
        pad = Size.Fixed(0.1)
        colormap_width = Size.Fraction(0.39, Size.AxesX(ax))
        cview_width = Size.Fraction(0.6, Size.AxesX(ax))
        divider.set_horizontal([ colormap_width, pad, cview_width ])

        cmap_ax.set_axes_locator(divider.new_locator(nx = 0, ny = 0))
        ax.figure.add_axes(cmap_ax)

        cview_ax.set_axes_locator(divider.new_locator(nx = 2, ny = 0))
        ax.figure.add_axes(cview_ax)

        ax.tick_params(left = False, bottom = False, labelleft = False, labelbottom = False)
        ax.set_axis_off()

    def add_item(self, name, color):

        self.colormap.add_item(name, color)

    def get_dict(self):

        return dict([ (name, item.rgb) for name, item in self.colormap.colors.iteritems() ])

class MapDisplay(object):

    def __init__(self, ax, cview, font_size = 8, pad = 4):

        self.ax = ax
        ax.tick_params(left = False, bottom = False, labelleft = False, labelbottom = False)
        ax.set_aspect("equal")
        ax.set_anchor("N")

        self.cview = cview

        self.font_size = font_size
        self.row_sz = 1.0 / (self.ax.figure.get_dpi() / (font_size + pad))
        self.rect_height = self.row_sz * 0.8
        self.rect_width = self.rect_height * 1.5

        self.colors = { }

    def add_item(self, name, color = None):

        self.colors[name] = DisplayItem(self, name, color)

class DisplayItem(object):

    def __init__(self, display, name, color = None):

        row = len(display.colors) + 1
        offset_y = 1.0 - (display.row_sz * row)

        if color is None:
            props = { "ec": (0.0, 0.0, 0.0), "fc": (1.0, 1.0, 1.0) }
        else:
            props = { "color": color }

        self.text = display.ax.text(display.rect_width + 0.1, offset_y + (display.row_sz / 2.0), name, va = "center", ha = "left")
        self.rect = plt.Rectangle((0.05, offset_y), display.rect_width, display.rect_height, **props)
        display.ax.add_patch(self.rect)
        display.ax.set_ylim(offset_y - display.row_sz * 0.5, 1.0)
        self.connect()

        self.cview = display.cview

    @property
    def rgb(self):
        return self.rect.get_fc()[:3]

    def set_color(self, color):
        self.rect.set_color(color)

    def on_press(self, event):

        if event.inaxes != self.rect.axes:
            return
        contains, attrd = self.rect.contains(event)
        if not contains:
            return

        if event.button == 1:
            color = self.rgb
            try:
                self.cview.highlight(color)
            except:
                pass
        elif event.button == 3:
            color = self.cview.selected
            if color is not None:
                self.set_color(color)

        self.rect.figure.canvas.draw()

    def connect(self):
        self.cidpress = self.rect.figure.canvas.mpl_connect('button_press_event', self.on_press)

    def disconnect(self):
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)

