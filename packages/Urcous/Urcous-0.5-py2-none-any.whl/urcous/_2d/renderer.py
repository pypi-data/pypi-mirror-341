from transform import apply

class Renderer(object):
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_polygon(self, pts, m, fill, outline, width):
        screen = []
        for x,y in pts:
            screen.extend(apply(m, x, y))
        self.canvas.create_polygon(screen, fill=fill, outline=outline, width=width)

    def draw_line(self, pts, m, outline, width):
        screen = []
        for x,y in pts:
            screen.extend(apply(m, x, y))
        self.canvas.create_line(screen, fill=outline, width=width)