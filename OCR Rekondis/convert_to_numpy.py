import numpy as np
import scipy.misc
import os
import matplotlib.pyplot as plt

def load_image(_path):
    return scipy.misc.imread(_path)

def drop_rgba(_matrix_layers):
    return _matrix_layers[:, :, 1]

def drop_gray_scale(_scipy_matrix):
    _y, _x = _scipy_matrix.shape
    _binary_numpy_matrix = np.zeros((_y, _x), np.bool)
    for _i in range(_y):
        for _j in range(_x):
            _binary_numpy_matrix[_i, _j] = _scipy_matrix[_i, _j]
    return _binary_numpy_matrix

_path_load = 'C:\\Users\\goscima\\Desktop\\workspace\\ocr_data\\'
_path_save = 'C:\\Users\\goscima\\Desktop\\workspace\\ocr_npy_data\\'
_list = os.listdir(_path_load)

for _i in range(len(_list)):
    captured_image = load_image(_path_load + _list[_i])
    captured_image = drop_rgba(captured_image)
    captured_image = drop_gray_scale(captured_image)
    captured_image = np.invert(captured_image)
    np.save(_path_save + str(_list[_i]).split('.')[0], captured_image)
