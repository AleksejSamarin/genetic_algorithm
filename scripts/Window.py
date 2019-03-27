from scripts.Plot import *
import tkinter
import sys
import warnings

class Window():

    def __init__(self, alg):
        self.root = tkinter.Tk(className=' Genetic Algorithm')
        self.root.configure(background='white')
        self.root.resizable(False, False)
        self.f_right = tkinter.Frame()
        self.f_left = tkinter.Frame()
        self.f_right.pack(side=tkinter.LEFT)
        self.f_left.pack(side=tkinter.LEFT)
        warnings.filterwarnings("ignore")
        self.plot_2d = Plot(self.root, self.f_right)
        self.plot_3d = Plot(self.root, self.f_left, True)
        alg.set_window(self)

        self.root.bind("<z>", lambda l: self.run(alg, 1))
        self.root.bind("<x>", lambda l: self.run(alg, 2))
        self.root.bind("<Escape>", self.exit)

        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.after(1000, lambda: self.root.focus_force())
        self.root.mainloop()
        return


    def update_plot(self, *args):
        if len(args) == 2:
            self.plot_2d.draw(args[0], args[1])
        else:
            self.plot_3d.draw(args[0], args[1], args[2])


    def run(self, alg, action):
        alg.run(action)


    def exit(self, event=None):
        self.root.withdraw()
        sys.exit()