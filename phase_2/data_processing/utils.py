import numpy as np


def consecutive(data, step_size=1):
    split_indices = np.where(np.diff(data) > step_size)[0]
    return split_indices, np.split(data, split_indices+1)
