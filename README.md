# Simple color picker for matplotlib

Groups colors based on HSV and plots swatches in a matplotlib figure.  Allows assignment of colors to a list of values in a legend-like container.

## Color Picker Usage

```
from colorpicker import *
items = [
    ("item 1", "xkcd:spruce"),
    ("item 2", "xkcd:dark mint green"),
    ("item 3", "xkcd:spearmint"),
    ("item 4", None),
]
fig, ax = plt.subplots()
cp = ColorPicker(ax, { "transpose": True }, { "font_size": 8, "pad": 4 }, items)
```

Add additional items:

```
cp.add_item("item 5", None)
```

Left click the item's rectangle to highlight the patch in the color display (if not None).
Right click to assign the currently selected color in the display.

To get a dictionary of currently assigned colors:

```
cp.get_dict()
```

## Color Viewer Usage

To use only the right half (color display):

```
from colorviewer import *
fig, ax = plt.subplots()
cview = ColorViewer(ax)
```

Hover over a color to see the name; click on the color to select it.

```
cview.selected
```

returns the RGBA value of the currently selected color.

### Optional arguments

#### named color mapping
The default is any named color defined in matplotlib.colors.  You can also use one of the more specific mpl named color sets, or create your own dictionary of name -> hex values.

#### bin_size
Size of group, in degrees (corresponding to hue value if plotted in polar coordinates).  The default is 5.

#### sort_order
Within group sort parameter.  I like darker colors to appear at the bottom to the extent possible, so the default sort order is reversed; for strict HSV sorting, use [ 0, 1, 2 ].

## Caveats

No documentation other than this file, error handling, or tests; sorry.

I made this because I need lots of colors organized by hue (for qualitative groups) as well as saturation/value (for subgroups) for a project I'm working on and was frustrated with the lack of organization of the colors on https://xkcd.com/color/rgb/ (all of these colors are available as named colors in mpl).
