#!/usr/bin/env python

import json
import numpy as np
import matplotlib.pyplot as plt

with open("foo.json") as handle:
    data = json.load(handle)

polygons = data["points"]
for poly in polygons:
    poly.append(poly[0])

origin = np.array([124.9258, 34.6012])

# def normalize(v):
#     norm = np.linalg.norm(v)
#     assert norm
#     return v / norm


def extract_key(polygon):
    bary = np.mean(polygon, axis=0) - origin
    return (np.linalg.norm(bary), np.arctan2(bary[1], bary[0]))


polygons.sort(key=extract_key)

polygons = np.array(polygons, dtype=float)
polygons = polygons[:150]

eyes = []
for polygon in polygons:
    midpoint = (polygon[5] + polygon[3]) / 2
    ex = (polygon[5] - polygon[3]) / 2
    ey = np.array([-ex[1], ex[0]])

    def add_eye(xx, yy, ww, hh):
        pos = midpoint + xx * ex + yy * ey
        eyes.append(
            [
                pos - hh * ey,
                pos + ww * ex,
                pos + hh * ey,
                pos - ww * ex,
                pos - hh * ey,
            ]
        )

    add_eye(0.4, 0, 0.3, 0.2)
    add_eye(-0.4, 0, 0.3, 0.2)
eyes = np.array(eyes)


fig = plt.figure()
axe = fig.subplots()
# axe.add_patch(plt.Circle(origin, patate, color="r"))
for poly in polygons:
    axe.plot(poly[:, 0], poly[:, 1], ls="-", color="k")
for poly in eyes:
    axe.plot(poly[:, 0], poly[:, 1], ls="-", color="k")
axe.axis("equal")


def transform_point(pps):
    pps -= origin
    radii = np.linalg.norm(pps, axis=1)
    pps[:, 0] /= radii
    pps[:, 1] /= radii
    radii = np.log(radii / 50 + 1)
    pps[:, 0] *= radii
    pps[:, 1] *= radii
    return pps
    # angles = np.angle(pps[:, 0] + pps[:, 1] * 1j)
    # foo = radii * np.exp(1j * angles)
    # return np.array([foo.real, foo.imag])


polygons_ = []
for polygon in polygons:
    polygon_ = transform_point(polygon)
    polygons_.append(polygon_)
polygons_ = np.array(polygons_, dtype=float)

eyes_ = []
for polygon in eyes:
    polygon_ = transform_point(polygon)
    eyes_.append(polygon_)
eyes_ = np.array(eyes_, dtype=float)

fig = plt.figure()
axe = fig.subplots()
for poly in polygons_:
    axe.plot(poly[:, 0], poly[:, 1], ls="-", color="k")
for poly in eyes_:
    axe.plot(poly[:, 0], poly[:, 1], ls="-", color="k")
axe.axis("equal")


plt.show()
