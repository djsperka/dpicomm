from openiris_udp_client import OpenIrisClient, EyesData, EyeData
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from ring import RingBuffer
import numpy as np
import sys
import matplotlib.pyplot as plt
from EyeTraceWidget import EyeTraceWidget
from PyQt6.QtCore import QThread, QObject
from PyQt6.QtWidgets import QMainWindow, QApplication
f_default_ip = 'localhost'




class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.UiComponents()
        self.show()

        self._worker = Plotter(self._plot)
        self._thread = QThread()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.myfunction)
        #Now you can connect the signals of AWorker class to any slots here
        #Also you might want to connect the finished signal of the thread
        # to some slot in order to perform something when the thread
        #finishes
        #e.g,
        #self.thread.finished.connect(self.mythreadhasfinished)
        #Finally you need to start the thread
        self._thread.start()


    def UiComponents(self):
        self._plot = EyeTraceWidget(parent=self, title="test")
        self.setCentralWidget(self._plot)



# Source - https://stackoverflow.com/a
# Posted by finmor
# Retrieved 2026-01-06, License - CC BY-SA 3.0

class Plotter(QObject):
    #define your signals here
    def __init__(self, w, ip='localhost'):
       super(Plotter, self).__init__()
       self._client = OpenIrisClient(ip)
       self._widget = w

    def myfunction(self):
        #Your code from run function goes here.
        #Possibly instead of using True in your while loop you might 
        #better use a flag e.g while self.running:
        #so that when you want to exit the application you can
        #set the flag explicitly to false, and let the thread terminate 
        while True:
            data = self._client.fetch_data(True)
            self._widget.addxy(data.left.frame_number, data.left.pupil.x, data.left.pupil.y)



if __name__ == "__main__":

    parser = ArgumentParser(description='DPI tracker diagnostic tool.', formatter_class=ArgumentDefaultsHelpFormatter)
    #parser.add_argument('--update', action='store_true', help='create new config file')
    parser.add_argument('--ip', default='localhost', help='ip addr of tracker host [default = {0:s}]'.format(f_default_ip))
    args = parser.parse_args()

    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())





# # prepare plot
# eyexy = RingBuffer(1000)
# plt.ion()
# fig = plt.figure()

# ax = fig.add_subplot(121)
# axeye = fig.add_subplot(122)
# line1 = None
# line_eye = None
# counter = 0

# with OpenIrisClient(args.ip) as client:
#     while True:
#         data = client.fetch_data(True)

#         if data is not None:
#             eyexy.add((data.left.frame_number, data.left.pupil.x, data.left.pupil.y))
#             counter += 1
#             if counter==100:
#                 counter = 0
#                 i = [i for i,_,_ in eyexy.get()]
#                 x = [x for _,x,_ in eyexy.get()]
#                 y = [y for _,_,y in eyexy.get()]
#                 imin = np.min(i)
#                 imax = np.max(i)
#                 if not line1:
#                     line1, = ax.plot(i,x)
#                     line2, = ax.plot(i,y)
#                 else:
#                     line1.set_xdata(i)
#                     line1.set_ydata(x)
#                     line2.set_xdata(i)
#                     line2.set_ydata(y)
#                 if imax<(imin+1000):
#                     imax = imin+1000
#                 ax.set_xlim(imin, imax)
#                 ax.set_ylim(100,600)

#                 if not line_eye:
#                     line_eye, = axeye.plot(x[-1], y[-1], 'go')
#                     axeye.set_xlim(-5,5)
#                     axeye.set_ylim(-5,5)
#                 else:
#                     line_eye.set_xdata([x[-1]])
#                     line_eye.set_ydata([y[-1]])

#                 fig.canvas.draw()
#                 fig.canvas.flush_events()
#         else:
#             break
#         #time.sleep(1)
    

