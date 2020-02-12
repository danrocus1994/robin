#!/usr/bin/python3
"""
Sample object module
"""

import tkinter as tk
import time
import sounddevice as sd

class Sample:
    """
    Sample object
    :data: The selected audio signal
    :nid: used to track, modify and interact with the data and view
    :window: the pop up window displayed
    :canvas: the main container for the sample view handles the drawing
    :play: plays the sample audio data
    """
    def __init__(self, root, data, nid):
        """
        Inits the attributes, view and listeners
        """
        self.data = data
        self.nid = nid
        self.window = tk.Toplevel(root.root)
        self.window.geometry("800x150+0+230")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.title("Sample from track {}".format(nid + 1))
        self.canvas = tk.Canvas(self.window, width=800,
                                height=150, bg="black",
                                bd=0, relief="ridge",
                                highlightthickness=0)
        self.play = tk.Canvas(self.canvas, width=30, height=30,
                              cursor="hand2",
                              bg="black",bd=0, relief="ridge",
                              highlightthickness=0)
        root.round_rectangle(3, 3, 27, 27,
                             self.play,
                             radius=20, fill="#32a852")
        self.play.create_text(20, 15,
                              text='>',
                              anchor='e', fill="white")
        self.play.bind("<Button-1>", lambda e: self.play_sound(e))
        self.play.place(x=0, y=120)

        self.canvas.pack()
        self.draw_sample()

    def on_close(self):
        """
        Removes the sample instances and view
        """
        print("deleting", self.nid, "sample")
        self.window.destroy()
        del self

    def play_sound(self, evn):
        """
        Plays the sample chunk of data
        """
        line = [None]
        line[0] = self.canvas.create_line(2, 1, 2, 120,
                                          fill="#3debe5",
                                          width=2)
        def draw_time_lapse():
            """
            Draws the time lapsing line
            """
            init = 0
            end = int(len(self.data))
            width = 800
            pos = 0
            lapse = 16
            chunk = int(len(self.data) / width) * lapse
            t_s = float(chunk / 44100) * 1
            print("chunk", chunk, "t_s", t_s)
            sd.play(self.data[init:end], 44100, blocking=False)
            while pos < width:
                end = init + chunk
                self.canvas.move(line[0], lapse, 0)
                self.canvas.update()
                time.sleep(t_s)
                pos += lapse
                init += chunk
            sd.stop()
        draw_time_lapse()
        print("end...")

    def draw_sample(self):
        """
        Draws the spectrogram for the sample data
        """
        width = len(self.data)
        col = "#4287f5"
        chunk = width
        steps = chunk / 800
        beak = 20
        x = 1
        pos = 0
        last = 60
        time = float(width / 44100)

        self.canvas.delete("all")
        while pos < chunk:
            y = float(self.data[pos]) + 0.5
            y = 120 - int((120 * y) / 1)
            self.canvas.create_line(x - 1, last, x, y, fill=col)
            last = y
            x += 1
            pos += int(steps)
        frecuency = 0.006
        sec = frecuency
        while sec < time:
            x = int((sec * 800) / time)
            self.canvas.create_rectangle(x - 1, 40, x + 1, 80,
                                         fill="white")
            sec += frecuency