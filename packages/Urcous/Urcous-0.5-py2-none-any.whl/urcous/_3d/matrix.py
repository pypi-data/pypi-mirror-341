import math

def rotation_matrix(ax, ay, az):
    cx, sx = math.cos(ax), math.sin(ax)
    cy, sy = math.cos(ay), math.sin(ay)
    cz, sz = math.cos(az), math.sin(az)
    rz = [
        [ cz, -sz, 0, 0],
        [ sz,  cz, 0, 0],
        [  0,   0, 1, 0],
        [  0,   0, 0, 1],
    ]
    ry = [
        [ cy, 0, sy, 0],
        [  0, 1,  0, 0],
        [-sy, 0, cy, 0],
        [  0, 0,  0, 1],
    ]
    rx = [
        [1,   0,    0, 0],
        [0,  cx, -sx, 0],
        [0,  sx,  cx, 0],
        [0,   0,   0, 1],
    ]

    def mul(a,b):
        R = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    R[i][j] += a[i][k]*b[k][j]
        return R
    return mul(rz, mul(ry, rx))

def transform_point(m, p):
    x = m[0][0]*p[0] + m[0][1]*p[1] + m[0][2]*p[2] + m[0][3]
    y = m[1][0]*p[0] + m[1][1]*p[1] + m[1][2]*p[2] + m[1][3]
    z = m[2][0]*p[0] + m[2][1]*p[1] + m[2][2]*p[2] + m[2][3]
    w = m[3][0]*p[0] + m[3][1]*p[1] + m[3][2]*p[2] + m[3][3]
    if w != 0:
        x, y, z = x/w, y/w, z/w
    return (x,y,z)