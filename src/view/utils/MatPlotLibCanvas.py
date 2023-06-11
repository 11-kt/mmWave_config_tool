from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


# Отображение графиков
class MatPlotLibCanvas(FigureCanvasQTAgg):

    def __init__(self, is_3d):
        fig = Figure()

        if not is_3d:
            self.axes = fig.add_subplot()

        else:
            self.axes = fig.add_subplot(111, projection='3d')

        self.axes.grid()
        super(MatPlotLibCanvas, self).__init__(fig)
