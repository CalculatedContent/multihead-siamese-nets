from data import data_loader
import numpy as np


class Dataset:

    def __init__(self, data_fn: str, num_tests: int):
        self.num_tests = num_tests
        self.sen1, self.sen2, self.labels, self.max_doc_len, self.vocabulary_size = data_loader.load_snli(data_fn)
        self.__shuffle_train_idxs = range(len(self.labels) - num_tests)
        self.train_sen1 = self.sen1[:-self.num_tests]
        self.train_sen2 = self.sen2[:-self.num_tests]

    def train_instances(self, shuffle=False):
        if shuffle:
            self.__shuffle_train_idxs = np.random.permutation(range(len(self.__shuffle_train_idxs)))
            self.train_sen1 = self.train_sen1[self.__shuffle_train_idxs]
            self.train_sen2 = self.train_sen2[self.__shuffle_train_idxs]
        return self.train_sen1, self.train_sen2

    def train_labels(self):
        train_labels = self.labels[self.__shuffle_train_idxs]
        return train_labels

    def test_instances(self):
        test_sen1 = self.sen1[-self.num_tests:]
        test_sen2 = self.sen2[-self.num_tests:]
        return test_sen1, test_sen2

    def test_labels(self):
        return self.labels[-self.num_tests:]

    def validation_instances(self, num_instances=None):
        if num_instances is None:
            num_instances = len(self.__shuffle_train_idxs)  # get all training instances for validation

        val_idxs = np.random.permutation(range(len(self.__shuffle_train_idxs)))
        train_sen1, train_sen2 = self.train_instances(shuffle=False)
        train_labels = self.train_labels()

        val_sen1, val_sen2 = train_sen1[val_idxs][:num_instances], train_sen2[val_idxs][:num_instances]
        val_labels = train_labels[val_idxs][:num_instances]
        return val_sen1, val_sen2, val_labels