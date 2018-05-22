from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as mcolors

HUE, SATURATION, VALUE = 0, 1, 2

class ColorViewer(object):

    def __init__(self, ax, colormap = None, bin_size = 5, sort_order = [ VALUE, SATURATION, HUE ], transpose = False):

        self.ax = ax

        if colormap is None:
            colormap = mcolors.get_named_colors_mapping()
        rgbvals = dict([ (n, mcolors.to_rgb(c)) for n, c in colormap.iteritems() ])
        colors = dict([ (n, c) for n, c in rgbvals.iteritems() if all([ v != c[0] for v in c[1:] ]) ])
        hsv, names = zip(*sorted([ (tuple(mcolors.rgb_to_hsv(color)), name) for name, color in colors.iteritems() ]))

        groups = { }
        bins = np.arange(0, 360, bin_size) * (1.0 / 360)
        for gr, name in zip(np.digitize([ h for h, s, v in hsv ], bins), names):
            if gr not in groups:
                groups[gr] = [ ]
            groups[gr].append(name)

        self.state = { "selected": None, "background": None }
        self.swatches = [ ]
        self.rgb_to_swatch, self.label_to_swatch = { }, { }

        hue = lambda c: hsv[names.index(c)][0]
        ordered = lambda c: [ hsv[names.index(c)][i] for i in sort_order ]
        max_y = 0

        for x, grp in enumerate(sorted(groups.itervalues(), key = lambda v: hue(v[0]))):
            for y, name in enumerate(sorted(grp, key = lambda n: ordered(n))):
                if transpose:
                    r = plt.Rectangle((y + 0.1, x + 0.1), 0.8, 0.8, color = rgbvals[name])
                else:
                    r = plt.Rectangle((x + 0.1, y + 0.1), 0.8, 0.8, color = rgbvals[name])
                ax.add_artist(r)
                sw = Swatch(r, name, self.state)
                sw.connect()
                self.swatches.append(sw)
                self.rgb_to_swatch[rgbvals[name]] = sw
                self.label_to_swatch[name] = sw
                if y > max_y:
                    max_y = y

        if transpose:
            ax.set_xlim(0, max_y + 1), ax.set_ylim(0, len(groups))
        else:
            ax.set_xlim(0, len(groups)), ax.set_ylim(0, max_y + 1)
        ax.set_axis_off()
        ax.figure.subplots_adjust(left = 0.02, right = 0.98, top = 0.98, bottom = 0.02, hspace = 0, wspace = 0)
        self.state["background"] = ax.get_figure().canvas.copy_from_bbox(ax.bbox)

    def highlight(self, item):

        if isinstance(item, (str, unicode)):
            swatch = self.label_to_swatch[item]
        elif isinstance(item, tuple):
            swatch = self.rgb_to_swatch[item[:3]]
        else:
            raise Exception("Invalid argument: %s" % str(item))

        swatch.select()
        if self.state["selected"] is not None:
            self.state["selected"].deselect()
        self.state["selected"] = swatch

    @property
    def selected(self):
        return tuple(self.state["selected"].rect.get_fc()[:3]) if self.state["selected"] else None

    def selected_with_alpha(self, alpha):
        return tuple(self.state["selected"].rect.get_fc()[:3], alpha) if self.state["selected"] else None

class Swatch(object):

    annotation_props = dict(boxstyle = "square", fc = (0.9, 0.9, 0.9, 1.0), ec = (0.1, 0.1, 0.1, 1.0))

    def __init__(self, r, label, state):

        self.rect = r
        self.label = label
        x, y = r.get_xy()
        x, y = x + r.get_width() / 2, y + r.get_height() / 2
        self.annotation = self.rect.axes.text(x, y, label, bbox = Swatch.annotation_props, visible = False)
        self.state = state

    def connect(self):

        self.cidpress = self.rect.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidmotion = self.rect.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def select(self):

        x, y = self.rect.xy
        color = self.rect.get_fc()
        ax = self.rect.axes
        self.rect.remove()
        r = plt.Rectangle((x, y), 0.8, 0.8, fc = color, ec = (0.0, 0.0, 0.0))
        ax.add_artist(r)
        self.rect = r

    def deselect(self):

        x, y = self.rect.xy
        color = self.rect.get_fc()
        ax = self.rect.axes
        self.rect.remove()
        r = plt.Rectangle((x, y), 0.8, 0.8, color = color)
        ax.add_artist(r)
        self.rect = r

    def on_press(self, event):

        if event.inaxes != self.rect.axes:
            return

        contains, attrd = self.rect.contains(event)
        if contains:
            self.rect.figure.canvas.restore_region(self.state["background"])
            self.annotation.set_visible(False)
            if self.state["selected"] is not None:
                self.state["selected"].deselect()
            self.select()
            self.rect.figure.canvas.blit(self.rect.axes)
            self.state["selected"] = self

        if not contains and self.annotation.get_visible():
            self.rect.figure.canvas.restore_region(self.state["background"])
            self.annotation.set_visible(False)
            self.rect.figure.canvas.blit(self.rect.axes)
            self.annotation.figure.canvas.blit(self.rect.axes)

    def on_motion(self, event):

        if event.inaxes != self.rect.axes:
            return

        contains, attrd = self.rect.contains(event)
        if not contains and self.annotation.get_visible():
            self.rect.figure.canvas.restore_region(self.state["background"])
            self.annotation.set_visible(False)
            self.annotation.figure.canvas.blit(self.rect.axes)
        
        if contains:
            self.rect.figure.canvas.restore_region(self.state["background"])
            self.annotation.set_visible(True)
            self.annotation.figure.canvas.blit(self.rect.axes)

    def disconnect(self):

        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.motion)

