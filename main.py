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

Tex = Texture(10, 10)
for i in range(10):
 for ii in range(10):
  Tex.set(i, ii, (255, 0, 0, 0), depth = i)

for i in range(10):
 for ii in range(10):
  Tex.set(i, ii, (255, 255, 255, 255), depth = ii)

for i in range(4,6):
 for ii in range(4,6):
  Tex[i, ii] = (255, 255, 0, 0)

Tex.save("test.png")
Tex.saveDepth("depth.png")
