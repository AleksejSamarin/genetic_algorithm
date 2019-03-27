import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import Axes3D

class Plot:

    def __init__(self, root, frame, plot_3d=False):
        figure = plt.Figure(figsize=(6.4, 5), dpi=100)
        if plot_3d:
            self.plot = figure.add_subplot(111, projection='3d')
            self.canvas = FigureCanvasTkAgg(figure, frame)
            self.plot.mouse_init()
        else:
            self.plot = figure.add_subplot(111)
            self.plot.set_title('Populations')
            self.plot.set_xlabel('Chromosome value')
            self.plot.set_ylabel('Function value')
            self.plot.grid()
            self.canvas = FigureCanvasTkAgg(figure, frame)
        self.canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)


    def draw(self, function, x, y=None):
        if y is None:
            self.plot.scatter(x, function, alpha=0.2)
        else:
            self.plot.scatter(x, y, function)
        self.canvas.draw()