from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
import random  # Used for random number generation
import thinkdsp  # Used for generating sine waves
from pydub import AudioSegment  # Used to convert sine waves into sound
from pydub.playback import play  # Used to play sound in python
import os

# fixme make sure to add a couple things into the GUI specifically (below)
'''
At the VERY beginning, BEFORE YOU EVEN MAKE THE GUI OR ANY PLACEHOLDER NOTES, allow the user to choose the timeSig (normally 4 for 4/4 time, but could be 7 for 7/4 time)
Otherwise, when the placeholder notes and whatnot are added, they won't be the right amount of beats. Then, instantiate the tracks with the correct timeSig.

Add a button on the measure chosen to run the clearMeasure function. This deletes all notes in the measure except a placeholder
to avoid errors.

You can make it so when you choose the measure from the main GUI, it passes in the track number and measure chosen to make
sure stuff gets added to the right spots. Just make it pass through those numbers in the lambda part, and add extra parameters to the called function to use them.
When calling the addNote function, pass in data gathered from entry boxes that the user puts values into. If one of the
boxes isn't filled, either use the default value (shown in the addNote definition), or give a warning box, your choice.

To handle volume, we can make it so there's a button on the main GUI that sets a loop in action to allow the user
to use the rotary encoder and displays the number it's at. When they then hit a confirm button, set the volume to that value.
We should be able to, at the end when we export, multiply each note by the volume of its track. Note that the volume parameter in the addNote
function still needs to be there for the user to change, as that determines the relative volume of each note to eath other. That way, you can have a loud track with
both louder and quieter notes, like a 3.0 note and a 1.0 note on a track set to volume 15.

I got rid of the playback function because of the weird delays, so don't miss it too much.
'''

PLAYBACK = 0  # determines whether or not the tracks play back in the script (causes weird delays)
METROID = 0  # create part of the metroid prime menu theme as a demo (currently 1 does that, 2 does some other test notes, and anything else does silence)


class Track:
    def __init__(self, volume=0.5, instrument=None, measures=16, timeSig=4):
        # measures is the base number of measures containing timeSig number of beats
        self.noteList = []
        self.noteNameList = []  # store the note names for plotting and deletion
        self.noteDurationList = []  # store the note durations to know how to fill out with blank spaces
        self.volume = volume
        self.instrument = instrument
        self.timeSig = timeSig
        self.measures = measures
        for i in range(measures):
            self.noteList.append([])
            self.noteNameList.append([])
            self.noteDurationList.append([])
        for i in range(len(self.noteList)):
            self.addNote(i, 0, 'O', "sawtooth", 0, self.timeSig, None, None)

    def addNote(self, measure, startBeat, noteName="A4", noteType="sine", amp=1, beats=1.0, filterType=None,
                cutoffType=None, filename="defaultFilename"):
        if noteName != 'O':
            totalLength = 0
            for i in range(len(self.noteList[measure])):
                if self.noteNameList[measure][i] != 'O':
                    totalLength += self.noteDurationList[measure][i]
            newLength = totalLength + beats
            print('newlength:', newLength)
            if newLength > self.timeSig:
                tkinter.messagebox.showerror("Note Length too Long", "The length of this note is longer than the measure can hold")  # fixme add this warning as pop up on gui upon return
                return

        # prompt user to create a new note with note attributes
        # get the values to put into this statement later from the gui
        if noteName != 'R' and noteName in noteFrequency:
            newNote = createNote(noteName=noteName, type=noteType, amp=amp, beats=beats, filter=filterType, cutoff=cutoffType, filename=filename)
            self.noteList[measure].insert(startBeat, newNote)
            self.noteNameList[measure].insert(startBeat, noteName)
            self.noteDurationList[measure].insert(startBeat, beats)
        elif noteName == 'R':
            restNote = createNote(amp = 0, beats = beats)
            self.noteList[measure].insert(startBeat, restNote)
            self.noteNameList[measure].insert(startBeat, 'R')
            self.noteDurationList[measure].insert(startBeat, beats)
        else:
            tkinter.messagebox.showerror("Invalid name", "That is neither a valid Note nor a Rest")


        # remove 'O' notes from list upon adding a note
        if len(self.noteNameList[measure]) == 2 and self.noteNameList[measure][0] == 'O':
            del self.noteNameList[measure][0]
            del self.noteList[measure][0]
            del self.noteDurationList[measure][0]

        # add blank notes in space left in measure (but only if note being added isn't blank)
        if noteName != 'O':
            self.addBlanks(measure)

    def clearMeasure(self, measure):
        # measure uses the list index
        self.noteList[measure] = []
        self.noteNameList[measure] = []
        self.noteDurationList[measure] = []
        self.addNote(measure, 0, 'O', "sawtooth", 0, self.timeSig, None, None)  # sets the measure to a silent note

    def deleteNote(self, measure, noteNumber):
        """Deletes the specified note at index noteNumber for the track's specified measure."""
        del self.noteList[measure][noteNumber]
        del self.noteDurationList[measure][noteNumber]
        del self.noteNameList[measure][noteNumber]


    def addBlanks(self, measure):
        """Adds blank notes to fill in the rest of the measure time for the specified measure of a specified track"""

        # clear previous blank notes
        if 'O' in self.noteNameList[measure]:
            O_Index = self.noteNameList[measure].index('O')
            del self.noteNameList[measure][O_Index]
            del self.noteDurationList[measure][O_Index]
            del self.noteList[measure][O_Index]

            print(self.noteNameList[measure])

        totalLength = 0
        for noteLength in self.noteDurationList[measure]:
            totalLength += noteLength  # sum up all the notes in the measure
        missingLength = self.timeSig - totalLength
        print('\n--------------------')
        print(missingLength)
        print(self.noteNameList[measure])

        if missingLength > 0:
            # create a blank note to fill in the missing time
            print('binga')
            self.addNote(measure, len(self.noteNameList), 'O', "sawtooth", 0, missingLength, None,
                         None)  # sets the measure to a silent note
        print('\n--------------------')

    def playBack(self):
        for measure in self.noteList:
            for note in measure:
                play(note)


# print(os.path.isfile('tmpkil32vrt.wav'))
trackList = []
global noteFrequency
noteFrequency = {"C0": 16.35, "Db0": 17.32, "D0": 18.35, "Eb0": 19.45,
                 "E0": 20.6, "F0": 21.83, "Gb0": 23.12, "G0": 24.5,
                 "Ab0": 25.96, "A0": 27.5, "Bb0": 29.14, "B0": 30.87,
                 "C1": 32.7, "Db1": 34.65, "D1": 36.71, "Eb1": 38.89,
                 "E1": 41.2, "F1": 43.65, "Gb1": 46.25, "G1": 49.00,
                 "Ab1": 51.91, "A1": 55.00, "Bb1": 58.27, "B1": 61.74,
                 "C2": 65.41, "Db2": 69.30, "D2": 73.42, "Eb2": 77.48,
                 "E2": 82.41, "F2": 87.31, "Gb2": 92.5, "G2": 98.00,
                 "Ab2": 103.83, "A2": 110.00, "Bb2": 116.54, "B2": 123.47,
                 "C3": 130.81, "Db3": 138.59, "D3": 146.83, "Eb3": 155.56,
                 "E3": 164.81, "F3": 174.61, "Gb3": 185.00, "G3": 196.00,
                 "Ab3": 207.65, "A3": 220.00, "Bb3": 233.08, "B3": 246.94,
                 "C4": 261.63, "Db4": 277.18, "D4": 293.66, "Eb4": 311.13,
                 "E4": 329.63, "F4": 349.23, "Gb4": 369.99, "G4": 392.00,
                 "Ab4": 415.30, "A4": 440.00, "Bb4": 446.16, "B4": 493.88,
                 "C5": 523.25, "Db5": 554.37, "D5": 587.33, "Eb5": 622.25,
                 "E5": 659.25, "F5": 698.46, "Gb5": 739.99, "G5": 783.99,
                 "Ab5": 830.61, "A5": 880.00, "Bb5": 932.33, "B5": 987.77,
                 "C6": 1046.50, "Db6": 1108.73, "D6": 1174.66, "Eb6": 1244.51,
                 "E6": 1318.51, "F6": 1396.91, "Gb6": 1479.98, "G6": 1567.98,
                 "Ab6": 1661.22, "A6": 1760.00, "Bb6": 1864.66, "B6": 1975.53,
                 "R": 0.00, "O": 0.00}  # O is for open. It is a blank space that doesn't make sound. R is for Rest.

# Generates a random set of coefficients to be used for Fourier Sound Synthesis
randomCoefficients = []
for i in range(0, 8):
    randomCoefficients.append(random.uniform(-1, 1))

# The coefficients represent the amplitude of the corresponding harmonic
fourierCoefficients = {
    "sine": [0, 1, 0, 0, 0, 0, 0, 0], "sawtooth": [0, 0.6366, 0, -0.2122, 0, 0.1273, 0, -0.0909],
    "trumpet": [0.1155, 0.3417, 0.1789, 0.1232, 0.0678, 0.0473, 0.0260, 0.0045, 0.0020], "random": randomCoefficients
}


# Actual sound synthesis part:
# Function that creates an AudioSegment of a certain note
# Amp is relative amplitude
# Beats is length of note relative to a quarter note at 120 BPM
# Filter can be low-pass or high-pass depending on the cutoff frequency given
# Filename doesn't really matter in this composition because I will be reading in the sound signal back into...
def createNote(noteName="A4", type="sine", amp=0.5, beats=1.0, filter=None, cutoff=None, filename="defaultFilename"):
    # Initializing values, let signal be empty first
    frequency = noteFrequency[noteName]
    duration = beats / 2
    signal = thinkdsp.SinSignal(freq=0)

    # Add harmonics to the signal according to their Fourier Synthesis Coefficients
    for i in range(0, 8):
        signal += thinkdsp.SinSignal(freq=frequency * i, amp=amp * fourierCoefficients[type][i], offset=0)
    # Convert signal into wave to .wav file to AudioSegment to be mixed and played by the program
    wave = signal.make_wave(duration=duration, start=0, framerate=44100)  # default framerate is 44100
    wave.write(filename=filename)
    audio = AudioSegment.from_wav(filename)
    # print("Creating note {} at {} for {} beats ###THERE WAS MORE TO THIS PRINT STATEMENT I JUST CANNOT SEE IT".format(noteName,str(frequency),str(beats)))
    # Adding filters
    if filter == "lowPass":
        audio = audio.low_pass_filter(cutoff)
        print("Applying Low-Pass Filter")
    if filter == "highPass":
        audio = audio.high_pass_filter(cutoff)
    return audio


def mixTracks(trackList, song_name):
    # determine where all tracks are blank (to prevent excessive silence at the end)
    lastMeasureIndex = 0
    for track in trackList:
        flag = 0
        for i in range(len(track.noteNameList) - 1, lastMeasureIndex - 1, -1):
            for j in range(len(track.noteNameList[i]) - 1, -1, -1):
                # print(i, j)
                # print(track.noteNameList[i], flag)
                if track.noteNameList[i][j] != 'O':
                    if i > lastMeasureIndex:
                        lastMeasureIndex = i
                        flag = 1
                        break
            if flag == 1:
                break

    trackWavs = []
    for track in trackList:
        track.noteList = track.noteList[0:lastMeasureIndex + 1]
        track.noteNameList = track.noteNameList[0:lastMeasureIndex + 1]
        print(track.noteList)
        print(track.noteNameList)
        print(track.noteDurationList)
        sound1 = track.noteList[0][0] + track.volume
        for measureNum in range(len(track.noteList)):
            if len(track.noteList[measureNum]) == 1 and measureNum == 0:  # if the first measure contains one note
                sound2 = 0  # 0 so that the only sound in measure 1 isn't doubled in amplitude
                newSound = sound1 + sound2
                sound1 = newSound
            elif len(track.noteList[measureNum]) == 1:  # if non-first measure is only one note long
                sound2 = track.noteList[measureNum][0] + track.volume
                newSound = sound1 + sound2
                sound1 = newSound
            elif measureNum == 0:  # cover for rest of 1st measure cases
                for note in range(1, len(track.noteList[measureNum])):
                    sound2 = track.noteList[measureNum][note] + track.volume
                    newSound = sound1 + sound2
                    sound1 = newSound
            else:
                for note in range(0, len(track.noteList[measureNum])):
                    sound2 = track.noteList[measureNum][note] + track.volume
                    newSound = sound1 + sound2
                    sound1 = newSound
        s = 'TrackTestNum' + str(trackList.index(track)) + '.wav'
        newSound.export(s, format='wav')
        trackWavs.append(newSound)

    # print(trackWavs)
    track1 = trackWavs[0]
    for i in range(1, len(trackWavs)):
        track2 = trackWavs[i]
        combinedTrack = track1.overlay(track2, position=0)
        track1 = combinedTrack
    combinedTrack.export('{}.wav'.format(song_name), format='wav')





WIDTH = 1200
HEIGHT = 600
mWIDTH = 800
mHEIGHT = 500


class MainWin(Canvas):
    def __init__(self, master, name, time_sig, track_list):
        Canvas.__init__(self, master, bg = "black")
        self.pack(fill = BOTH, expand = 1)
        self.song_name = name
        self.time_sig = time_sig
        self.track_list = track_list
        self.copiedMeasureNames = ''  # placeholder to copy and paste the note names
        self.copiedMeasureLengths = ''  # placeholder to copy and paste the note durations
        self.copiedMeasure = []  # placeholder to copy and paste the actual note objects

    def setUP(self):
        # vol buttons
        t1vol = Button(self.master, text = "T1 vol", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.TrackVolGUICall("T1 Vol"))
        t1vol.place(bordermode = OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6))
        t2vol = Button(self.master, text = "T2 vol", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.TrackVolGUICall("T2 Vol"))
        t2vol.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y = 100)
        t3vol = Button(self.master, text = "T3 vol", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.TrackVolGUICall("T3 Vol"))
        t3vol.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y = 200)
        t4vol = Button(self.master, text = "T4 vol", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.TrackVolGUICall("T4 Vol"))
        t4vol.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y = 300)
        t5vol = Button(self.master, text = "T5 vol", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.TrackVolGUICall("T5 Vol"))
        t5vol.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y = 400)
        t6vol = Button(self.master, text = "T6 vol", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.TrackVolGUICall("T6 Vol"))
        t6vol.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y = 500)

        #track display
        t1disp = Label(self.master, text = "Track 1", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6))
        t1disp.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), x = int((WIDTH/18)+(1/3)))
        t2disp = Label(self.master, text = "Track 2", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6))
        t2disp.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y = 100, x = int((WIDTH/18)+(1/3)))
        t3disp = Label(self.master, text = "Track 3", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6))
        t3disp.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y= 200, x = int((WIDTH/18)+(1/3)))
        t4disp = Label(self.master, text = "Track 4", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6))
        t4disp.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y= 300, x = int((WIDTH/18)+(1/3)))
        t5disp = Label(self.master, text = "Track 5", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6))
        t5disp.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y= 400, x = int((WIDTH/18)+(1/3)))
        t6disp = Label(self.master, text = "Track 6", font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black", width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6))
        t6disp.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), y = 500, x = int((WIDTH/18)+(1/3)))

        #t1 measures
        t1m1 = Button(self.master, text = "t1m1", fg = "sky blue", bg = "black", width = int(WIDTH/2), height = int(HEIGHT/6), command = lambda:self.MeasureGUICall("t1m1", 1, 1))
        t1m1.place(bordermode=OUTSIDE, width = int((WIDTH/18)+(1/3)), height = int(HEIGHT/6), x = int((WIDTH/18)+(1/3))*2)
        t1m2 = Button(self.master, text="t1m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m2", 1, 2))
        t1m2.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3))*3)
        t1m3 = Button(self.master, text="t1m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m3", 1, 3))
        t1m3.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3))*4)
        t1m4 = Button(self.master, text="t1m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m4", 1, 4))
        t1m4.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3))*5)
        t1m5 = Button(self.master, text="t1m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m5", 1, 5))
        t1m5.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 6)
        t1m6 = Button(self.master, text="t1m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m6", 1, 6))
        t1m6.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 7)
        t1m7 = Button(self.master, text="t1m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m7", 1, 7))
        t1m7.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3))*8)
        t1m8 = Button(self.master, text="t1m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m8", 1, 8))
        t1m8.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 9)
        t1m9 = Button(self.master, text="t1m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m9", 1, 9))
        t1m9.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 10)
        t1m10 = Button(self.master, text="t1m10", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m10", 1, 10))
        t1m10.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 11)
        t1m11 = Button(self.master, text="t1m11", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m11", 1, 11))
        t1m11.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 12)
        t1m12 = Button(self.master, text="t1m12", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m12", 1, 12))
        t1m12.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 13)
        t1m13 = Button(self.master, text="t1m13", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m13", 1, 13))
        t1m13.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 14)
        t1m14 = Button(self.master, text="t1m14", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m14", 1, 14))
        t1m14.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 15)
        t1m15 = Button(self.master, text="t1m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m15", 1, 15))
        t1m15.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 16)
        t1m16 = Button(self.master, text="t1m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t1m16", 1, 16))
        t1m16.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 17)

        # t2 measures
        t2m1 = Button(self.master, text="t2m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m1", 2, 1))
        t2m1.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3))*2, y = (HEIGHT / 6))
        t2m2 = Button(self.master, text="t2m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m2", 2, 2))
        t2m2.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 3, y = (HEIGHT / 6))
        t2m3 = Button(self.master, text="t2m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m3", 2, 3))
        t2m3.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 4, y = (HEIGHT / 6))
        t2m4 = Button(self.master, text="t2m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m4", 2, 4))
        t2m4.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 5, y = (HEIGHT / 6))
        t2m5 = Button(self.master, text="t2m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m5", 2, 5))
        t2m5.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 6, y = (HEIGHT / 6))
        t2m6 = Button(self.master, text="t2m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m6", 2, 6))
        t2m6.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 7, y = (HEIGHT / 6))
        t2m7 = Button(self.master, text="t2m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m7", 2, 7))
        t2m7.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 8, y = (HEIGHT / 6))
        t2m8 = Button(self.master, text="t2m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m8", 2, 8))
        t2m8.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 9, y = (HEIGHT / 6))
        t2m9 = Button(self.master, text="t2m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m9", 2, 9))
        t2m9.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 10, y = (HEIGHT / 6))
        t2m10 = Button(self.master, text="t2m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m10", 2, 10))
        t2m10.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 11, y = (HEIGHT / 6))
        t2m11 = Button(self.master, text="t2m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m11", 2, 11))
        t2m11.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 12, y = (HEIGHT / 6))
        t2m12 = Button(self.master, text="t2m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m12", 2, 12))
        t2m12.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 13, y = (HEIGHT / 6))
        t2m13 = Button(self.master, text="t2m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m13", 2, 13))
        t2m13.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 14, y = (HEIGHT / 6))
        t2m14 = Button(self.master, text="t2m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m14", 2, 14))
        t2m14.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 15, y = (HEIGHT / 6))
        t2m15 = Button(self.master, text="t2m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m15", 2, 15))
        t2m15.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 16, y = (HEIGHT / 6))
        t2m16 = Button(self.master, text="t2m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t2m16", 2, 16))
        t2m16.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 17, y = (HEIGHT / 6))

        # t2 measures
        t3m1 = Button(self.master, text="t3m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m1", 3, 1))
        t3m1.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3))*2, y = (HEIGHT / 6)*2)
        t3m2 = Button(self.master, text="t3m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m2", 3, 2))
        t3m2.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 3, y = (HEIGHT / 6)*2)
        t3m3 = Button(self.master, text="t3m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m3", 3, 3))
        t3m3.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 4, y = (HEIGHT / 6)*2)
        t3m4 = Button(self.master, text="t3m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m4", 3, 4))
        t3m4.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 5, y = (HEIGHT / 6)*2)
        t3m5 = Button(self.master, text="t3m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m5",3, 5))
        t3m5.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 6, y = (HEIGHT / 6)*2)
        t3m6 = Button(self.master, text="t3m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m6", 3, 6))
        t3m6.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 7, y = (HEIGHT / 6)*2)
        t3m7 = Button(self.master, text="t3m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m7", 3, 7))
        t3m7.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 8, y = (HEIGHT / 6)*2)
        t3m8 = Button(self.master, text="t3m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m8", 3, 8))
        t3m8.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 9, y = (HEIGHT / 6)*2)
        t3m9 = Button(self.master, text="t3m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m9", 3, 9))
        t3m9.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 10, y = (HEIGHT / 6)*2)
        t3m10 = Button(self.master, text="t3m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m10", 3, 10))
        t3m10.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 11, y = (HEIGHT / 6)*2)
        t3m11 = Button(self.master, text="t3m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m11", 3, 11))
        t3m11.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 12, y = (HEIGHT / 6)*2)
        t3m12 = Button(self.master, text="t3m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m12", 3, 12))
        t3m12.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 13, y = (HEIGHT / 6)*2)
        t3m13 = Button(self.master, text="t3m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m13", 3, 13))
        t3m13.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 14, y = (HEIGHT / 6)*2)
        t3m14 = Button(self.master, text="t3m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m14", 3, 14))
        t3m14.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 15, y = (HEIGHT / 6)*2)
        t3m15 = Button(self.master, text="t3m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m15", 3, 15))
        t3m15.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 16, y = (HEIGHT / 6)*2)
        t3m16 = Button(self.master, text="t3m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t3m16", 3, 16))
        t3m16.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 17, y = (HEIGHT / 6)*2)

        # t4 measures
        t4m1 = Button(self.master, text="t4m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m1", 4, 1))
        t4m1.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3))*2, y = (HEIGHT / 6)*3)
        t4m2 = Button(self.master, text="t4m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m2", 4, 2))
        t4m2.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 3, y = (HEIGHT / 6)*3)
        t4m3 = Button(self.master, text="t4m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m3", 4, 3))
        t4m3.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 4, y = (HEIGHT / 6)*3)
        t4m4 = Button(self.master, text="t4m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m4", 4, 4))
        t4m4.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 5, y = (HEIGHT / 6)*3)
        t4m5 = Button(self.master, text="t4m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m5", 4, 5))
        t4m5.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 6, y = (HEIGHT / 6)*3)
        t4m6 = Button(self.master, text="t4m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m6", 4, 6))
        t4m6.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 7, y = (HEIGHT / 6)*3)
        t4m7 = Button(self.master, text="t4m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m7", 4, 7))
        t4m7.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 8, y = (HEIGHT / 6)*3)
        t4m8 = Button(self.master, text="t4m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m8", 4, 8))
        t4m8.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 9, y = (HEIGHT / 6)*3)
        t4m9 = Button(self.master, text="t4m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m9", 4, 9))
        t4m9.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 10, y = (HEIGHT / 6)*3)
        t4m10 = Button(self.master, text="t4m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m10", 4, 10))
        t4m10.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 11, y = (HEIGHT / 6)*3)
        t4m11 = Button(self.master, text="t4m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m11", 4, 11))
        t4m11.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 12, y = (HEIGHT / 6)*3)
        t4m12 = Button(self.master, text="t4m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m12", 4, 12))
        t4m12.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 13, y = (HEIGHT / 6)*3)
        t4m13 = Button(self.master, text="t4m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m13", 4, 13))
        t4m13.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 14, y = (HEIGHT / 6)*3)
        t4m14 = Button(self.master, text="t4m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m14", 4, 14))
        t4m14.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 15, y = (HEIGHT / 6)*3)
        t4m15 = Button(self.master, text="t4m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m15", 4, 15))
        t4m15.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 16, y = (HEIGHT / 6)*3)
        t4m16 = Button(self.master, text="t4m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t4m16", 4, 16))
        t4m16.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 17, y = (HEIGHT / 6)*3)

        # t5 measures
        t5m1 = Button(self.master, text="t5m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m1", 5, 1))
        t5m1.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3))*2, y = (HEIGHT / 6)*4)
        t5m2 = Button(self.master, text="t5m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m2", 5, 2))
        t5m2.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 3, y = (HEIGHT / 6)*4)
        t5m3 = Button(self.master, text="t5m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m3", 5, 3))
        t5m3.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 4, y = (HEIGHT / 6)*4)
        t5m4 = Button(self.master, text="t5m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m4", 5, 4))
        t5m4.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 5, y = (HEIGHT / 6)*4)
        t5m5 = Button(self.master, text="t5m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m5", 5, 5))
        t5m5.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 6, y = (HEIGHT / 6)*4)
        t5m6 = Button(self.master, text="t5m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m6", 5, 6))
        t5m6.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 7, y = (HEIGHT / 6)*4)
        t5m7 = Button(self.master, text="t5m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m7", 5, 7))
        t5m7.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 8, y = (HEIGHT / 6)*4)
        t5m8 = Button(self.master, text="t5m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m8", 5, 8))
        t5m8.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 9, y = (HEIGHT / 6)*4)
        t5m9 = Button(self.master, text="t5m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m9", 5, 9))
        t5m9.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 10, y = (HEIGHT / 6)*4)
        t5m10 = Button(self.master, text="t5m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m10", 5, 10))
        t5m10.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 11, y = (HEIGHT / 6)*4)
        t5m11 = Button(self.master, text="t5m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m11", 5, 11))
        t5m11.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 12, y = (HEIGHT / 6)*4)
        t5m12 = Button(self.master, text="t5m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m12", 5, 12))
        t5m12.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 13, y = (HEIGHT / 6)*4)
        t5m13 = Button(self.master, text="t5m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m13", 5, 13))
        t5m13.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 14, y = (HEIGHT / 6)*4)
        t5m14 = Button(self.master, text="t5m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m14", 5, 14))
        t5m14.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 15, y = (HEIGHT / 6)*4)
        t5m15 = Button(self.master, text="t5m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m15", 5, 15))
        t5m15.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 16, y = (HEIGHT / 6)*4)
        t5m16 = Button(self.master, text="t5m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t5m16", 5, 16))
        t5m16.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 17, y = (HEIGHT / 6)*4)

        # t6 measures
        t6m1 = Button(self.master, text="t6m1", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m1", 6, 1))
        t6m1.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3))*2, y = (HEIGHT / 6)*5)
        t6m2 = Button(self.master, text="t6m2", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m2", 6, 2))
        t6m2.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 3, y = (HEIGHT / 6)*5)
        t6m3 = Button(self.master, text="t6m3", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m3", 6, 3))
        t6m3.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 4, y = (HEIGHT / 6)*5)
        t6m4 = Button(self.master, text="t6m4", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m4", 6, 4))
        t6m4.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 5, y = (HEIGHT / 6)*5)
        t6m5 = Button(self.master, text="t6m5", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m5", 6, 5))
        t6m5.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 6, y = (HEIGHT / 6)*5)
        t6m6 = Button(self.master, text="t6m6", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m6", 6, 6))
        t6m6.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 7, y = (HEIGHT / 6)*5)
        t6m7 = Button(self.master, text="t6m7", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m7", 6, 7))
        t6m7.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 8, y = (HEIGHT / 6)*5)
        t6m8 = Button(self.master, text="t6m8", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m8", 6, 8))
        t6m8.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 9, y = (HEIGHT / 6)*5)
        t6m9 = Button(self.master, text="t6m9", fg="sky blue", bg="black", width=int(WIDTH / 2), height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m9", 6, 9))
        t6m9.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 10, y = (HEIGHT / 6)*5)
        t6m10 = Button(self.master, text="t6m10", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m10", 6, 10))
        t6m10.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 11, y = (HEIGHT / 6)*5)
        t6m11 = Button(self.master, text="t6m11", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m11", 6, 11))
        t6m11.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 12, y = (HEIGHT / 6)*5)
        t6m12 = Button(self.master, text="t6m12", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m12", 6, 12))
        t6m12.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 13, y = (HEIGHT / 6)*5)
        t6m13 = Button(self.master, text="t6m13", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m13", 6, 13))
        t6m13.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 14, y = (HEIGHT / 6)*5)
        t6m14 = Button(self.master, text="t6m14", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m14", 6, 14))
        t6m14.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 15, y = (HEIGHT / 6)*5)
        t6m15 = Button(self.master, text="t6m15", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m15", 6, 15))
        t6m15.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 16, y = (HEIGHT / 6)*5)
        t6m16 = Button(self.master, text="t6m16", fg="sky blue", bg="black", width=int(WIDTH / 2),height=int(HEIGHT / 6), command = lambda:self.MeasureGUICall("t6m16", 6, 16))
        t6m16.place(bordermode=OUTSIDE, width=int((WIDTH / 18)+(1/3)), height=int(HEIGHT / 6), x=int((WIDTH / 18)+(1/3)) * 17, y = (HEIGHT / 6)*5)

        #Beats/Measure, Export button, & help
        bPerMes_label = Label(self.master, text = "Beats/Measure: {}".format(self.time_sig), font = ("MingLiU-ExtB", 12), fg = "turquoise1", bg = "black")
        bPerMes_label.place(width=int(WIDTH/6)*4, height=40, y = HEIGHT)
        help_doc = Button(self.master, text="HELP", fg="turquoise1", bg="black", font = ("MingLiU-ExtB", 12), command = self.helpCall)
        help_doc.place(width=int(WIDTH/6), height=40, y = HEIGHT, x = int(WIDTH/6)*4)
        export_button = Button(self.master, text= "Export Song", fg = "turquoise1", bg = "black", font = ("MingLiU-ExtB", 12), command = self.exportCall)
        export_button.place(width=int(WIDTH/6), height = 40, y = HEIGHT, x = int(WIDTH/6)*5)

    def helpCall(self):
        #fixme Please put in some correct doccumentation here
        tkinter.messagebox.showinfo("Synth Documentation", "Place holder info")

    #fixme Place the export method call here
    def exportCall(self):
        mixTracks(self.track_list, self.song_name)
        tkinter.messagebox.showinfo("Export Completion", "Your song is done exporting")

    def MeasureGUICall(self, name, track, mes):
        top = Toplevel(window, bg = "black")
        top.attributes("-topmost", True)
        top.geometry("{}x{}".format(mWIDTH, mHEIGHT))
        top.title(name)
        Label(top, text=name, font=("MingLiU-ExtB", 12), bg = "black", fg = "light blue").place(width=mWIDTH, height=int(mHEIGHT/12))

        #Labels and Text Entries
        N_N = StringVar()
        Num_B = StringVar()
        volu = StringVar()
        B_start = StringVar()

        note_name_label = Label(top, text = "Note Name", font=("MingLiU-ExtB", 12), bg = "black", fg = "light blue")
        note_name_label.place(width=int(mWIDTH/2), height=int(mHEIGHT/12), y = int(mHEIGHT/12))
        note_name = Entry(top, textvariable= N_N, bg = "gray", fg = "blue", font=("MingLiU-ExtB", 12))
        note_name.place(width=int(mWIDTH/2)-20, height=int(mHEIGHT/12)-20, y = (int(mHEIGHT/12)*2)+10, x=10)
        note_name.insert(END, "C4")

        number_beats_label = Label(top, text="Number of Beats", font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        number_beats_label.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12), x=int(mWIDTH / 2))
        number_beats = Entry(top, textvariable=Num_B, bg="gray", fg="blue", font=("MingLiU-ExtB", 12))
        number_beats.place(width=int(mWIDTH / 2)-20, height=int(mHEIGHT/12)-20, y=(int(mHEIGHT/12) * 2)+10, x=int(mWIDTH / 2)+10)
        number_beats.insert(END, "1")

        volume_label = Label(top, text="Volume", font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        volume_label.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12)*3)
        note_vol = Entry(top, textvariable=volu, bg="gray", fg="blue", font=("MingLiU-ExtB", 12))
        note_vol.place(width=int(mWIDTH / 2)-20, height=int(mHEIGHT/12)-20, y=(int(mHEIGHT/12) * 4)+10, x=10)
        note_vol.insert(END, "0.5")

        beat_start_label = Label(top, text="Note Number", font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        beat_start_label.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12)*3, x=int(mWIDTH / 2))
        self.start_beat = Entry(top, textvariable=B_start, bg="gray", fg="blue", font=("MingLiU-ExtB", 12))
        self.start_beat.place(width=int(mWIDTH / 2)-20, height=int(mHEIGHT/12)-20, y=(int(mHEIGHT/12) * 4)+10, x=int(mWIDTH / 2)+10)

        self.start_beat.insert(END, str(len(trackDict[str(track)].noteList[mes-1])))  # fixme jwebfakwejbfakjgbawe.kfbae.kjfbaw.kjvba.KEjfbaw.kejfbwae.kjfbqer.kgjvbre
        #self.start_beat.insert(END, len(trackDict[str(track)].noteList[mes]))

        #displays current notes with respective lengths
        names_list_label = Label(top, text = "Notes in Order:", font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        names_list_label.place(width= int(mWIDTH/2), height= int(mHEIGHT/12), y = int(mHEIGHT/12)*7)
        self.names_list = Label(top, text = trackDict[str(track)].noteNameList[mes-1], font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        self.names_list.place(width = int(mWIDTH/2), height= int(mHEIGHT/12), y = int(mHEIGHT/12)*7, x= int(mWIDTH/2))
        lengths_list_label = Label(top, text = "Note Lengths in Order:", font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        lengths_list_label.place(width= int(mWIDTH/2), height= int(mHEIGHT/12), y = int(mHEIGHT/12)*8)
        self.lengths_list = Label(top, text=trackDict[str(track)].noteDurationList[mes - 1], font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        self.lengths_list.place(width=int(mWIDTH/2), height=int(mHEIGHT/12), y=int(mHEIGHT/12) * 8, x= int(mWIDTH/2))

        # add note, clear note, and delete note buttons
        add_note_button = Button(top, text = "Add Note", font=("MingLiU-ExtB", 12), bg="black", fg="light blue", command = lambda:self.noteAdd(track, mes, N_N.get(), Num_B.get(), volu.get(), B_start.get()))
        add_note_button.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12) * 5)
        add_note_button.bind("<Return>", lambda event:self.noteAdd(track, mes, N_N.get(), Num_B.get(), volu.get(), B_start.get()))
        add_note_button.focus()

        clear_measure_button = Button(top, text="Clear_Measure", font=("MingLiU-ExtB", 12), bg="black", fg="light blue", command = lambda:self.measureClear(track, mes))
        clear_measure_button.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12) * 5, x=int(mWIDTH / 2))

        delete_note_button = Button(top, text="Delete Note", font=("MingLiU-ExtB", 12), bg="black", fg="light blue", command = lambda:self.noteDelete(track, mes, B_start.get()))
        delete_note_button.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12) * 6)

        # copy and paste buttons and information
        copy_measure_button = Button(top, text="Copy Measure", font=("MingLiU-ExtB", 12), bg="black", fg="light blue", command = lambda:self.measureCopy(track, mes))
        copy_measure_button.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12) * 9)

        paste_measure_button = Button(top, text="Paste Measure", font=("MingLiU-ExtB", 12), bg="black", fg="light blue", command = lambda:self.measurePaste(track, mes))
        paste_measure_button.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12) * 9, x=int(mWIDTH / 2))

        copied_measure_label = Label(top, text="Copied Notes: ", font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        copied_measure_label.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12) * 10)
        self.copied_measure_names = Label(top, text = self.copiedMeasureNames, font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        self.copied_measure_names.place(width = int(mWIDTH/2), height= int(mHEIGHT/12), y = int(mHEIGHT/12)*10, x= int(mWIDTH/2))

        copied_lengths_label = Label(top, text="Copied Lengths: ", font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        copied_lengths_label.place(width=int(mWIDTH / 2), height=int(mHEIGHT/12), y=int(mHEIGHT/12) * 11)
        self.copied_measure_lengths = Label(top, text = self.copiedMeasureLengths, font=("MingLiU-ExtB", 12), bg="black", fg="light blue")
        self.copied_measure_lengths.place(width = int(mWIDTH/2), height= int(mHEIGHT/12), y = int(mHEIGHT/12)*11, x= int(mWIDTH/2))



    #fixme track vol here V
    def TrackVolGUICall(self, track):
        top = Toplevel(window, bg = "black")
        top.geometry("{}x{}".format(mWIDTH, mHEIGHT))
        top.title(track)
        Label(top, text=track, font=("MingLiU-ExtB", 12), bg = "black", fg = "light blue").place(width=mWIDTH, height=int(mHEIGHT/6))

    def noteAdd(self, track, measure, note_name, note_length, note_vol, note_start):
        trackDict[str(track)].addNote(measure-1, int(note_start)-1, note_name.capitalize(), "sine", float(note_vol), float(note_length))
        self.names_list["text"] = trackDict[str(track)].noteNameList[measure-1]
        self.lengths_list["text"] = trackDict[str(track)].noteDurationList[measure-1]
        #self.start_beat.delete(0, END)
        #self.start_beat.insert(0, len(trackDict[str(track)].noteList[measure]))
        self.start_beat.delete(0, END)
        self.start_beat.insert(0, str(len(trackDict[str(track)].noteList[measure - 1])))


    def measureClear(self, track, measure):
        trackDict[str(track)].clearMeasure(measure-1)
        self.names_list["text"] = trackDict[str(track)].noteNameList[measure-1]
        self.lengths_list["text"] = trackDict[str(track)].noteDurationList[measure-1]
        self.start_beat.delete(0, END)
        self.start_beat.insert(0, str(len(trackDict[str(track)].noteList[measure - 1])))

    def noteDelete(self, track, measure, noteNumber):
        # prevent user from deleting 'O' Notes
        if trackDict[str(track)].noteNameList[measure-1][int(noteNumber)-1] != 'O':
            trackDict[str(track)].deleteNote(measure-1, int(noteNumber)-1)
            trackDict[str(track)].addBlanks(measure-1)
            self.names_list["text"] = trackDict[str(track)].noteNameList[measure-1]
            self.lengths_list["text"] = trackDict[str(track)].noteDurationList[measure-1]
        else:
            tkinter.messagebox.showerror("Deletion Error",
            "Unable to Delete 'O' Placeholder Notes. They automatically change based on other note changes.")

    def measureCopy(self, track, measure):
        self.copiedMeasureNames = trackDict[str(track)].noteNameList[measure - 1]  # copy the names of the current measure
        self.copiedMeasureLengths = trackDict[str(track)].noteDurationList[measure - 1]  # copy the lengths of the current measure
        self.copiedMeasure = trackDict[str(track)].noteList[measure - 1]  # copy the note objects
        tkinter.messagebox.showinfo("Copy Notice", "Current Measure Has Been Copied!")

        # update GUI to reflect copied measure
        self.copied_measure_names['text'] = self.copiedMeasureNames
        self.copied_measure_lengths['text'] = self.copiedMeasureLengths

    def measurePaste(self, track, measure):
        trackDict[str(track)].noteNameList[measure - 1] = self.copiedMeasureNames  # paste current measure names to current measure
        trackDict[str(track)].noteDurationList[measure - 1] = self.copiedMeasureLengths  # paste current measure lengths to current measure
        trackDict[str(track)].noteList[measure - 1] = self.copiedMeasure # paste copied note objects

        # update GUI to show new notes
        self.names_list["text"] = trackDict[str(track)].noteNameList[measure - 1]
        self.lengths_list["text"] = trackDict[str(track)].noteDurationList[measure - 1]

        # update Note Number for convenience
        # fixme the Note Number status isn't updating and you can add notes that cause negative measure time tobe remaining after
        self.start_beat.delete(0, END)
        self.start_beat.insert(0, str(len(trackDict[str(track)].noteList[measure - 1])))


############# MAIN CODE
window = Tk()
song_name = tkinter.simpledialog.askstring("Song Name", "Enter name of new song")
signature = tkinter.simpledialog.askinteger("Time Signature", "Please enter number of beats per measure")

# initialize  tracks
track1 = Track(timeSig = signature)
track2 = Track(timeSig = signature)
track3 = Track(timeSig = signature)
track4 = Track(timeSig = signature)
track5 = Track(timeSig = signature)
track6 = Track(timeSig = signature)

trackDict = { "1": track1, "2": track2, "3": track3, "4": track4, "5": track5, "6": track6}
track_list = [track1, track2, track3, track4, track5, track6]


window.geometry("{}x{}".format(WIDTH, HEIGHT+40))
window.title("Amplicity Synthesizer - " + song_name)
mainwin = MainWin(window, song_name, signature, track_list)
mainwin.setUP()
window.mainloop()
