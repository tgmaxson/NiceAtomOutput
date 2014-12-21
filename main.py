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

Tex = Texture(1000, 100)

for i in range(20):
    Tex.outlined_circle(50 + (i*50), 50, 50, (255, 255, 0, 0), depth = i)

Tex.save("test.png")
Tex.saveDepth("depth.png")
