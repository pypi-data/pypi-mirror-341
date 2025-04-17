class Renderer(object):
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    def project(self, x, y, z):
        scale = 100
        return (self.width//2 + x*scale,
                self.height//2 - y*scale)

    def render(self, mesh, rot_angles=(0,0,0)):
        from math import sin, cos

        self.canvas.delete("all")

        rx, ry, rz = rot_angles

        def rotate(v):
            x,y,z = v
            y,z = y*cos(rx)-z*sin(rx), y*sin(rx)+z*cos(rx)
            x,z = x*cos(ry)+z*sin(ry), -x*sin(ry)+z*cos(ry)
            x,y = x*cos(rz)-y*sin(rz), x*sin(rz)+y*cos(rz)
            return (x,y,z)

        verts = [rotate(v) for v in mesh.vertices]

        for face in mesh.faces:
            pts = [self.project(*verts[i]) for i in face]
            self.canvas.create_polygon(pts, outline='black', fill='', width=1)