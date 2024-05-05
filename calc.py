import sys
import scipy.constants as constants
import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import sqlite3
import gc

# stars masses
STARS_DICT = {'Солнце': 1, 'Альфа Центавра': 0.9, 'Бетельгейзе': 11,
              'Сириус': 2, 'Арктур': 1.3, 'Ригель': 18, 'Альдебаран': 2.5}
# astronomical unit in meterы
A_E = 1.5 * (10 ** 11)
# Solar mass in kg
SOLAR_MASS = 1.989 * (10 ** 30)
# Gravity constant
G = constants.G
# time delay between points
DT = 30
# points number
N = 2000000
# infinity number
INF = 10 ** 16


# calulations 2D
@njit(fastmath=True)
def count_2d(x0, y0, v0, alpha, M, n, dt, k1, k):
    stop_count = 0
    alpha0 = (alpha / 180) * np.pi
    x = np.zeros(n)
    x[0] = x0
    y = np.zeros(n)
    y[0] = y0
    vx = np.zeros(n)
    vx[0] = v0 * np.cos(alpha0)
    vy = np.zeros(n)
    vy[0] = v0 * np.sin(alpha0)
    for i in range(1, n):
        if (x[i - 1] == 0 and y[i - 1] == 0) or (x[i - 1] > INF or y[i - 1] > INF):
            stop_count = i - 1
            break

        ax = ((-G * M * x[i - 1]) / ((x[i - 1] ** 2 + y[i - 1] ** 2) ** 1.5)) + (k - k1) * vx[i - 1]
        vx2 = vx[i - 1] + dt * ax
        ax1 = ((-G * M * (x[i - 1] + vx[i - 1] * dt)) / (
                    ((x[i - 1] + vx[i - 1] * dt) ** 2 + (y[i - 1] + vy[i - 1] * dt) ** 2) ** 1.5)) + (k - k1) * vx2
        vx[i] = vx[i - 1] + (dt / 2) * (ax + ax1)
        x[i] = x[i - 1] + (dt / 2) * (vx[i - 1] + vx[i])

        ay = ((-G * M * y[i - 1]) / ((x[i - 1] ** 2 + y[i - 1] ** 2) ** 1.5)) + (k - k1) * vy[i - 1]
        vy2 = vy[i - 1] + dt * ay
        ay1 = ((-G * M * ((y[i - 1]) + vy[i - 1] * dt)) / (
                    ((x[i - 1] + vx[i - 1] * dt) ** 2 + (y[i - 1] + vy[i - 1] * dt) ** 2) ** 1.5)) + (k - k1) * vy2
        vy[i] = vy[i - 1] + (dt / 2) * (ay + ay1)
        y[i] = y[i - 1] + (dt / 2) * (vy[i - 1] + vy[i])
    if stop_count:
        for i in range(stop_count, len(x) - 1):
            x[i] = x[stop_count]
            y[i] = y[stop_count]
    return x, y, vx, vy
