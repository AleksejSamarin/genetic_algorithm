import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from mpl_toolkits.mplot3d import Axes3D

class Plot:

    def __init__(self, frame, iterations, plot_3d=False):
        self.counter = 0
        self.iterations = iterations
        figure = plt.Figure(figsize=(6.4, 5), dpi=100)
        if plot_3d:
            self.plot = figure.add_subplot(111, projection='3d')
            self.plot.set_xlabel('Chromosome value x')
            self.plot.set_ylabel('Chromosome value y')
            self.plot.set_zlabel('Function value')
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
            self.canvas.draw()
        else:
            self.counter += 1
            if self.counter % self.iterations > self.iterations - 2:
                self.plot.scatter(x, y, function)
                self.canvas.draw()


    def build(self, values):
        if len(values) == 2:
            self.plot.plot(values[0], values[1], '-')
        else:
            self.plot.plot_wireframe(values[0], values[1], values[2], linewidth=0.3, rstride=2, cstride=2)
        self.canvas.draw()