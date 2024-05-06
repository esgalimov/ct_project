import numpy as np
import matplotlib.pyplot as plt
from numba import njit

from constants import *


# calulations 2D
@njit(fastmath=True) # <---- jit-compile calculations to have better perfomance :) 
def count_2d(x0, y0, v0, alpha, M, n, dt, k1, k):
    # index to stop calc
    stop_count = 0

    # degrees in radians
    alpha0 = (alpha / 180) * np.pi

    # init arrays and start values
    x = np.zeros(n)
    x[0] = x0
    y = np.zeros(n)
    y[0] = y0
    vx = np.zeros(n)
    vx[0] = v0 * np.cos(alpha0)
    vy = np.zeros(n)
    vy[0] = v0 * np.sin(alpha0)

    for i in range(1, n):
        # if object flew far away or fell to star - stop
        if (x[i - 1] == 0 and y[i - 1] == 0) or (x[i - 1] > INF or y[i - 1] > INF):
            stop_count = i - 1
            break

        # Euler-Cauchy numeric method
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
    
    # if object flew far away or fell to star - fill last array with last good values to have good graph
    if stop_count:
        for i in range(stop_count, len(x) - 1):
            x[i] = x[stop_count]
            y[i] = y[stop_count]
    return x, y


# 3D (same to 2D)
@njit(fastmath=True)
def count_3d(x0, y0, z0, vx0, vy0, vz0, M, n, dt, k1, k):
    stop_count = 0
    x = np.zeros(n)
    x[0] = x0
    y = np.zeros(n)
    y[0] = y0
    z = np.zeros(n)
    z[0] = z0
    vx = np.zeros(n)
    vx[0] = vx0
    vy = np.zeros(n)
    vy[0] = vy0
    vz = np.zeros(n)
    vz[0] = vz0

    for i in range(1, n):
        if (x[i - 1] == 0 and y[i - 1] == 0 and z[i - 1] == 0) or (x[i - 1] > INF or y[i - 1] > INF or z[i - 1] > INF):
            stop_count = i - 1
            break
        ax = ((-G * M * x[i - 1]) / ((x[i - 1] ** 2 + y[i - 1] ** 2 + z[i - 1] ** 2) ** 1.5)) + (k - k1) * vx[i - 1]
        vx2 = vx[i - 1] + dt * ax
        ax1 = ((-G * M * (x[i - 1] + vx[i - 1] * dt)) / (((x[i - 1] + vx[i - 1] * dt) ** 2 + (
                    y[i - 1] + vy[i - 1] * dt) ** 2 + (z[i - 1] + vz[i - 1] * dt) ** 2) ** 1.5)) + (k - k1) * vx2
        vx[i] = vx[i - 1] + (dt / 2) * (ax + ax1)
        x[i] = x[i - 1] + (dt / 2) * (vx[i - 1] + vx[i])

        ay = ((-G * M * y[i - 1]) / ((x[i - 1] ** 2 + y[i - 1] ** 2 + z[i - 1] ** 2) ** 1.5)) + (k - k1) * vy[i - 1]
        vy2 = vy[i - 1] + dt * ay
        ay1 = ((-G * M * (y[i - 1] + vy[i - 1] * dt)) / (((x[i - 1] + vx[i - 1] * dt) ** 2 + (
                    y[i - 1] + vy[i - 1] * dt) ** 2 + (z[i - 1] + vz[i - 1] * dt) ** 2) ** 1.5)) + (k - k1) * vy2
        vy[i] = vy[i - 1] + (dt / 2) * (ay + ay1)
        y[i] = y[i - 1] + (dt / 2) * (vy[i - 1] + vy[i])

        az = ((-G * M * z[i - 1]) / ((x[i - 1] ** 2 + y[i - 1] ** 2 + z[i - 1] ** 2) ** 1.5)) + (k - k1) * vz[i - 1]
        vz2 = vz[i - 1] + dt * az
        az1 = ((-G * M * (z[i - 1] + vy[i - 1] * dt)) / (((x[i - 1] + vx[i - 1] * dt) ** 2 + (
                    y[i - 1] + vy[i - 1] * dt) ** 2 + (z[i - 1] + vz[i - 1] * dt) ** 2) ** 1.5)) + (k - k1) * vz2
        vz[i] = vz[i - 1] + (dt / 2) * (az + az1)
        z[i] = z[i - 1] + (dt / 2) * (vz[i - 1] + vz[i])
    if stop_count:
        for i in range(stop_count, len(x) - 1):
            x[i] = x[stop_count]
            y[i] = y[stop_count]
            z[i] = z[stop_count]
    return x, y, z

# 2D graph
def draw_2d(to_draw):
    data_arrays = np.array(to_draw)
    # limits to make better position in the end
    x_lim1 = []
    x_lim2 = []
    y_lim1 = []
    y_lim2 = []

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # print(data_arrays)
    for j in data_arrays:
        # plot only 1/1000 part of all points because of matplotlib limit to draw too much points
        x1 = np.zeros(int(N / 1000))
        y1 = np.zeros(int(N / 1000))

        for i in range(0, int(N / 1000)):
            x1[i] = j[0][i * 1000]

        for i in range(0, int(N / 1000)):
            y1[i] = j[1][i * 1000]

        # find limits to make best graph position in the end
        xmax = max(x1)
        ymax = max(y1)
        maxm = max([xmax, ymax])

        xmin = min(x1)
        ymin = min(y1)
        minm = min([xmin, ymin])

        deltax = (maxm - xmax + minm - xmin) / 2
        deltay = (maxm - ymax + minm - ymin) / 2

        x_lim1.append(minm - deltax)
        x_lim2.append(maxm - deltax)

        y_lim1.append(minm - deltay)
        y_lim2.append(maxm - deltay)

        # plot points
        ax.plot(x1, y1)

    # positions
    ax.set_xlim(min(x_lim1), max(x_lim2))
    ax.set_ylim(min(y_lim1), max(y_lim2))

    # some settings
    ax.scatter(0, 0, color='red')
    ax.grid(True)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.show()


# 3D graph - (analog to 2D)
def draw_3d(to_draw):
    data_arrays = np.array(to_draw)
    x_lim1 = []
    x_lim2 = []
    y_lim1 = []
    y_lim2 = []
    z_lim1 = []
    z_lim2 = []

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for j in data_arrays:
        x1 = np.zeros(int(N / 1000))
        y1 = np.zeros(int(N / 1000))
        z1 = np.zeros(int(N / 1000))

        for i in range(0, int(N / 1000)):
            x1[i] = j[0][i * 1000]

        for i in range(0, int(N / 1000)):
            y1[i] = j[1][i * 1000]

        for i in range(0, int(N / 1000)):
            z1[i] = j[2][i * 1000]

        xmax = max(x1)
        ymax = max(y1)
        zmax = max(z1)

        xmin = min(x1)
        ymin = min(y1)
        zmin = min(z1)

        minm = min([xmin, ymin, zmin])
        maxm = max([xmax, ymax, zmax])

        deltax = (maxm - xmax + minm - xmin) / 2
        deltay = (maxm - ymax + minm - ymin) / 2
        deltaz = (maxm - zmax + minm - zmin) / 2

        x_lim1.append(minm - deltax)
        x_lim2.append(maxm - deltax)

        y_lim1.append(minm - deltay)
        y_lim2.append(maxm - deltay)

        z_lim1.append(minm - deltaz)
        z_lim2.append(maxm - deltaz)
        ax.plot(x1, y1, z1)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.scatter(0, 0, 0, color='red')
    ax.set_xlim(min(x_lim1), max(x_lim2))
    ax.set_ylim(min(y_lim1), max(y_lim2))
    ax.set_zlim(min(z_lim1), max(z_lim2))
    plt.show()