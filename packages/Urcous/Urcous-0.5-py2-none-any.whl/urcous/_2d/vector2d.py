# max2dtk/vector2d.py
import math

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def scale(v, s):
    return (v[0]*s, v[1]*s)

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]

def length(v):
    return math.sqrt(dot(v,v))

def normalize(v):
    l = length(v)
    if l != 0:
        return (v[0]/l, v[1]/l)
    else:
        return (0, 0)