from bokeh.io import vplot
from bokeh.models import Range
from bokeh.plotting import figure, show
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_plane(orb, plane='XY', show_steps=True, show_plot=True, width=500, height=500):
    r = orb.s0.body.mean_radius.value
    x, y, z = np.array(orb.rx), np.array(orb.ry), np.array(orb.rz)
    if plane == 'XY':
        x, y, z = x, y, z
        x0 = orb.s0.r[0].value
        y0 = orb.s0.r[1].value
        if orb.interpolate:
            xs = orb._states[0,:]
            ys = orb._states[1,:]
    elif plane == 'XZ':
        x, y, z = x, z, y
        x0 = orb.s0.r[0].value
        y0 = orb.s0.r[2].value
        if orb.interpolate:
            xs = orb._states[0,:]
            ys = orb._states[2,:]
    elif plane == 'YZ':
        x, y, z = y, z, x
        x0 = orb.s0.r[1].value
        y0 = orb.s0.r[2].value
        if orb.interpolate:
            xs = orb._states[1,:]
            ys = orb._states[2,:]

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
    nan = float('nan')
    x_bg = x.copy()
    y_bg = y.copy()
    x_fg = x.copy()
    y_fg = y.copy()
    x_bg[~ind] = nan
    y_bg[~ind] = nan
    x_fg[ind] = nan
    y_fg[ind] = nan
    f.circle(x=0, y=0, radius=r, alpha=0.5)
    f.line(x_fg, y_fg, line_width=2, color='blue')
    f.circle(x_bg, y_bg, size=2, color='darkblue')
    if orb.interpolate and show_steps:
        f.cross(x=xs, y=ys, size=15, line_width=2, color='darkblue')
    f.cross(x=x0, y=y0, size=15, line_width=2, color='red')
    f.x(x=x[-1], y=y[-1], size=12, line_width=3, color='purple')
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



