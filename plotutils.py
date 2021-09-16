import itertools

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import lines
import numpy as np


def _get_labels(style):
    labels = "abcdefghijklmnopqrstuvwxyz"
    if style == "lowercase":
        return labels
    elif style == "uppercase":
        return labels.upper()
    else:
        raise ValueError(f"Unknown style '{style}'")
    

class Background():
    """
    Background axes for Matplotlib figures, which can be used for layouting (when visible=True)
    and for plotting various annotations and markers that do not belong to any specific subplot.
    """
    
    
    def __init__(self, fig=None, visible=False, spacing=0.1, linecolor='0.5', linewidth=1):
        """
        Args:
            fig:             Matplotlib figure. If None, the current one is used.
            visible (bool):  Show the grid if True. 
            spacing:         Spacing of the background grid. Irrelevant if visible=False.
            linecolor:       Default color of added lines.
            linewidth:       Default width of added lines.
        """
        
        if fig is not None:
            plt.scf(fig)
        ax = plt.axes([0,0,1,1], facecolor=None, zorder=-1000)
        plt.xticks(np.arange(0, 1 + spacing/2., spacing))
        plt.yticks(np.arange(0, 1 + spacing/2., spacing))
        plt.grid()
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        ax.autoscale(False)
        if not visible:
            plt.axis('off')
        self.axes = ax
        self.linecolor = linecolor
        self.linewidth = linewidth

    def vline(self, x, y0=0, y1=1, **args):
        "Place a vertical line at position x spanning between y0 and y1."
        
        defargs = dict(color=self.linecolor, linewidth=self.linewidth)
        defargs.update(args)
        self.axes.add_line(lines.Line2D([x, x], [y0, y1], **defargs))

    def hline(self, y, x0=0, x1=1, **args):
        "Place a horizontal line at position y spanning between x0 and x1."
        
        defargs = dict(color=self.linecolor, linewidth=self.linewidth)
        defargs.update(args)
        self.axes.add_line(lines.Line2D([x0, x1], [y, y], **defargs))
        
    def box(self, pos, title=None, titlestyle=None, pad=0.0, **args):
        """Draw a box with optional title.
        
        Args:
            pos:         (left, right, bottom, top) axes coordinates.
            title:       Optional box title.
            titlestyle:  Dict with arguments passed to plt.text().
            pad:         Padding size in axes coordinates.
        """

        plt.sca(self.axes)
        width = pos[1] - pos[0]
        height = pos[3] - pos[2]
        
        defargs = dict(ec=self.linecolor, linewidth=self.linewidth, fc='none')
        defargs.update(args)
        
        fancy = matplotlib.patches.FancyBboxPatch((pos[0], pos[2]), width, height,
                                                  boxstyle=f"round,pad={pad}", **defargs)
        self.axes.add_patch(fancy)

        if title:
            titleargs = dict(ha='left', va='center', backgroundcolor='w',
                             color=self.linecolor, fontsize=12)
            if titlestyle is not None:
                titleargs.update(titlestyle)
            
            plt.text(pos[0]+0.02, pos[3]+pad, title, **titleargs)
            
            
    def add_labels(self, xs, ys, fontsize=18, style="uppercase", labels=None):
        """Place panel labels at positions given by x-coordinates and y-coordinates.
        
        Args:
            xs:       x-coordinates of lower left corner of the labels.
            ys:       y-coordinates of lower left corner of the labels.
            fontsize: Font size.
            style:    Either 'uppercase' or 'lowercase'.
            labels:   If provided, these labels are used. Overrides style.
        """
        
        if labels is None:
            labels = _get_labels(style)
        
        assert len(xs) == len(ys)
        for x, y, label in zip(xs, ys, labels):
            self.axes.text(x, y, label, transform=self.axes.transAxes, size=fontsize, 
                           weight='bold', ha='left', va='bottom')


def add_panel_labels(fig=None, axes=None, fontsize=18, xs=-0.05, ys=1.05, style='uppercase', labels=None):
    """Place panel labels to given (or all) axes, relative to their upper left corner.
    
    Args:
        fig:       Matplotlib figure. If None, the current one is used.
        axes:      Axes to which place the labels. If None, all axes in fig are used.
        fontsize:  Font size.
        xs:        x-coordinate(s) of the label lower left corners. In axes coordinates.
                   Can be either float (then used for all axes), or list of floats, one for every axes.
        ys:        y-coordinate(s) of the label lower left corners. In axes coordinates.
                   Can be either float (then used for all axes), or list of floats, one for every axes.
        style:    Either 'uppercase' or 'lowercase'.
        labels:   If provided, these labels are used. Overrides style.
    """

    if labels is None:
        labels = _get_labels(style)

    if fig is None:
        fig = plt.gcf()

    if axes is None:
        axes = fig.get_axes()

    if not hasattr(xs, '__iter__'):
        xs = itertools.repeat(xs)
    if not hasattr(ys, '__iter__'):
        ys = itertools.repeat(ys)

    for i, (ax, x, y) in enumerate(zip(axes, xs, ys)):
        ax.text(x, y, labels[i], transform=ax.transAxes, size=fontsize,
                weight='bold', ha='left', va='bottom')


def axtext(ax, text, **args):
    """Place text in the middle of given axes, and remove everything else.
    
    Occasionaly useful for placing labels of subplot grids. 
    """
    
    defargs = {'fontsize': 12, 'ha': 'center', 'va': 'center'}
    defargs.update(args)
    plt.sca(ax)
    plt.text(0.5, 0.5, text, **defargs)
    plt.xlim([0, 1]); plt.ylim([0, 1])
    plt.axis('off')


def bottomleft_spines(ax):
    """Hide the right and top spines."""
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
