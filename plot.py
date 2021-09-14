import itertools

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import lines
import numpy as np


class Background():
    def __init__(self, fig=None, visible=False, spacing=0.1, linecolor='0.5', linewidth=1):
        if fig is not None:
            plt.scf(fig)
        ax = plt.axes([0,0,1,1], facecolor=None, zorder=-1000)
        plt.xticks(np.arange(0, 1 + spacing/2., spacing))
        plt.yticks(np.arange(0, 1 + spacing/2., spacing))
        plt.grid()
        if not visible:
            plt.axis('off')
        self.axes = ax
        self.linecolor = linecolor
        self.linewidth = linewidth

    def vline(self, x, y0=0, y1=1, **args):
        defargs = dict(color=self.linecolor, linewidth=self.linewidth)
        defargs.update(args)
        self.axes.add_line(lines.Line2D([x, x], [y0, y1], **defargs))

    def hline(self, y, x0=0, x1=1, **args):
        defargs = dict(color=self.linecolor, linewidth=self.linewidth)
        defargs.update(args)
        self.axes.add_line(lines.Line2D([x0, x1], [y, y], **defargs))
        
    def labels(self, xs, ys, fontsize=18):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        assert len(xs) == len(ys)
        for x, y, letter in zip(xs, ys, letters):
            self.axes.text(x, y, letter, transform=self.axes.transAxes, size=fontsize, 
                           weight='bold', ha='left', va='bottom')


def add_panel_letters(fig, axes=None, fontsize=18, xpos=-0.04, ypos=1.05):
    labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if axes is None:
        axes = fig.get_axes()

    if type(xpos) == float:
        xpos = itertools.repeat(xpos)
    if type(ypos) == float:
        ypos = itertools.repeat(ypos)

    for i, (ax, x, y) in enumerate(zip(axes, xpos, ypos)):
        ax.text(x, y, labels[i],
                transform=ax.transAxes, size=fontsize, weight='bold')


def axtext(ax, text, **args):
    defargs = {'fontsize': 14, 'ha': 'center', 'va': 'center'}
    defargs.update(args)
    plt.text(0.5, 0.5, text, **defargs)
    plt.xlim([0, 1]); plt.ylim([0, 1])
    plt.axis('off')


def box_rounded(ax, pos, title=None, pad=0.0):
    """Draw a box with rounded corner around a gridspec
    pos: (left, right, bottom, top)
    """

    plt.sca(ax)
    width = pos[1]-pos[0]
    height = pos[3]-pos[2]
    fancy = matplotlib.patches.FancyBboxPatch((pos[0], pos[2]), width, height,
                                              fc='none', ec='0.4', boxstyle=f"round,pad={pad}")
    ax.add_patch(fancy)

    if title:
        plt.text(pos[0]+0.02, pos[3]+pad, title, ha='left', va='center', backgroundcolor='w',
                 color='0.4', fontsize=8)


def axbottomleft(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
