#! /usr/bin/env python
from png import PNG
from texture import Texture

# The majority of this code is probably random nonsense
# until the other major parts of the code are done.  This
# file is named "main.py" but is closer to "test.py". As
# is this file has no defined behavior but this safety pig
# should protect you from any danger.
#                          _
#  _._ _..._ .-',     _.._(`))
# '-. `     '  /-._.-'    ',/
#    )         \            '.
#   / _    _    |             \
#  |  a    a    /              |
#  \   .-.                     ;  
#   '-('' ).-'       ,'       ;
#      '-;           |      .'
#         \           \    /
#         | 7  .__  _.-\   \
#         | |  |  ``/  /`  /
#        /,_|  |   /,_/   /
#           /,_/      '`-'

from ase.io import read
from ase.data import covalent_radii as cr
from ase.data.colors import jmol_colors as colors_us
import numpy as np
a = read("POSCAR")

zoom = 30
x, y, z = a.get_cell()
Tex = Texture(int(x[0]*zoom), int(y[1]*zoom))

colors = []
for col in colors_us:
    r, g, b = col
    color = (255, int(r*255), int(g*255), int(b*255))
    colors.append(color)

for x, atom in enumerate(a):
    print x
    num = atom.number
    color = colors[num]
    radius = int(cr[num] * zoom)
    x = atom.position[0]*zoom
    y = atom.position[1]*zoom
    depth = -atom.position[2]*zoom
    Tex.outlined_circle(x, y, radius, color, depth = depth)

Tex.save("test.png")
Tex.saveDepth("depth.png")
