import os


class KittiDataset(object):

    def __init__(self, cfg, set='train'):
        self.root = cfg.ROOT_DIR
