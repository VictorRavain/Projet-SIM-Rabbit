# coding: utf-8

from frontend import interface
from backend import arduino, data_file
import backend.myGlobal as Glob
import time
import yaml

import sys
from PyQt5.QtWidgets import QApplication


def main():
    # 1. Load configuration
    with open('config.yaml', 'r') as file:
        settings = yaml.safe_load(file)

    # 2. Init global variables
    Glob.start, Glob.inject, Glob.stop, Glob.export = start, inject, stop, export
    Glob.data = data_file.DataFile(**settings['data'])
    Glob.plot_channels = settings['plotting']['channels']
    Glob.data.init()
    Glob.running = False

    # 3. Start app
    Glob.robot = arduino.Arduino(settings['data']['channels'], **settings['arduino'])
    Glob.app = QApplication(sys.argv)
    Glob.window = interface.Window(settings)
    sys.exit(Glob.app.exec_())


def start(chart):
    print('Start')
    Glob.running = True
    Glob.cur_state = Glob.data.stable_state
    data = Glob.data
    time0 = time.time_ns()
    virtual_time = 0
    ttw = Glob.FREQUENCY * Glob.NUMBER_OF_LINES * Glob.IN_NS
    while Glob.running:
        csts = data.read_data(Glob.plot_channels)
        Glob.robot.arduino_communication(csts)
        chart.update_chart()
        virtual_time += ttw
        elapsed_time = time.time_ns() - time0
        real_sleep_duration = (virtual_time - elapsed_time) / Glob.IN_NS  # turn in sec
        gap = int(real_sleep_duration / Glob.FREQUENCY)  # in ms
        if real_sleep_duration > 0:
            time.sleep(real_sleep_duration)
        # adapt nb lines to read
        Glob.NUMBER_OF_LINES = min(Glob.MAX_NB_LINES, max(Glob.MIN_NB_LINES, Glob.NUMBER_OF_LINES - gap))
        print(Glob.NUMBER_OF_LINES)
        ttw = Glob.FREQUENCY * Glob.NUMBER_OF_LINES * Glob.IN_NS


def inject(molecule):
    print("Inject", molecule)
    Glob.cur_state = molecule
    Glob.need_change_file = True


def stop():
    print("Stopped")
    Glob.running = False


def export(name, xdata, ydata):
    if name != ".txt":
        if name[-8:] == ".txt.txt":
            name = name[:-4]
        file = open(name, "w")
        # file.write("t (ms)\tPression Arterielle\n")
        for i in range(len(Glob.tdata)):
            line = str(Glob.tdata[i]) + "\t" + str(Glob.ydata[i]) + "\n"
            file.write(line)
        file.close()
        print("Exported with success")
    else:
        print("Export aborted")


if __name__ == "__main__":
    main()
