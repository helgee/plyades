from bokeh.io import vplot
from bokeh.models import Range
from bokeh.plotting import figure, show
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_plane(orb, plane='XY', show_plot=True, width=500, height=500):
    r = orb.s0.body.mean_radius.value
    x, y, z = np.array(orb.rx), np.array(orb.ry), np.array(orb.rz)
    if plane == 'XY':
        x, y, z = x, y, z
        x0 = orb.s0.r[0].value
        y0 = orb.s0.r[1].value
        if orb.states is not None:
            xs = orb.states[0,:]
            ys = orb.states[1,:]
    elif plane == 'XZ':
        x, y, z = x, z, y
        x0 = orb.s0.r[0].value
        y0 = orb.s0.r[2].value
        if orb.states is not None:
            xs = orb.states[0,:]
            ys = orb.states[2,:]
    elif plane == 'YZ':
        x, y, z = y, z, x
        x0 = orb.s0.r[1].value
        y0 = orb.s0.r[2].value
        if orb.states is not None:
            xs = orb.states[1,:]
            ys = orb.states[2,:]

    magnitudes = np.sqrt(np.square(x)+np.square(y))
    limit = np.maximum(r, magnitudes.max()) * 1.2
    f = figure(
        height = height,
        width = width,
        title = plane,
        x_range = (-limit, limit),
        y_range = (-limit, limit),
    )
    ind = (magnitudes < r) & (z < 0)
    start = -np.flatnonzero(ind)[0]
    x_bg = x[ind]
    y_bg = y[ind]
    x_fg = x[~ind]
    y_fg = y[~ind]
    x_bg = np.roll(x_bg, start)
    y_bg = np.roll(y_bg, start)
    x_fg = np.roll(x_fg, start)
    y_fg = np.roll(y_fg, start)
    f.line(x_fg, y_fg, line_width=2, color='darkblue')
    f.circle(x=0, y=0, radius=r, alpha=0.5)
    f.circle(x_bg, y_bg, size=2, color='darkblue')
    if orb.states is not None:
        f.diamond(x=xs, y=ys, size=10, color='darkblue')
    f.diamond(x=x0, y=y0, size=15, color='purple')
    if show_plot:
        show(f)
    else:
        return f


def plot3d(orb, show_plot=True):
    fig = plt.figure("Plyades Plot", figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    orb.s0.body.plot3d(ax)
    ax.plot(orb.rx, orb.ry, zs=orb.rz, color="r")

    if show_plot:
        plt.show()
    else:
        return ax



