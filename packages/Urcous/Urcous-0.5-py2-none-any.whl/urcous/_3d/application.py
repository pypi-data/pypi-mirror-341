class UcousAppBase(object):
    def __init__(self, width=600, height=400, title='Urcous Engine - Application', win_look='default', icon=r'urcous\py_icon.ico'):
        self.width = width
        self.height = height
        self.title = title
        self.win_look = win_look
        self.icon = icon

        from Tkinter import Tk, Canvas

        self.__TK__ = Tk()
        self.__TK__.title(self.title)
        self.__TK__.config(bg="white")
        self.__TK__.iconbitmap(self.icon)
        sc_w = self.__TK__.winfo_screenwidth()
        sc_h = self.__TK__.winfo_screenheight()
        x = (sc_w - self.width) / 2
        y = (sc_h - self.height) / 2
        self.__TK__.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))
        self.__TK__.resizable(0, 0)

        self.WIN_LOOK(self.win_look)

        c = Canvas(self.__TK__, width=self.width, height=self.height, bg="white")
        c.pack()

        from renderer import Renderer

        self.renderer = Renderer(c, self.width, self.height)

        self.angles = [0.0,0.0,0.0]

        self.running = False

    def WIN_LOOK(self, Win_look):
        if Win_look == 'direct':
            self.__TK__.overrideredirect(1)

        else:
            self.__TK__.overrideredirect(0)

    def run(self):
        self.running = True
        if self.running:
            self.__TK__.mainloop()
        self.running = False