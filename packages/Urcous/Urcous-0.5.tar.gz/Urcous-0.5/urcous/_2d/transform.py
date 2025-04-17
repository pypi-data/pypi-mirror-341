def identity():
    return [1,0,0,
            0,1,0,
            0,0,1]

def translate(tx, ty):
    return [1,0,tx,
            0,1,ty,
            0,0,1]

def scale(sx, sy):
    return [sx,0, 0,
            0, sy,0,
            0, 0, 1]

def rotate(rad):
    import math
    c, s = math.cos(rad), math.sin(rad)
    return [ c,-s,0,
             s, c,0,
             0, 0,1]

def mul(a, b):
    r = [0]*9
    for i in range(3):
        for j in range(3):
            s = 0
            for k in range(3):
                s += a[i*3+k]*b[k*3+j]
            r[i*3+j] = s
    return r

def apply(m, x, y):
    xp = m[0]*x + m[1]*y + m[2]
    yp = m[3]*x + m[4]*y + m[5]
    wp = m[6]*x + m[7]*y + m[8]
    if wp!=0:
        xp, yp = xp/wp, yp/wp
    return (xp, yp)