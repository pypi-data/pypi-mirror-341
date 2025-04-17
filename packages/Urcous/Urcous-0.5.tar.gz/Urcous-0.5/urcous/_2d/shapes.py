from transform import identity

class Shape(object):
    def __init__(self):
        self.transform = identity()
        self.fill   = ''
        self.outline= 'black'
        self.width  = 1

    def set_transform(self, m):
        self.transform = m

    def draw(self, renderer):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, w, h):
        super(Rectangle, self).__init__()
        self.w, self.h = w, h

    def draw(self, r):

        pts = [(-self.w/2, -self.h/2),
               ( self.w/2, -self.h/2),
               ( self.w/2,  self.h/2),
               (-self.w/2,  self.h/2)]
        r.draw_polygon(pts, self.transform, self.fill, self.outline, self.width)

class Circle(Shape):
    def __init__(self, r, segments=32):
        super(Circle, self).__init__()
        self.r = r
        self.seg = segments

    def draw(self, r):
        pts = []
        import math
        for i in range(self.seg+1):
            theta = 2*math.pi*i/self.seg
            pts.append((self.r*math.cos(theta), self.r*math.sin(theta)))
        r.draw_polygon(pts, self.transform, self.fill, self.outline, self.width)

class Polygon(Shape):
    def __init__(self, pts):
        super(Polygon, self).__init__()
        self.pts = pts

    def draw(self, r):
        r.draw_polygon(self.pts, self.transform, self.fill, self.outline, self.width)

class Line(Shape):
    def __init__(self, pts):
        super(Line, self).__init__()
        self.pts = pts

    def draw(self, r):
        r.draw_line(self.pts, self.transform, self.outline, self.width)