import numpy as np


def angle_resolution(
        tx: int,
        rx: int
):

    num_virtual_antenna = tx * rx

    degree_resolution = np.rad2deg(2 / num_virtual_antenna)

    degrees = 180 / degree_resolution

    return degree_resolution, degrees
