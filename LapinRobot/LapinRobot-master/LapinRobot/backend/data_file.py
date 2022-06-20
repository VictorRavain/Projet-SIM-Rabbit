# coding: utf-8

import backend.myGlobal as Glob

import os
import random as rd
import pandas as pd
from collections import defaultdict
import lzma


def get_key(name, keys):
    if name in keys or len(keys) == 0:
        return name
    else:
        for key in keys:
            if name.startswith(key):
                return key
    return None


class DataFile:

    def __init__(self, directory, keys, channels, stable_state):
        self.map = defaultdict(list)
        self.channels = channels
        self.stable_state = stable_state
        Glob.cur_state = stable_state
        self.filename = None
        self.data = None
        self.line_number = 0
        self.nb_of_lines = 0
        for root, dirs, files in os.walk(directory):
            for file in files:
                push = False
                name = file
                if file.endswith(".txt"):
                    name = file[:-4]
                    push = True
                elif file.endswith(".txt.lzma"):
                    name = file[:-9]
                    push = True
                if push:
                    key = get_key(name, keys)
                    if key is not None:
                        self.map[key].append(os.path.join(root, file))

        Glob.states = [e for e in self.map.keys() if e != stable_state]

    def init(self):
        self.pick_random_file()
        self.open_file()
        Glob.rest_file_name = self.filename

    def pick_random_file(self):
        self.filename = rd.choice(self.map[Glob.cur_state])

    def open_file(self):
        print('Open ', self.filename)
        if self.filename.endswith(".txt.lzma"):
            with lzma.open(self.filename, "r") as f:
                self.data = pd.read_csv(f, sep='\t')
        elif self.filename.endswith(".txt"):
            self.data = pd.read_csv(self.filename, sep='\t')

        self.line_number = 1
        self.nb_of_lines = len(self.data)

    def change_file(self):
        self.pick_random_file()
        self.open_file()

    def read_data(self, chnls):
        """ Read the data to be sent to the robot and the chart """
        self.check_event()
        cstes = {channel['id']: 0 for channel in self.channels}
        for _ in range(Glob.NUMBER_OF_LINES):
            for channel in self.channels:
                cstes[channel['id']] += self.data.loc[self.line_number, channel['name']]
                if channel['name'] in chnls:
                    Glob.tdata[channel['id']].append(Glob.time)
                    Glob.ydata[channel['id']].append(self.data.loc[self.line_number, channel['name']])
            self.line_number += 1
            Glob.time += Glob.FREQUENCY
        for channel in self.channels:
            cstes[channel['id']] /= Glob.NUMBER_OF_LINES
        return cstes

    def check_event(self):
        if self.line_number + Glob.NUMBER_OF_LINES > len(self.data):
            Glob.cur_state = self.stable_state
            Glob.window.rest_back()
            Glob.need_change_file = True

        if Glob.need_change_file:
            self.change_file()
            Glob.need_change_file = False


if __name__ == "__main__":
    print("-------------------------")
    data = DataFile(directory="../public/data/Cardio_Respi/Data_2016", keys=[], channels={},
                    stable_state='Sansinjection')
    for k in sorted(data.map.keys()):
        print(k)
        print(data.map[k])
