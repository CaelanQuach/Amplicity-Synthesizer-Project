from tkinter import *
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread

WIDTH = 1200
HEIGHT = 600
mWIDTH = int(WIDTH/2)
mHEIGHT = int(HEIGHT*2/3)
#code for declaring variables for the GPIO board
switches = [18,19,20,17,16,13,12,6,5]
leds = [23,24,22]
GPIO.setmode(GPIO.BCM)
GPIO.setup(leds,GPIO.OUT)
GPIO.setup(switches,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


class MainWin(Canvas):
    def __init__(self, master, title):
        Canvas.__init__(self, master, bg = "black")
        self.pack(fill = BOTH, expand = 1)
        self.title = title
        master.geometry("{}x{}".format(WIDTH+130, HEIGHT))
        self.setUP()

    def setUP(self):
        t1disp = Label(self.master, text = "Track 1", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int(WIDTH/17), height = int(HEIGHT/6))
        t1disp.place(bordermode=OUTSIDE, width = int(WIDTH/17), height = int(HEIGHT/6))
        t2disp = Label(self.master, text = "Track 2", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int(WIDTH/17), height = int(HEIGHT/6))
        t2disp.place(bordermode=OUTSIDE, width = int(WIDTH/17), height = int(HEIGHT/6), y = 100)
        t3disp = Label(self.master, text = "Track 3", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int(WIDTH/17), height = int(HEIGHT/6))
        t3disp.place(bordermode=OUTSIDE, width = int(WIDTH/17), height = int(HEIGHT/6), y= 200)
        t4disp = Label(self.master, text = "Track 4", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int(WIDTH/17), height = int(HEIGHT/6))
        t4disp.place(bordermode=OUTSIDE, width = int(WIDTH/17), height = int(HEIGHT/6), y= 300)
        t5disp = Label(self.master, text = "Track 5", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int(WIDTH/17), height = int(HEIGHT/6))
        t5disp.place(bordermode=OUTSIDE, width = int(WIDTH/17), height = int(HEIGHT/6), y= 400)
        t6disp = Label(self.master, text = "Track 6", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int(WIDTH/17), height = int(HEIGHT/6))
        t6disp.place(bordermode=OUTSIDE, width = int(WIDTH/17), height = int(HEIGHT/6), y = 500)

        #t1 measures
        t1m1 = Button(self.master, text = "t1m1", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.MeasureGUICall("t1m1"))
        t1m1.place(bordermode=OUTSIDE, width = int(WIDTH/17), height = int(HEIGHT/6), x = int(WIDTH/17))
        t1m2 = Button(self.master, text="t1m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m2"))
        t1m2.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17)*2)
        t1m3 = Button(self.master, text="t1m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m3"))
        t1m3.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17)*3)
        t1m4 = Button(self.master, text="t1m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m4"))
        t1m4.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17)*4)
        t1m5 = Button(self.master, text="t1m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m5"))
        t1m5.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 5)
        t1m6 = Button(self.master, text="t1m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m6"))
        t1m6.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 6)
        t1m7 = Button(self.master, text="t1m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m7"))
        t1m7.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17)*7)
        t1m8 = Button(self.master, text="t1m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m8"))
        t1m8.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 8)
        t1m9 = Button(self.master, text="t1m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m9"))
        t1m9.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 9)
        t1m10 = Button(self.master, text="t1m10", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m10"))
        t1m10.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 10)
        t1m11 = Button(self.master, text="t1m11", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m11"))
        t1m11.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 11)
        t1m12 = Button(self.master, text="t1m12", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m12"))
        t1m12.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 12)
        t1m13 = Button(self.master, text="t1m13", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m13"))
        t1m13.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 13)
        t1m14 = Button(self.master, text="t1m14", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m14"))
        t1m14.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 14)
        t1m15 = Button(self.master, text="t1m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m15"))
        t1m15.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 15)
        t1m16 = Button(self.master, text="t1m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m16"))
        t1m16.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 16)
        t1volume = Button(self.master, text = "track volume", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.VolumeGUICall("track 1"))
        t1volume.place(bordermode=OUTSIDE, width = int(WIDTH/8.5), height = int(HEIGHT/12), x = int(WIDTH/17) * 17,y = (HEIGHT / 20))
        # t2 measures
        t2m1 = Button(self.master, text="t2m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m1"))
        t2m1.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17), y = (HEIGHT / 6))
        t2m2 = Button(self.master, text="t2m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m2"))
        t2m2.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 2, y = (HEIGHT / 6))
        t2m3 = Button(self.master, text="t2m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m3"))
        t2m3.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 3, y = (HEIGHT / 6))
        t2m4 = Button(self.master, text="t2m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m4"))
        t2m4.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 4, y = (HEIGHT / 6))
        t2m5 = Button(self.master, text="t2m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m5"))
        t2m5.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 5, y = (HEIGHT / 6))
        t2m6 = Button(self.master, text="t2m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m6"))
        t2m6.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 6, y = (HEIGHT / 6))
        t2m7 = Button(self.master, text="t2m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m7"))
        t2m7.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 7, y = (HEIGHT / 6))
        t2m8 = Button(self.master, text="t2m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m8"))
        t2m8.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 8, y = (HEIGHT / 6))
        t2m9 = Button(self.master, text="t2m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m9"))
        t2m9.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 9, y = (HEIGHT / 6))
        t2m10 = Button(self.master, text="t2m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m10"))
        t2m10.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 10, y = (HEIGHT / 6))
        t2m11 = Button(self.master, text="t2m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m11"))
        t2m11.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 11, y = (HEIGHT / 6))
        t2m12 = Button(self.master, text="t2m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m12"))
        t2m12.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 12, y = (HEIGHT / 6))
        t2m13 = Button(self.master, text="t2m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m13"))
        t2m13.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 13, y = (HEIGHT / 6))
        t2m14 = Button(self.master, text="t2m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m14"))
        t2m14.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 14, y = (HEIGHT / 6))
        t2m15 = Button(self.master, text="t2m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m15"))
        t2m15.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 15, y = (HEIGHT / 6))
        t2m16 = Button(self.master, text="t2m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m16"))
        t2m16.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 16, y = (HEIGHT / 6))
        t2volume = Button(self.master, text = "track 2 volume", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.VolumeGUICall("track 2"))
        t2volume.place(bordermode=OUTSIDE, width = int(WIDTH/8.5), height = int(HEIGHT/12), x = int(WIDTH/17) * 17,y = (HEIGHT / 20)*4)
        
        # t2 measures
        t3m1 = Button(self.master, text="t3m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m1"))
        t3m1.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17), y = (HEIGHT / 6)*2)
        t3m2 = Button(self.master, text="t3m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m2"))
        t3m2.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 2, y = (HEIGHT / 6)*2)
        t3m3 = Button(self.master, text="t3m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m3"))
        t3m3.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 3, y = (HEIGHT / 6)*2)
        t3m4 = Button(self.master, text="t3m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m4"))
        t3m4.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 4, y = (HEIGHT / 6)*2)
        t3m5 = Button(self.master, text="t3m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m5"))
        t3m5.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 5, y = (HEIGHT / 6)*2)
        t3m6 = Button(self.master, text="t3m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m6"))
        t3m6.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 6, y = (HEIGHT / 6)*2)
        t3m7 = Button(self.master, text="t3m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m7"))
        t3m7.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 7, y = (HEIGHT / 6)*2)
        t3m8 = Button(self.master, text="t3m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m8"))
        t3m8.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 8, y = (HEIGHT / 6)*2)
        t3m9 = Button(self.master, text="t3m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m9"))
        t3m9.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 9, y = (HEIGHT / 6)*2)
        t3m10 = Button(self.master, text="t3m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m10"))
        t3m10.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 10, y = (HEIGHT / 6)*2)
        t3m11 = Button(self.master, text="t3m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m11"))
        t3m11.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 11, y = (HEIGHT / 6)*2)
        t3m12 = Button(self.master, text="t3m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m12"))
        t3m12.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 12, y = (HEIGHT / 6)*2)
        t3m13 = Button(self.master, text="t3m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m13"))
        t3m13.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 13, y = (HEIGHT / 6)*2)
        t3m14 = Button(self.master, text="t3m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m14"))
        t3m14.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 14, y = (HEIGHT / 6)*2)
        t3m15 = Button(self.master, text="t3m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m15"))
        t3m15.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 15, y = (HEIGHT / 6)*2)
        t3m16 = Button(self.master, text="t3m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m16"))
        t3m16.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 16, y = (HEIGHT / 6)*2)
        t3volume = Button(self.master, text = "track 3 volume", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.VolumeGUICall("track 3"))
        t3volume.place(bordermode=OUTSIDE, width = int(WIDTH/8.5), height = int(HEIGHT/12), x = int(WIDTH/17) * 17,y = (HEIGHT / 20)*7.5)
        
        # t4 measures
        t4m1 = Button(self.master, text="t4m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m1"))
        t4m1.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17), y = (HEIGHT / 6)*3)
        t4m2 = Button(self.master, text="t4m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m2"))
        t4m2.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 2, y = (HEIGHT / 6)*3)
        t4m3 = Button(self.master, text="t4m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m3"))
        t4m3.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 3, y = (HEIGHT / 6)*3)
        t4m4 = Button(self.master, text="t4m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m4"))
        t4m4.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 4, y = (HEIGHT / 6)*3)
        t4m5 = Button(self.master, text="t4m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m5"))
        t4m5.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 5, y = (HEIGHT / 6)*3)
        t4m6 = Button(self.master, text="t4m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m6"))
        t4m6.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 6, y = (HEIGHT / 6)*3)
        t4m7 = Button(self.master, text="t4m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m7"))
        t4m7.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 7, y = (HEIGHT / 6)*3)
        t4m8 = Button(self.master, text="t4m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m8"))
        t4m8.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 8, y = (HEIGHT / 6)*3)
        t4m9 = Button(self.master, text="t4m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m9"))
        t4m9.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 9, y = (HEIGHT / 6)*3)
        t4m10 = Button(self.master, text="t4m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m10"))
        t4m10.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 10, y = (HEIGHT / 6)*3)
        t4m11 = Button(self.master, text="t4m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m11"))
        t4m11.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 11, y = (HEIGHT / 6)*3)
        t4m12 = Button(self.master, text="t4m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m12"))
        t4m12.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 12, y = (HEIGHT / 6)*3)
        t4m13 = Button(self.master, text="t4m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m13"))
        t4m13.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 13, y = (HEIGHT / 6)*3)
        t4m14 = Button(self.master, text="t4m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m14"))
        t4m14.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 14, y = (HEIGHT / 6)*3)
        t4m15 = Button(self.master, text="t4m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m15"))
        t4m15.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 15, y = (HEIGHT / 6)*3)
        t4m16 = Button(self.master, text="t4m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m16"))
        t4m16.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 16, y = (HEIGHT / 6)*3)
        t4volume = Button(self.master, text = "track 4 volume", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.VolumeGUICall("track 4"))
        t4volume.place(bordermode=OUTSIDE, width = int(WIDTH/8.5), height = int(HEIGHT/12), x = int(WIDTH/17) * 17,y = (HEIGHT / 20)*10.75)
        
        # t5 measures
        t5m1 = Button(self.master, text="t5m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m1"))
        t5m1.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17), y = (HEIGHT / 6)*4)
        t5m2 = Button(self.master, text="t5m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m2"))
        t5m2.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 2, y = (HEIGHT / 6)*4)
        t5m3 = Button(self.master, text="t5m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m3"))
        t5m3.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 3, y = (HEIGHT / 6)*4)
        t5m4 = Button(self.master, text="t5m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m4"))
        t5m4.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 4, y = (HEIGHT / 6)*4)
        t5m5 = Button(self.master, text="t5m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m5"))
        t5m5.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 5, y = (HEIGHT / 6)*4)
        t5m6 = Button(self.master, text="t5m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m6"))
        t5m6.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 6, y = (HEIGHT / 6)*4)
        t5m7 = Button(self.master, text="t5m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m7"))
        t5m7.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 7, y = (HEIGHT / 6)*4)
        t5m8 = Button(self.master, text="t5m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m8"))
        t5m8.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 8, y = (HEIGHT / 6)*4)
        t5m9 = Button(self.master, text="t5m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m9"))
        t5m9.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 9, y = (HEIGHT / 6)*4)
        t5m10 = Button(self.master, text="t5m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m10"))
        t5m10.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 10, y = (HEIGHT / 6)*4)
        t5m11 = Button(self.master, text="t5m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m11"))
        t5m11.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 11, y = (HEIGHT / 6)*4)
        t5m12 = Button(self.master, text="t5m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m12"))
        t5m12.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 12, y = (HEIGHT / 6)*4)
        t5m13 = Button(self.master, text="t5m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m13"))
        t5m13.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 13, y = (HEIGHT / 6)*4)
        t5m14 = Button(self.master, text="t5m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m14"))
        t5m14.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 14, y = (HEIGHT / 6)*4)
        t5m15 = Button(self.master, text="t5m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m15"))
        t5m15.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 15, y = (HEIGHT / 6)*4)
        t5m16 = Button(self.master, text="t5m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m16"))
        t5m16.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 16, y = (HEIGHT / 6)*4)
        t5volume = Button(self.master, text = "track 5 volume", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.VolumeGUICall("track 5"))
        t5volume.place(bordermode=OUTSIDE, width = int(WIDTH/8.5), height = int(HEIGHT/12), x = int(WIDTH/17) * 17,y = (HEIGHT / 20)*14.25)
        
        # t6 measures
        t6m1 = Button(self.master, text="t6m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m1"))
        t6m1.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17), y = (HEIGHT / 6)*5)
        t6m2 = Button(self.master, text="t6m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m2"))
        t6m2.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 2, y = (HEIGHT / 6)*5)
        t6m3 = Button(self.master, text="t6m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m3"))
        t6m3.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 3, y = (HEIGHT / 6)*5)
        t6m4 = Button(self.master, text="t6m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m4"))
        t6m4.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 4, y = (HEIGHT / 6)*5)
        t6m5 = Button(self.master, text="t6m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m5"))
        t6m5.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 5, y = (HEIGHT / 6)*5)
        t6m6 = Button(self.master, text="t6m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m6"))
        t6m6.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 6, y = (HEIGHT / 6)*5)
        t6m7 = Button(self.master, text="t6m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m7"))
        t6m7.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 7, y = (HEIGHT / 6)*5)
        t6m8 = Button(self.master, text="t6m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m8"))
        t6m8.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 8, y = (HEIGHT / 6)*5)
        t6m9 = Button(self.master, text="t6m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m9"))
        t6m9.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 9, y = (HEIGHT / 6)*5)
        t6m10 = Button(self.master, text="t6m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m10"))
        t6m10.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 10, y = (HEIGHT / 6)*5)
        t6m11 = Button(self.master, text="t6m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m11"))
        t6m11.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 11, y = (HEIGHT / 6)*5)
        t6m12 = Button(self.master, text="t6m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m12"))
        t6m12.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 12, y = (HEIGHT / 6)*5)
        t6m13 = Button(self.master, text="t6m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m13"))
        t6m13.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 13, y = (HEIGHT / 6)*5)
        t6m14 = Button(self.master, text="t6m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m14"))
        t6m14.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 14, y = (HEIGHT / 6)*5)
        t6m15 = Button(self.master, text="t6m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m15"))
        t6m15.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 15, y = (HEIGHT / 6)*5)
        t6m16 = Button(self.master, text="t6m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m16"))
        t6m16.place(bordermode=OUTSIDE, width=int(WIDTH / 17), height=int(HEIGHT / 6), x=int(WIDTH / 17) * 16, y = (HEIGHT / 6)*5)
        t6volume = Button(self.master, text = "track 6 volume", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.VolumeGUICall("track 6"))
        t6volume.place(bordermode=OUTSIDE, width = int(WIDTH/8.5), height = int(HEIGHT/12), x = int(WIDTH/17) * 17,y = (HEIGHT / 20)*17.5)
        
    def MeasureGUICall(self, measure):
        top = Toplevel(window)
        top.geometry("{}x{}".format(mWIDTH, mHEIGHT))
        top.title(measure)
        Label(top, text=measure, font=("MingLiU-ExtB", 12), bg = "black", fg = "light blue").place(width=mWIDTH, height=mHEIGHT)
    
    def VolumeGUICall(self, track):
        top = Toplevel(window)
        top.geometry("{}x{}".format(mWIDTH, mHEIGHT))
        top.title(track)
        global currentTrack
        global UniVolume
        global mute
        global TrackVolumeLabel
        currentTrack = int(track.split()[1])
        print(currentTrack)
        clkLastState = GPIO.input(switches[0])
        Label(top, text=track, font=("MingLiU-ExtB", 12), bg = "black", fg = "light blue").place(x=mWIDTH/2.25, y=0)
        TrackVolumeLabel = Label(top, text='volume:{}'.format(UniVolume.get()), font=("MingLiU-ExtB", 12), bg = "black", fg = "light blue")
        TrackVolumeLabel.place(x=mWIDTH/2.25, y=0)
        #self.GUIUpdate(TrackVolumeLabel,top)
    def GUIUpdate(self,TrackVolumeLabel,top):
        global UniVolume
        TrackVolumeLabel.config(text = 'volume:{}'.format(UniVolume.get()))
        top.after(2000,self.GUIUpdate(TrackVolumeLabel,top))
    
def ReadingInput():
    global mute
    global TrackVolumeLabel
    global UniVolume
    volumeReading = 5
    mute_press = 0
    mute = IntVar(value=mute_press)
    UniVolume = IntVar(value=volumeReading)
    clkLastState = GPIO.input(switches[0])
    while(True):
        clkState = GPIO.input(switches[0])
        dtState = GPIO.input(switches[1])
        muteState = GPIO.input(switches[2])
        track1State = GPIO.input(switches[3])
        track2State = GPIO.input(switches[4])
        track3State = GPIO.input(switches[5])
        track4State = GPIO.input(switches[6])
        track5State = GPIO.input(switches[7])
        track6State = GPIO.input(switches[8])
        if track1State != 0:
            print('Opening Track 1')
            MainWin.VolumeGUICall(window,"track 1")
            sleep(.5)
        if track2State != 0:
            print('Opening Track 2')
            MainWin.VolumeGUICall(window,"track 2")
            sleep(.5)
        if track3State != 0:
            print('Opening Track 3')
            MainWin.VolumeGUICall(window,"track 3")
            sleep(.5)
        if track4State != 0:
            print('Opening Track 4')
            MainWin.VolumeGUICall(window,"track 4")
            sleep(.5)
        if track5State != 0:
            print('Opening Track 5')
            MainWin.VolumeGUICall(window,"track 5")
            sleep(.5)
        if track6State != 0:
            print('Opening Track 6')
            MainWin.VolumeGUICall(window,"track 6")
            sleep(.5)
        if volumeReading != 0:
            lastVolumeState = volumeReading
        if muteState != 0:
            if mute_press < 1:
                mute_press += 1
                GPIO.output(leds[2], True)
                volumeReading = 0
                print('muted')
                sleep(.25)
            else:
                if mute_press > 0:
                    mute_press -= 1
                GPIO.output(leds[2], False)
                volumeReading = lastVolumeState
                print('unmuted')
                sleep(.25)
        muteLastState = mute_press
        if clkState != clkLastState:
            if dtState != clkState:
                if volumeReading < 10:
                    volumeReading = volumeReading + 1
                GPIO.output(leds[0], True)
                GPIO.output(leds[1], False)
            else:
                if volumeReading > 0:
                    volumeReading = volumeReading - 1
                GPIO.output(leds[1], True)
                GPIO.output(leds[0], False)
        clkLastState = clkState
        mute.set(mute_press)
        UniVolume.set(volumeReading)
        try:
            TrackVolumeLabel.config(text = 'volume:{}'.format(UniVolume.get()))
        except:
            pass
        
############# MAIN CODE ###############
window = Tk()
if __name__ == '__main__':
    thread2 = Thread(target = MainWin, args = (window, "Amplicity Synthesizer"))
    thread = Thread(target = ReadingInput)
    thread2.start()
    thread.start()
    window.mainloop()
