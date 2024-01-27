#!/usr/bin/env python

import json
import numpy as np
import matplotlib.pyplot as plt

with open("foo.json") as handle:
    data = json.load(handle)

polygons = data["points"]
for poly in polygons:
    poly.append(poly[0])

polygons = np.array(polygons, dtype=float)
# polygons = polygons[:512]

fig = plt.figure()
axe = fig.subplots()
for poly in polygons:
    axe.plot(poly[:, 0], poly[:, 1], ls="-", color="k")
axe.axis("equal")


plt.show()
