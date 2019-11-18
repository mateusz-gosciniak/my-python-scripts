import sys
import argparse
import scipy
import scipy.misc
import numpy as np
import tensorflow as tf

def cut_to_numbers(_numpy_matrix_image):
    _y, _x = _numpy_matrix_image.shape
    _up_rows = 0
    for _i in range(_y):
        if np.sum(_numpy_matrix_image[_i:_i+1, 0:_x]) == 0:
            _up_rows += 1
        else:
            break
    _numpy_matrix_image = _numpy_matrix_image[_up_rows:_y, 0:_x]
    
    _y, _x = _numpy_matrix_image.shape
    _down_rows = 0
    for _i in range(_y):
        if np.sum(_numpy_matrix_image[_i:_i+1, 0:_x]) == 0:
            _down_rows += 1
    _numpy_matrix_image = _numpy_matrix_image[0:_y-_down_rows, 0:_x]
    
    _y, _x = _numpy_matrix_image.shape
    _left_col = 0
    for _i in range(_x):
        if np.sum(_numpy_matrix_image[0:_y, _i:_i+1]) == 0:
            _left_col += 1
        else:
            break
    _numpy_matrix_image = _numpy_matrix_image[0:_y, _left_col:_x]
    
    _y, _x = _numpy_matrix_image.shape
    _right_col = 0
    for _i in range(_x, -1, -1):
        if np.sum(_numpy_matrix_image[0:_y, _i-1:_i]) == 0:
            _right_col += 1
        else:
            break
    _numpy_matrix_image = _numpy_matrix_image[0:_y, 0:_x-_right_col]
    
    return _numpy_matrix_image

def get_number(_numpy_matrix_image):
    _y, _x = _numpy_matrix_image.shape
    _columns_of_number = 0
    for _i in range(_x):
        if np.sum(_numpy_matrix_image[0:_y, _i:_i+1]) > 0:
            _columns_of_number += 1
        else:
            break
    _number = _numpy_matrix_image[0:_y, 0:_columns_of_number]
    _numpy_matrix_image = _numpy_matrix_image[0:_y, _columns_of_number:_x]
    return _number, _numpy_matrix_image

def remove_empty_columns_after_number(_numpy_matrix_image):
    _y, _x = _numpy_matrix_image.shape
    _empty_columns = 0
    for _i in range(_x):
        if np.sum(_numpy_matrix_image[0:_y, _i:_i+1]) == 0:
            _empty_columns += 1
        else:
            break
    return _numpy_matrix_image[0:_y, _empty_columns:_x]

def resize_numpy_matrix(_numpy_matrix, _x_offset, _y_offset):
    _y, _x = _numpy_matrix.shape
    _resized_numpy_matrix = np.zeros((_y_offset + _y + _y_offset, _x_offset + _x + _x_offset), _numpy_matrix.dtype)
    for _i in range(_y):
            for _j in range(_x):
                _resized_numpy_matrix[_i + _y_offset, _j + _x_offset] = _numpy_matrix[_i, _j]
    return _resized_numpy_matrix

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

def get_table_of_numbers_from_image(_numpy_matrix):
    _table_of_numbers = []
    _y, _x = _numpy_matrix.shape
    while _x > 0:
        _number, _numpy_matrix = get_number(_numpy_matrix)
        _table_of_numbers.append(_number)
        _numpy_matrix = remove_empty_columns_after_number(_numpy_matrix)
        _y, _x = _numpy_matrix.shape
    return _table_of_numbers

def adjust_numbers_to_ann(_numbers_table):
    for _i in range(len(_numbers_table)):
        _y, _x = _numbers_table[_i].shape
        if _x == 3:
            _numbers_table[_i] = resize_numpy_matrix(_numbers_table[_i], 2, 1)
        else:
            _numbers_table[_i] = resize_numpy_matrix(_numbers_table[_i], 1, 1)
    return _numbers_table

def show_numbers_table(_numbers_table):
    for _i in range(len(_numbers_table)):
        plt.imshow(_numbers_table[_i])
        plt.show()

def one_hot_to_label(_one_hot):
    for _i in range(len(_one_hot)):
        if _one_hot[_i] == 1:
            if _i == 10:
                return '/'
            else:
                return _i
    return False

label = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/']

def main():
    path = sys.argv[1]
    model = frozen_graph = sys.argv[2] 

    captured_image = load_image(path)
    captured_image = drop_rgba(captured_image)
    captured_image = drop_gray_scale(captured_image)
    captured_image = np.invert(captured_image)
    captured_image = cut_to_numbers(captured_image)
    numbers_table = get_table_of_numbers_from_image(captured_image)
    numbers_table = adjust_numbers_to_ann(numbers_table)

    with tf.gfile.GFile(frozen_graph, "rb") as f:
        restored_graph_def = tf.GraphDef()
        restored_graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(restored_graph_def, input_map=None, return_elements=None, name="")

    y = graph.get_tensor_by_name("wyjscie:0")
    x = graph.get_tensor_by_name("wejscie:0")
    
    Output = ''
    for i in range(len(numbers_table)):
        sess = tf.Session(graph=graph)
        results = sess.run(y, feed_dict={x: np.reshape(numbers_table[i], (1, 77))})
        results = np.squeeze(results)
        results = np.around(results, decimals=2)
        result = label[np.argmax(results)]
        Output = Output + str(result)
        sess.close()
    print(Output)
    
if __name__ == '__main__':
    main()
