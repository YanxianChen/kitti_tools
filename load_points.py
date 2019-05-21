import os
import cv2
import numpy as np
import mayavi.mlab as mlab
from config import cfg


def load_kitti_velodyne(velo_path):
    points = np.fromfile(velo_path, dtype=np.float32).reshape(-1, 4)
    print(len(points))
    return points


def get_filtered_lidar(lidar, boxes3d=None):
    pxs = lidar[:, 0]
    pys = lidar[:, 1]
    pzs = lidar[:, 2]

    filter_x = np.where((pxs >= cfg.xrange[0]) & (pxs < cfg.xrange[1]))[0]
    filter_y = np.where((pys >= cfg.yrange[0]) & (pys < cfg.yrange[1]))[0]
    filter_z = np.where((pzs >= cfg.zrange[0]) & (pzs < cfg.zrange[1]))[0]
    filter_xy = np.intersect1d(filter_x, filter_y)
    filter_xyz = np.intersect1d(filter_xy, filter_z)
    print(len(lidar[filter_xyz]))
    return lidar[filter_xyz]


def kitti_velo_to_cam(xyzi, calib_path, front_only=True):
    if not os.path.exists(calib_path):
        calib_tracking_path = calib_path[:-11] + '.txt'
        with open(calib_tracking_path, 'r') as f:
            lines = f.readlines()
    else:
        with open(calib_path, 'r') as f:
            lines = f.readlines()

    R0 = np.array([float(x) for x in lines[4].strip().split(' ')[1:10]])
    R0_rect = np.eye(4, dtype=np.float32)
    R0_rect[:3, :3] = R0.reshape(3, 3)
    Tr_velo_to_cam = np.array([float(x) for x in lines[5].strip().split(' ')[1:]]).reshape(3, 4)
    Tr_velo_to_cam = np.vstack((Tr_velo_to_cam, \
                                np.array([0, 0, 0, 1], dtype=np.float32)))
    P_velo_to_rect = R0_rect.dot(Tr_velo_to_cam)
    if front_only:
        P2 = np.array([float(x) for x in lines[2].strip().split(' ')[1:]]).reshape(3, 4)
        P_velo_to_img = P2.dot(P_velo_to_rect)

        # remove all points behind image plane (approximation)
        xyzi = xyzi[xyzi[:, 0] >= 3.0]

        # project to image plane, uv: 2xN
        uv = project_to_image(xyzi[:, :3].transpose(), P_velo_to_img)

        # keep points within image viewpoint
        im_path = calib_path.replace('calib', 'image_2')[:-4] + '.png'
        if not os.path.exists(im_path):
            im_path = calib_path.replace('calib', 'image_02')[:-4] + '.png'
        im_shape = cv2.imread(im_path).shape
        uv = np.round(uv)
        keep = (uv[0, :] >= 0) & (uv[1, :] >= 0) & \
               (uv[0, :] < im_shape[1]) & (uv[1, :] < im_shape[0])
        xyzi = xyzi[keep]

    # project to rectified camera 0, x: right, y: down, z: forward
    xyz = P_velo_to_rect.dot(np.vstack((xyzi[:, :3].transpose(), \
                                        np.ones((1, xyzi.shape[0]), dtype=np.float32))))
    xyzi[:, :3] = xyz[:3, :].transpose()
    print(len(xyzi))
    return xyzi


def project_to_image(xyz, P):
    """
    Input
        xyz:    3xN array
        P:      3x4 projection matrix
    Return
        uv      2xN array
    """
    uv = P.dot(np.vstack((xyz, np.ones((1, xyz.shape[1]), dtype=np.float32))))
    uv[:2] = uv[:2] / uv[2]
    return uv[:2]


