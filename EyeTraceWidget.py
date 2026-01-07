from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from typing import Iterable, List
from PyQt6.QtGui import QPaintEvent
from typing import Tuple
from ring import RingBuffer

# Inheriting from FigureCanvasQTAgg. 
# FigureCanvas is a widget. Call update() to invalidate and trigger a paintEvent.

class EyeTraceWidget(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, title=None, capacity=1000):
        self._fig = Figure(figsize=(width, height), dpi=dpi)
        self._axes = self._fig.add_subplot(111)
        self._capacity = capacity
        if title:
            self._axes.set_title(title)
        self._fig.tight_layout()
        
        # these are the line objects
        self._xline = None
        self._yline = None

        # x,y data are positions, idata is the x-coordinate
        self._idata = RingBuffer(capacity)
        self._xdata = RingBuffer(capacity)
        self._ydata = RingBuffer(capacity)
        self._invalidated = False

        super().__init__(self._fig)


    def paintEvent(self, e: QPaintEvent) -> None:
        if not self._invalidated:
            return
        idata = self._idata.get()
        if not self._xline:
            lines = self._axes.plot(idata, self._xdata.get(), 'r')
            self._xline = lines[0]
        else:
            self._xline.set_xdata(idata)
            self._xline.set_ydata(self._xdata.get())

        if not self._yline:
            lines = self._axes.plot(idata, self._ydata.get(), 'b')
            self._yline = lines[0]
        else:
            self._yline.set_xdata(idata)
            self._yline.set_ydata(self._ydata.get())

        self._axes.set_xlim(idata[0], idata[0]+self._capacity)
        self._axes.set_ylim(100,600)
        self._invalidated = False
        self.draw()
        super().paintEvent(e)


    def addxy(self, i, x, y):
        # Set _invalidated to true and call update(). The update() call will move the actual update
        # to the gui thread, not the daq thread.

        self._idata.add(i)
        self._xdata.add(x)
        self._ydata.add(y)
        self._invalidated = True
        self.update()

