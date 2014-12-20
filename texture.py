from png import PNG
from color import ColorToInt as CTI


class Texture:
    def __init__(self, width, height, edge=(255, 255, 255, 255),
                 data=None, depth=None):
        # Keep track of basic values for convenience 
        self.width = width
        self.height = height
        
        # Handle the edge condition
        self.edge = edge
      
        # Initialize the and depth data arrays
        self.data = None
        self.depth = None
        if isinstance(data, list):
            self.data = data
            if isinstance(depth, list):
                self.depth = depth
        if self.data is None:
            self.data = []
            for x in range(width):
                self.data.append([])
                for y in range(height):
                    self.data[-1].append((255, 255, 255, 255))
        if self.depth is None:
            self.depth = []
            for x in range(width):
                self.depth.append([])
                for y in range(height):
                    self.depth[-1].append(None)

    def save(self, filename):
        # Initialize an array to hold the colors converted
        # to 32 bit unsigned integers
        intData = []
        for x in range(self.width):
            intData.append([])
            for y in range(self.height):
                argb = self.data[x][y]
                # Reorder the alpha to the back
                intData[-1].append(CTI(argb[1], argb[2], argb[3], argb[0]))
        # Actually save the information to a file
        PNG(intData, filename)

    def saveDepth(self, filename):
        minDepth=None
        maxDepth=None

        # Find the range of values in the depth array
        for x in range(self.width):
            for y in range(self.height):
                depthVal = self.depth[x][y]    
                if depthVal is not None:
                    if maxDepth is None or depthVal > maxDepth:
                        maxDepth = depthVal
                    if minDepth is None or depthVal < minDepth:
                        minDepth = depthVal

        # Define a method for reverse linear (inter/extra)polation.
        def RLerp(v0, v1, val):
            return float(val - v0) / float(v1 - v0)

        # Create visual for depth
        intData = []
        # First make sure min/max are different and not None
        if minDepth is None or maxDepth is None or minDepth == maxDepth:
            # There is no real depth information,  white screen
            for x in range(self.width):
               intData.append([])
               for y in range(self.height):
                   intData[-1].append(0x00000000)
        else:
            # Depth information exists and makes sense
            for x in range(self.width):
               intData.append([])
               for y in range(self.height):
                   depthVal = self.depth[x][y]
                   if depthVal is not None:
                       depthScale = RLerp(minDepth, maxDepth, depthVal)
                       depthColor = int(depthScale * 255)
                       intData[-1].append(CTI(depthColor, depthColor, depthColor, 255))
                   else:
                       intData[-1].append(CTI(0, 0, 0, 0))
        PNG(intData, filename)

    def __getitem__(self, index):
        x, y = index
        x = int(x)
        y = int(y)
        if x < 0 or x > self.width or \
           y < 0 or y > self.width:
            if isinstance(self.edge, basestring):
                if self.edge == "wrap":
                    x = x % self.width
                    y = y % self.height
                elif self.edge == "extend":
                    def Clamp(val, low, high):
                         return max(min(high, val), low)
                    x = Clamp(x, 0, self.width)
                    y = Clamp(y, 0, self.height)
                else:
                    raise ValueError("The edge condition is a string and "
                                      "is not 'wrap' or 'extend'")
            elif isinstance(self.edge, tuple):
                return self.edge
            else:
                raise ValueError("The edge condition is improperly specified")
        return self.data[x][y]

    def __setitem__(self, index, value):
        x, y = index
        x = int(x)
        y = int(y)
        self.set(x, y, value)
 
    def set(self, x, y, value, depth=None):
        x0 = int(x)
        y0 = int(y)
        if x0 < 0 or x0 > self.width or \
           y0 < 0 or y0 > self.width:
            # Out of bounds
            return
        if depth is not None:
            # Do depth check
            depthAt = self.depth[x0][y0]
            if depthAt is not None and self.depth[x0][y0] < depth:
                return
        self.data[x0][y0] = value
        self.depth[x0][y0] = depth

