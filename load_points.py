import os
import numpy as np
from config import cfg


def load_kitti_velodyne(velo_path):
    points=np.fromfile(velo_path, dtype=np.float32).reshape(-1, 4)


def get_filtered_lidar(lidar, boxes3d=None):
    pxs = lidar[:, 0]
    pys = lidar[:, 1]
    pzs = lidar[:, 2]

    filter_x = np.where((pxs >= cfg.xrange[0]) & (pxs < cfg.xrange[1]))[0]
    filter_y = np.where((pys >= cfg.yrange[0]) & (pys < cfg.yrange[1]))[0]
    filter_z = np.where((pzs >= cfg.zrange[0]) & (pzs < cfg.zrange[1]))[0]
    filter_xy = np.intersect1d(filter_x, filter_y)
    filter_xyz = np.intersect1d(filter_xy, filter_z)

    return lidar[filter_xyz]
