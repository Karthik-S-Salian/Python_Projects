from PIL import Image as PILImage
from numpy import zeros,uint8

class ColorMap:
    def __init__(self):
        self.arr = zeros((255, 255, 3), dtype=uint8)

    def hsv_to_rgb(self,h, s, v):
        h=h/360
        if s == 0.0: v *= 255; return (v, v, v)
        i = int(h * 6.)
        f = (h * 6.) - i
        p, q, t = int(255 * (v * (1. - s))), int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))))
        v *= 255
        i %= 6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

    def rgb_to_hsv(self,r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = (df / mx) 
        v = mx
        return round(h), round(s,2), round(v,2)


    def colormap_image_generator(self,h):
        
        rows,cols,_=self.arr.shape
        for i in range(rows):
            v = rows - i
            for j in range(cols):
                self.arr[i][j] = self.hsv_to_rgb(h, j / 255, v / 255)

        return PILImage.fromarray(self.arr)

    
    def rgb_to_hex(self,r,g,b):
        return "#"+self.hex(r)+self.hex(g)+self.hex(b)

    def hex_to_rgb(self,hex):
        sign='0123456789abcdef'
        r=sign.index(hex[1])*16+sign.index(hex[2])
        g=sign.index(hex[3])*16+sign.index(hex[4])
        b=sign.index(hex[5])*16+sign.index(hex[6])
        return [r,g,b]

    def hex(self,value):
        ans=''
        sign='0123456789abcdef'
        ans+=sign[value%16]
        value=value//16
        ans+=sign[value%16]
        return ans

    def h_scale_generator(self):
        arr=zeros((30,360,3),dtype=uint8)
        for i in range(arr.shape[1]):
            for j in range(arr.shape[0]):
                arr[j][i]=self.hsv_to_rgb(i/360,1,1) 
        return PILImage.fromarray(arr)

    def alpha_scale_generator(self):
        arr=zeros((30,360,3),dtype=uint8)
        for i in range(arr.shape[1]):
            for j in range(arr.shape[0]):
                arr[j][i]=self.hsv_to_rgb(0,0,i/arr.shape[1])
