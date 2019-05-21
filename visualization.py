import numpy as np
import mayavi.mlab as mlab


def vis_points(points, vals="distance"):
    x = points[:, 0]  # x position of point
    y = points[:, 1]  # y position of point
    z = points[:, 2]  # z position of point
    r = points[:, 3]  # reflectance value of point
    d = np.sqrt(x ** 2 + y ** 2)  # Map Distance from sensor

    if vals == "height":
        col = z
    else:
        col = d

    # set the background color and window size
    fig = mlab.figure(bgcolor=(0, 0, 0), size=(1280, 720))
    mlab.points3d(x, y, z,
                  # col,  # Values used for Color
                  r,
                  mode="point",
                  colormap='spectral',  # 'bone', 'copper', 'gnuplot', 'spectral'
                  # color=(0, 1, 0),   # Used a fixed (r,g,b) instead
                  figure=fig,
                  )
    mlab.show()
