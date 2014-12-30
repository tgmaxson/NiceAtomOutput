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
        
        print self.width, len(self.data)
        print self.height, len(self.data[0])

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
        if x0 < 0 or x0 >= self.width or \
           y0 < 0 or y0 >= self.height:
            # Out of bounds
            return
        if depth is not None:
            # Do depth check
            depthAt = self.depth[x0][y0]
            if depthAt is not None and self.depth[x0][y0] < depth:
                return
        self.data[x0][y0] = value
        self.depth[x0][y0] = depth

    def get_depth(self, x, y):
        x0 = int(x)
        y0 = int(y)
        if x0 < 0 or x0 >= self.width or \
           y0 < 0 or y0 >= self.height:
            # Out of bounds
            return -1e99
        return self.depth[x0][y0]

    def circle(self, x0, y0, radius, color, depth=0):
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        self.set(x0, y0 + radius, color, depth)
        self.set(x0, y0 - radius, color, depth)
        self.set(x0 + radius, y0, color, depth)
        self.set(x0 - radius, y0, color, depth)
 
        while x < y:
            if f >= 0: 
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x    
            self.set(x0 + x, y0 + y, color, depth)
            self.set(x0 - x, y0 + y, color, depth)
            self.set(x0 + x, y0 - y, color, depth)
            self.set(x0 - x, y0 - y, color, depth)
            self.set(x0 + y, y0 + x, color, depth)
            self.set(x0 - y, y0 + x, color, depth)
            self.set(x0 + y, y0 - x, color, depth)
            self.set(x0 - y, y0 - x, color, depth)
    
    def filled_circle(self, x0, y0, radius, color, depth=0):
        for i in range(0-radius, radius+1):
            for ii in range(0-radius, radius+1):
                if (i**2 + ii**2 <= radius**2):
                    self.set(i+x0, ii+y0, color, depth)
                    
    def shaded_circle(self, x0, y0, radius, color, depth=0, lightdir=(0.20, -0.3, 0.9), specBoost=(255,255,255), ramp=5):
        def Normalize(v0):
            x, y, z = v0
            mag = (x**2. + y**2. + z**2.)**(1./2.)
            return (x/mag, y/mag, z/mag)
        
        def C2Dto3D(v0, r = 1):
            x, y = v0
            z = (r**2 - x**2. - y**2.)**(1./2.)
            return Normalize((x, y, z))
            
        def Dot3D(v0, v1):
            x0, y0, z0 = v0
            x1, y1, z1 = v1
            return float((x0*x1) + (y0*y1) + (z0*z1))
        
        lightVect = Normalize(lightdir)        
        for i in range(0-radius, radius+1):
            for ii in range(0-radius, radius+1):
                if (i**2 + ii**2 <= radius**2):
                    normal = C2Dto3D((i,ii), r=radius)
                    dot = Dot3D(lightdir, normal)
                    dot = max(dot, 0.45)
                    specDot = min((dot/1.2) ** ramp, 1)
                    sr, sg, sb = specBoost
                    spec = (int(sr * specDot), int(sg * specDot), int(sb * specDot))
                    result = (color[0], int(color[1]*dot+spec[0]), int(color[2]*dot+spec[1]), int(color[3]*dot+spec[2]))
                    self.set(i+x0, ii+y0, result, depth-normal[2])

    def outlined_circle(self, x0, y0, radius, color, width=1, color2=(255, 0, 0, 0), depth=0, ramp=5):
        self.filled_circle(x0, y0, radius, color2, depth=depth)
        self.shaded_circle(x0, y0, radius-width, color, depth=depth, ramp=ramp)
