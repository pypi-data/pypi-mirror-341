import Tkinter as tk
from renderer import Renderer

class Scene(object):
    def __init__(self, width=600, height=400, title='Urcous Engine - Application', icon=r'urcous\py_icon.ico'):
        self.width = width
        self.height = height
        self.title = title
        self.icon = icon

        self.__TK__ = tk.Tk()
        self.__TK__.title(self.title)
        self.__TK__.resizable(0, 0)
        self.__TK__.iconbitmap(self.icon)
        self.canvas = tk.Canvas(self.__TK__, width=self.width, height=self.height, bg='white')
        self.canvas.pack()
        self.renderer = Renderer(self.canvas)
        self.objects = []
        self.running = False

    def add(self, shape):
        self.objects.append(shape)

    def render(self):
        self.canvas.delete('all')
        for obj in self.objects:
            obj.draw(self.renderer)

    def run(self, fps=30):
        self.running = True
        def loop():
            if not self.running: return
            self.render()
            self.__TK__.after(int(1000/fps), loop)
        loop()
        self.__TK__.mainloop()

    def stop(self):
        self.running = False