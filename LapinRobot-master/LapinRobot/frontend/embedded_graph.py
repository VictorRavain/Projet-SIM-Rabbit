from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FingureCanvas

import backend.myGlobal as Glob

plt.ion()


class DynamicChart(FingureCanvas):
    def __init__(self, settings, width, parent=None):
        self.min_t = 0
        self.max_t = width
        self.graph_width = width
        self.margin_t = 0.1 * width

        Glob.plot_channels = settings['plotting']['channels']
        channels = settings['data']['channels']
        self.fig, self.axes = plt.subplots(nrows=len(Glob.plot_channels), ncols=1, squeeze=False)  # squeeze=False to deal with 1 channel selected
        self.lines = defaultdict(list)
        Glob.tdata = defaultdict(list)
        Glob.ydata = defaultdict(list)
        for i in range(len(Glob.plot_channels)):
            ch = next(filter(lambda c: c['name'] == Glob.plot_channels[i], channels), None)
            ax = self.axes[i][0]  # due to squeeze = False
            ax.set_ylabel(ch['description'])
            ax.set_xlabel("Temps (s)")
            ax.grid()
            ax.set_xlim(self.min_t, self.max_t + self.margin_t)
            bounds = ch['bounds']
            margin = 0.1 * (bounds[1] - bounds[0])
            ax.set_ylim(bounds[0] - margin, bounds[1] + margin)
            id = ch['id']
            Glob.tdata[id] = []
            Glob.ydata[id] = []
            self.lines[id], = self.axes[i][0].plot([], [], '-')

        FingureCanvas.__init__(self, self.fig)
        self.setParent(parent)

    def update_chart(self):
        for k in Glob.tdata.keys():
            self.lines[k].set_xdata(Glob.tdata[k])
            self.lines[k].set_ydata(Glob.ydata[k])

        self.set_scale()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def set_scale(self):
        for i in range(len(Glob.tdata.keys())):
            xydata = self.axes[i][0].get_lines()[0].get_xydata()
            if len(xydata) > 0:
                xdata = xydata[:, 0]
                ydata = xydata[:, 1]
                self.axes[i][0].set_xlim(xdata.max() - self.graph_width, xdata.max() + +self.margin_t)
                yrange = (ydata.max() - ydata.min()) * .2
                self.axes[i][0].set_ylim(ydata.min() - yrange, ydata.max() + yrange)

    def reinit_graph(self):
        for k in Glob.tdata.keys():
            Glob.tdata[k] = []
            Glob.ydata[k] = []
        Glob.time = 0
        self.min_t = 0
        self.max_t = self.graph_width
        self.set_scale()
