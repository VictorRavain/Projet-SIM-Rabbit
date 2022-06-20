# coding: utf-8

"""
file to init global variables in every files imported as glob
"""

IN_NS = 1e9  # for duration in nanoseconds
FREQUENCY = 0.005  # one line every 5 ms
NUMBER_OF_LINES = 40  # bunch of lines
MIN_NB_LINES = 20 # ~ 100 ms
MAX_NB_LINES = 100 # ~ 500 ms

# Store the configuration
settings = None
# Store de 'data_file' object that manages the files and date for the simulation
data = None
# Store the channel to plot on the diagram
plot_channels = None

robot = None
app = None
window = None
running = False

time = 0
tdata = None
ydata = None

states = []
cur_state = None
rest_state = None

need_change_file = False


def start(chart):
    return None


def inject(txt):
    return None


def stop():
    return None


def export(param, xdata, ydata):
    return None