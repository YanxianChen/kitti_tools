import os


class KittiDataset(object):

    def __init__(self, cfg, set='train'):
        self._cfg = cfg
        self._set = set
        self._index = self._load_index()
        self._image_ext = '.png'

    # load the index of data from a prepare txt format file
    def _load_index(self):
        set_file = os.path.join(self._cfg.DATA_DIR, 'splits', self._set + '.txt')
        assert os.path.exists(set_file), 'Path does not exists: {}'.format(set_file)
        with open(set_file) as f:
            index = [x.strip() for x in f.readlines()]
        return index

    def image_path_at(self, i):
        """
        Return the absolute path to image i in the image sequence.
        """
        return self.image_path_from_index(self._index[i])

    def image_path_from_index(self, index):
        """
        Construct an image path from the image's "index" identifier.
        """
        image_path = os.path.join(self._cfg.IMAGE_DIR, index + '.png')
        assert os.path.exists(image_path), 'Path does not exist: {}'.format(image_path)
        return image_path

    def calib_path_at(self, i):
        return self.calib_path_from_index(self._index[i])

    def calib_path_from_index(self, index):
        file_path = os.path.join(self._cfg.CALIB_DIR, index + '.txt')
        assert os.path.exists(file_path), 'Path does not exist: {}'.format(file_path)
        return file_path

    def lidar_path_at(self, i, crop=True):
        return self.lidar_path_from_index(self._index[i], crop)

    def lidar_path_from_index(self, index, crop=True):
        if crop:
            file_path = os.path.join(self._cfg.LIDAR_CROP_DIR, index + '.bin')
        else:
            file_path = os.path.join(self._cfg.LIDAR_DIR, index + '.bin')
        assert os.path.exists(file_path), 'Path does not exist: {}'.format(file_path)
        return file_path

    def label_path_at(self, i):
        return self.lidar_path_from_index(self._index[i])

    def label_path_from_index(self, index):
        file_path = os.path.join(self._cfg.LABEL_DIR, index + '.txt')
        assert os.path.exists(file_path), 'Path does not exist: {}'.format(file_path)
        return file_path
