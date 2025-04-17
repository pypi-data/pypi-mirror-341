__author__ = "xlinfr"

import numpy as np


# Slope and aspect used in SEBE and Wall aspect
def get_ders(dsm, scale):
    # dem,_,_=read_dem_grid(dem_file)
    dx = 1 / scale
    # dx=0.5
    fy, fx = np.gradient(dsm, dx, dx)
    asp, grad = cart2pol(fy, fx, "rad")
    slope = np.arctan(grad)
    asp = asp * -1
    asp = asp + (asp < 0) * (np.pi * 2)
    return slope, asp


def cart2pol(x, y, units="deg"):
    radius = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    if units in ["deg", "degs"]:
        theta = theta * 180 / np.pi
    return theta, radius
