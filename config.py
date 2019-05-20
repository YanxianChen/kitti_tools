import os
import numpy as np
from easydict import EasyDict as edict


__C = edict()
# Consumers can get config by: from config import cfg
cfg = __C

# Root directory of project
__C.ROOT_DIR = os.path.dirname(__file__)
# Data directory
__C.DATA_DIR = os.path.join(__C.ROOT_DIR, 'data')
# Calibration directory
__C.CALIB_DIR = os.path.join(__C.DATA_DIR, 'calib')
# Velodyne points cloud directory
__C.LIDAR_DIR = os.path.join(__C.DATA_DIR, 'velodyne')
# Velodyne points cloud with crop directory
__C.LIDAR_CROP_DIR = os.path.join(__C.DATA_DIR, 'velodyne_crop')
# Image directory
__C.IMAGE_DIR = os.path.join(__C.DATA_DIR, 'image_2')
# Label directory
__C.LABEL_DIR = os.path.join(__C.DATA_DIR, 'label_2')

__C.TRAIN_TYPE = 'velodyne_train'
__C.TEST_TYPE = 'velodyne_test'

# Point cloud range
__C.xrange = (0, 70.4)
__C.yrange = (-40, 40)
__C.zrange = (-3, 1)

