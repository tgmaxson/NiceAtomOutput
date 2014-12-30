def ColorToInt(R, G, B, A=255):
    def Clamp(n):
        val = int(n)
        if val > 255: return 255
        if val < 0:   return 0
        return val
    return (Clamp(A) << 24) | (Clamp(R) << 16) | (Clamp(G) << 8) | (Clamp(B));

def IntToColor(ARGB):
    return (ARGB // 256 // 256 // 256 % 256,
            ARGB // 256 // 256 % 256,
            ARGB // 256 % 256,
            ARGB % 256)
