# Simple color picker for matplotlib

Groups colors based on HSV and plots swatches in a matplotlib figure.

## Basic Usage
```
from colorpicker import *
fig = plt.figure()
cview = ColorViewer(fig)
```

Hover over a color to see the name; click on the color to select it.

```
cview.selected
```

returns the RGBA value of the currently selected color.

## Optional arguments

#### named color mapping
The default is any named color defined in matplotlib.colors.  You can also use one of the more specific mpl named color sets, or create your own dictionary of name -> hex values.

#### bin_size
Size of group, in degrees (corresponding to hue value if plotted in polar coordinates).  The default is 5.

#### sort_order
Within group sort parameter.  I like darker colors to appear at the bottom to the extent possible, so the default sort order is reversed; for strict HSV sorting, use [ 0, 1, 2 ].

## Caveats

No documentation other than this file, error handling, or tests; sorry.

I made this because I need lots of colors organized by hue (for qualitative groups) as well as saturation/value (for subgroups) for a project I'm working on and was frustrated with the lack of organization of the colors on https://xkcd.com/color/rgb/ (all of these colors are available as named colors in mpl).
