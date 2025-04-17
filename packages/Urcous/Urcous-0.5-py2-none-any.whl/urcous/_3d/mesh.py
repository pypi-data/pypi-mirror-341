class Mesh:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces

    @classmethod
    def cube(cls, size=2):
        c = size/2.0
        verts = [(-c,-c,-c),( c,-c,-c),( c, c,-c),(-c, c,-c),
                 (-c,-c, c),( c,-c, c),( c, c, c),(-c, c, c)]
        faces = [
          (0,1,2),(0,2,3),
          (4,6,5),(4,7,6),
          (0,4,5),(0,5,1),
          (1,5,6),(1,6,2),
          (2,6,7),(2,7,3),
          (3,7,4),(3,4,0)
        ]
        return cls(verts, faces)

    @classmethod
    def circle(cls, radius=1.0, segments=32):
        import math
        verts = []
        faces = []

        verts.append((0.0, 0.0, 0.0))

        for i in range(segments):
            theta = 2 * math.pi * i / segments
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            verts.append((x, y, 0.0))

        for i in range(1, segments):
            faces.append((0, i, i+1))
        faces.append((0, segments, 1))

        return cls(verts, faces)

    @classmethod
    def plane(cls, width=1.0, height=1.0, w_segs=1, h_segs=1):
        verts = []
        faces = []
        dx = width  / w_segs
        dy = height / h_segs
        for iy in range(h_segs+1):
            for ix in range(w_segs+1):
                x = ix*dx - width/2
                y = iy*dy - height/2
                verts.append((x, y, 0.0))
        def idx(ix, iy): return iy*(w_segs+1) + ix
        for iy in range(h_segs):
            for ix in range(w_segs):
                i0 = idx(ix,   iy)
                i1 = idx(ix+1, iy)
                i2 = idx(ix+1, iy+1)
                i3 = idx(ix,   iy+1)
                faces.append((i0, i1, i2))
                faces.append((i0, i2, i3))
        return cls(verts, faces)

    @classmethod
    def sphere(cls, radius=1.0, lat_segs=16, lon_segs=32):
        import math
        verts = []
        faces = []

        for i in range(lat_segs+1):
            theta = math.pi * i / lat_segs
            sin_t = math.sin(theta)
            cos_t = math.cos(theta)
            for j in range(lon_segs):
                phi = 2*math.pi * j / lon_segs
                x = radius * sin_t * math.cos(phi)
                y = radius * sin_t * math.sin(phi)
                z = radius * cos_t
                verts.append((x,y,z))

        def vid(i,j): return i*lon_segs + (j % lon_segs)
        for i in range(lat_segs):
            for j in range(lon_segs):
                a = vid(i,   j)
                b = vid(i+1, j)
                c = vid(i+1, j+1)
                d = vid(i,   j+1)
                if i != 0:
                    faces.append((a, b, d))
                if i != lat_segs-1:
                    faces.append((b, c, d))
        return cls(verts, faces)

    @classmethod
    def cylinder(cls, radius=1.0, height=2.0, radial_segs=32, height_segs=1):
        import math
        verts = []
        faces = []

        for i in range(height_segs+1):
            z = -height/2 + height * i / height_segs
            for j in range(radial_segs):
                theta = 2*math.pi * j / radial_segs
                x = radius * math.cos(theta)
                y = radius * math.sin(theta)
                verts.append((x,y,z))

        def vid(i,j): return i*radial_segs + (j % radial_segs)
        for i in range(height_segs):
            for j in range(radial_segs):
                a = vid(i,   j)
                b = vid(i+1, j)
                c = vid(i+1, j+1)
                d = vid(i,   j+1)
                faces.append((a,b,c))
                faces.append((a,c,d))

        base_center = len(verts)
        top_center  = base_center + 1
        verts.append((0,0,-height/2))
        verts.append((0,0, height/2))

        for j in range(radial_segs):
            faces.append((base_center, vid(0,j+1), vid(0,j)))

        for j in range(radial_segs):
            faces.append((top_center, vid(height_segs,j), vid(height_segs,j+1)))
        return cls(verts, faces)

    @classmethod
    def cone(cls, radius=1.0, height=2.0, radial_segs=32):
        import math
        verts = []
        faces = []
        base_center = 0
        verts.append((0,0,-height/2))
        for j in range(radial_segs):
            theta = 2*math.pi * j / radial_segs
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            verts.append((x,y,-height/2))
        apex = len(verts)
        verts.append((0,0, height/2))
        for j in range(radial_segs):
            faces.append((base_center, j+1, ((j+1)%radial_segs)+1))
            faces.append((apex, j+1, ((j+1)%radial_segs)+1))
        return cls(verts, faces)

    @classmethod
    def torus(cls, radius_major=1.0, radius_minor=0.3, major_segs=32, minor_segs=16):
        import math
        verts = []
        faces = []

        for i in range(major_segs):
            theta = 2*math.pi * i / major_segs
            cx = math.cos(theta) * radius_major
            cz = math.sin(theta) * radius_major
            for j in range(minor_segs):
                phi = 2*math.pi * j / minor_segs
                x = (radius_major + radius_minor * math.cos(phi)) * math.cos(theta)
                y = radius_minor * math.sin(phi)
                z = (radius_major + radius_minor * math.cos(phi)) * math.sin(theta)
                verts.append((x, y, z))

        def vid(i,j):
            return (i % major_segs) * minor_segs + (j % minor_segs)

        for i in range(major_segs):
            for j in range(minor_segs):
                a = vid(i,   j)
                b = vid(i+1, j)
                c = vid(i+1, j+1)
                d = vid(i,   j+1)
                faces.append((a, b, c))
                faces.append((a, c, d))

        return cls(verts, faces)