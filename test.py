from config import cfg
from threading import Thread
from kitti import KittiDataset
from visualization import vis_points
from load_points import load_kitti_velodyne, get_filtered_lidar, kitti_velo_to_cam


dataset = KittiDataset(cfg)
index = dataset._load_index()
print(len(index), type(index))
print(index)
print(dataset.label_path_at(5))
print(dataset.lidar_path_at(5))
print(dataset.image_path_at(5))
print(dataset.calib_path_at(5))

origin = load_kitti_velodyne(dataset.lidar_path_at(5))
crop = get_filtered_lidar(origin)
# vis_mayavi(origin)
xyzi = kitti_velo_to_cam(origin, dataset.calib_path_at(5))

vis_points(xyzi)