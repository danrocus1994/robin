#!/usr/bin/python3
"""
RObin Spectrum ANalizer -- ROSAN -- module

"""

import tkinter as tk
import os, time
from sound_reader import AudioFile
import sounddevice as sd
from track import Track
from sample import Sample

class Window:
    """
    The main view, holds the tracks and the main tools
    """
    def __init__(self):
        """
        Inits the windows attributes instances and views
        """
        self.root = tk.Tk()
        self.root.geometry("1280x150")
        self.root.configure(background="black")
        self.root.title("RObin Spectrum ANalyzer - ROSAN")
        menubar = tk.Menu(self.root, bg="black", foreground='white')
        menubar.add_command(label="Add Track", command=lambda: self.add_track())
        self.root.config(menu=menubar)
        self.canvas = [None, None]
        self.zones = [None]
        self.selecting = False
        self.au_d = [None, None]
        self.tracks = [None]
        self.tracks[0] = Track(self)

    def add_track(self):
        """
        Adds a new track to the main window
        """
        self.tracks.append(Track(self))

    def selectZoneStart(self, ev, nid):
        """
        Set the start point for the sample selection
        """
        if self.tracks[nid].zone != None:
            self.tracks[nid].canvas.delete(self.tracks[nid].zone)
        print(ev, ev.x, ev.y)
        self.tracks[nid].zone = self.tracks[nid].canvas.create_rectangle(ev.x, 1,
                                                        ev.x, 120,
                                                        fill="#2453a3",
                                                        stipple="gray12")
        self.selecting = True


    def selectZoneEnd(self, ev, state, nid):
        """
        Resizes the selection
        and create the new sample when press out the click button
        """
        if state == True and self.selecting == True:
            last = self.tracks[nid].canvas.coords(self.tracks[nid].zone)
            x = last[0]
            self.tracks[nid].canvas.coords(self.tracks[nid].zone, x, 1, ev.x, 120)
        elif self.selecting == True:
            self.selecting = False
            x = self.tracks[nid].canvas.coords(self.tracks[nid].zone)[0]
            width = len(self.au_d[nid].data)
            #Scaling to view size
            x1 = int((width * x) / 1280)
            x2 = int((width * ev.x) / 1280)
            self.sample = AudioFile("samps/sample.wav")
            self.sample.data = self.au_d[nid].data[x1:x2]
            self.set_sample(self.sample.data, nid)
            print(x, ev.x)
        pass

    def set_sample(self, data, nid):
        """
        Set the sample view and instance
        """
        self.sample = Sample(self, data, nid)

    def play_file(self, event, c):
        """
        Plays the track file
        """
        if self.au_d[c] != None:
            self.au_d[c].canvas = self.tracks[c].canvas
            self.au_d[c].play()

    def open_file(self, event, c):
        """
        open a file and save data in an AudioFile object
        prints a list of files in recs/ folder
        wait for user input
        checks if file exists
        and call draw_spectrum
        """
        print("\033[34mFiles: \x1b[38;5;202m")
        files = os.listdir("./recs")
        for i in range(0, len(files), 3):
            try:
                print("{:18}".format(files[i]), "\t", end='')
                print("{:18}".format(files[i + 1]), "\t", end='')
                print("{:18}".format(files[i + 2]), end='')
            except:
                pass
            print()
        inp = input("\033[0m\nChoose a file: ")

        if inp+".wav" in files:
            if c >= len(self.au_d):
                self.au_d.append(None)
            self.au_d[c] = AudioFile(inp)
            data = self.au_d[c].read_file(inp)
            self.draw_spectrum(data, c)
        else:
            print("No file named ", inp)
            self.open_file(event, c)

    def draw_spectrum(self, sound, c, ini=0, end=None):
        """
        Iterates the full data by steps given by chunk of data
        divided by window size
        get each value and scale each one to the track window height
        draws a line from the last to the actual
        """
        if end == None:
            end = len(sound)
        col = "#a834eb" if c == 0 else "#f2a618"
        chunk = end - ini
        steps = chunk / 1280
        beak = 20
        x = 1
        pos = 0
        last = 60
        self.tracks[c].canvas.delete("all")
        while pos < chunk and pos + ini < end:
            y = float(sound[pos + ini]) + 0.5
            y = 120 - int((120 * y) / 1)
            self.tracks[c].canvas.create_line(x - 1, last, x, y, fill=col)
            last = y
            x += 1
            pos += int(steps)
        time = float(chunk / 44100)
        frecuency = 0.1
        sec = frecuency
        while sec < time:
            x = int((sec * 1280) / time)
            self.tracks[c].canvas.create_rectangle(x - 1, 40, x + 1, 80,
                                                   fill="white")
            sec += frecuency

        return ini, ini + chunk

    def round_rectangle(self, x1, y1, x2, y2, s, radius=25, **kwargs):
        """
        creates a rounded rectangle shape
        used for buttons and tools
        """
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius,
                  y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius,
                  x1, y1+radius, x1, y1]
        return s.create_polygon(points, **kwargs, smooth=True)
