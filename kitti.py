import os


class KittiDataset(object):

    def __init__(self, cfg, set='sub_train'):
        self._cfg = cfg
        self._set = set
        self._index = self._load_index()

    def _load_index(self):
        """
        load the index of data from a prepare txt format file
        :return: a index list
        """
        set_file = os.path.join(self._cfg.DATA_DIR, 'splits', self._set + '.txt')
        assert os.path.exists(set_file), 'Path does not exists: {}'.format(set_file)
        with open(set_file) as f:
            index = [x.strip() for x in f.readlines()]
        return index

    def image_path_at(self, i):
        """
        Return the absolute path to image i in the image sequence.
        :return: a prefix string
        """
        return self.image_path_from_index(self._index[i])

    def image_path_from_index(self, index):
        """
        Construct an image path from the image's "index" identifier.
        :return: a path
        """
        image_path = os.path.join(self._cfg.IMAGE_DIR, index + '.png')
        assert os.path.exists(image_path), 'Path does not exist: {}'.format(image_path)
        return image_path

    def calib_path_at(self, i):
        return self.calib_path_from_index(self._index[i])

    def calib_path_from_index(self, index):
        calib_path = os.path.join(self._cfg.CALIB_DIR, index + '.txt')
        assert os.path.exists(calib_path), 'Path does not exist: {}'.format(calib_path)
        return calib_path

    def lidar_path_at(self, i, crop=False):
        return self.lidar_path_from_index(self._index[i], crop)

    def lidar_path_from_index(self, index, crop=False):
        # Dispatch to cropped point cloud or origin point cloud
        if crop:
            lidar_path = os.path.join(self._cfg.LIDAR_CROP_DIR, index + '.bin')
        else:
            lidar_path = os.path.join(self._cfg.LIDAR_DIR, index + '.bin')
        assert os.path.exists(lidar_path), 'Path does not exist: {}'.format(lidar_path)
        return lidar_path

    def label_path_at(self, i):
        return self.label_path_from_index(self._index[i])

    def label_path_from_index(self, index):
        label_path = os.path.join(self._cfg.LABEL_DIR, index + '.txt')
        assert os.path.exists(label_path), 'Path does not exist: {}'.format(label_path)
        return label_path
