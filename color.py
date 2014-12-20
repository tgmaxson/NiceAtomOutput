def ColorToInt(R, G, B, A=255):
    def Clamp(n):
        return max(min(255, n), 0)
    return (Clamp(A) << 24) | (Clamp(R) << 16) | (Clamp(G) << 8) | (Clamp(B));

def IntToColor(ARGB):
    return (ARGB // 256 // 256 // 256 % 256,
            ARGB // 256 // 256 % 256,
            ARGB // 256 % 256,
            ARGB % 256)
