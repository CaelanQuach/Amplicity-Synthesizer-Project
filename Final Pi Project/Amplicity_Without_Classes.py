import random #Used for random number generation
import thinkdsp #Used for generating sine waves
from pydub import AudioSegment #Used to convert sine waves into sound
from pydub.playback import play #Used to play sound in python
import os

#fixme make sure to add a couple things into the GUI specifically (below)
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
METROID = 1  # create part of the metroid prime menu theme as a demo (currently 1 does that, 2 does some other test notes, and anything else does silence)

class Track:
    def __init__(self, volume = 0.5, instrument=None, measures=16, timeSig = 4):
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
    
    def addNote(self, measure, startBeat, noteName="A4", noteType = "sine", amp = 0.5, beats = 1.0, filterType = None, cutoffType = None, filename="defaultFilename"):
        if noteName != 'O':
            totalLength = 0
            for i in range(len(self.noteList[measure])):
                if self.noteNameList[measure][i] != 'O':
                    totalLength += self.noteDurationList[measure][i]
            newLength = totalLength + beats
            print('newlength:', newLength)
            if newLength > self.timeSig:
                print(
                    '\n--------------------\n\n\n\nError: note to add is too long\n\n\n\n--------------------\n')  # fixme add this warning as pop up on gui upon return
                return

        # prompt user to create a new note with note attributes
        # get the values to put into this statement later from the gui
        newNote = createNote(noteName=noteName, type = noteType, amp = amp, beats = beats, filter = filterType, cutoff = cutoffType, filename=filename)
        self.noteList[measure].insert(startBeat, newNote)
        self.noteNameList[measure].insert(startBeat, noteName)
        self.noteDurationList[measure].insert(startBeat, beats)
        
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

    def addBlanks(self, measure):
        '''Adds blank notes to fill in the rest of the measure time for the specified measure of a specified track'''

        # clear previous blank notes
        listToClear = []
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
            self.addNote(measure, len(self.noteNameList), 'O', "sawtooth", 0, missingLength, None, None)  # sets the measure to a silent note
        print('\n--------------------')


    def playBack(self):
        for measure in self.noteList:
            for note in measure:
                play(note)
            
            
#print(os.path.isfile('tmpkil32vrt.wav'))
trackList = []

noteFrequency = {"C0": 16.35,"Db0": 17.32,"D0": 18.35,"Eb0": 19.45,
                 "E0": 20.6,"F0": 21.83,"Gb0": 23.12,"G0": 24.5,
                 "Ab0": 25.96,"A0": 27.5,"Bb0": 29.14,"B0": 30.87,
                 "C1": 32.7,"Db1": 34.65,"D1": 36.71,"Eb1": 38.89,
                 "E1": 41.2,"F1": 43.65,"Gb1": 46.25,"G1": 49.00,
                 "Ab1": 51.91,"A1": 55.00,"Bb1": 58.27,"B1": 61.74,
                 "C2": 65.41,"Db2": 69.30,"D2": 73.42,"Eb2": 77.48,
                 "E2": 82.41,"F2": 87.31,"Gb2": 92.5,"G2": 98.00,
                 "Ab2": 103.83,"A2": 110.00,"Bb2": 116.54,"B2": 123.47,
                 "C3": 130.81,"Db3": 138.59,"D3": 146.83,"Eb3": 155.56,
                 "E3": 164.81,"F3": 174.61,"Gb3": 185.00,"G3": 196.00,
                 "Ab3": 207.65,"A3": 220.00,"Bb3": 233.08,"B3": 246.94,
                 "C4": 261.63,"Db4": 277.18,"D4": 293.66,"Eb4": 311.13,
                 "E4": 329.63,"F4": 349.23,"Gb4": 369.99,"G4": 392.00,
                 "Ab4": 415.30,"A4": 440.00,"Bb4": 446.16,"B4": 493.88,
                 "C5": 523.25,"Db5": 554.37,"D5": 587.33,"Eb5": 622.25,
                 "E5": 659.25,"F5": 698.46,"Gb5": 739.99,"G5": 783.99,
                 "Ab5": 830.61,"A5": 880.00,"Bb5": 932.33,"B5": 987.77,
                 "C6": 1046.50, "Db6": 1108.73, "D6": 1174.66, "Eb6": 1244.51,
                 "E6": 1318.51, "F6": 1396.91, "Gb6": 1479.98, "G6": 1567.98,
                 "Ab6": 1661.22, "A6": 1760.00, "Bb6": 1864.66, "B6": 1975.53,
                 "R": 0.00, "O": 0.00}  # O is for open. It is a blank space that doesn't make sound. R is for Rest.

#Generates a random set of coefficients to be used for Fourier Sound Synthesis
randomCoefficients = []
for i in range(0,8):
    randomCoefficients.append(random.uniform(-1,1))

#The coefficients represent the amplitude of the corresponding harmonic
fourierCoefficients = {
    "sine": [0,1,0,0,0,0,0,0],"sawtooth":[0,0.6366,0,-0.2122,0,0.1273,0,-0.0909],
    "trumpet":[0.1155,0.3417,0.1789,0.1232,0.0678,0.0473,0.0260,0.0045,0.0020], "random": randomCoefficients
}
#Actual sound synthesis part:
#Function that creates an AudioSegment of a certain note
#Amp is relative amplitude
#Beats is length of note relative to a quarter note at 120 BPM
#Filter can be low-pass or high-pass depending on the cutoff frequency given
#Filename doesn't really matter in this composition because I will be reading in the sound signal back into...
def createNote(noteName="A4", type = "sine", amp = 0.5, beats = 1.0, filter = None, cutoff = None, filename="defaultFilename"):
    #Initializing values, let signal be empty first
    frequency = noteFrequency[noteName]
    duration = beats / 2
    signal = thinkdsp.SinSignal(freq=0)

    #Add harmonics to the signal according to their Fourier Synthesis Coefficients
    for i in range(0,8):
        signal += thinkdsp.SinSignal(freq=frequency*i,amp=amp*fourierCoefficients[type][i], offset=0)
    #Convert signal into wave to .wav file to AudioSegment to be mixed and played by the program
    wave = signal.make_wave(duration=duration, start=0, framerate=44100)  # default framerate is 44100
    wave.write(filename=filename)
    audio = AudioSegment.from_wav(filename)
    #print("Creating note {} at {} for {} beats ###THERE WAS MORE TO THIS PRINT STATEMENT I JUST CANNOT SEE IT".format(noteName,str(frequency),str(beats)))
    #Adding filters
    if filter == "lowPass":
        audio = audio.low_pass_filter(cutoff)
        print("Applying Low-Pass Filter")
    if filter == "highPass":
        audio = audio.high_pass_filter(cutoff)
    return audio


def mixTracks(traskList):
    pass





#Example Notes


# initialize 5 tracks
track1 = Track()
track2 = Track()
track3 = Track()
track4 = Track()
track5 = Track()


# sample song
if METROID:
    track1.timeSig = 6
    track2.timeSig = 6
    track3.timeSig = 6
    track4.timeSig = 6
    track5.timeSig = 6
    # line 1 omitted
    # line 2
    track1.addNote(0, 0, "A5", "sine", 1.0, 3.0, None, None)
    track1.addNote(0, 1, "G5", "sine", 1.0, 1.0, None, None)
    track1.addNote(0, 2, "C6", "sine", 1.0, 1.0, None, None)
    track1.addNote(0, 3, "E5", "sine", 1.0, 1.0, None, None)

    track2.addNote(0, 0, "E5", "sine", 1.0, 5.0, None, None)


    track1.addNote(1, 0, "F5", "sine", 1.0, 3.0, None, None)
    track1.addNote(1, 1, "E5", "sine", 1.0, 1.0, None, None)
    track1.addNote(1, 2, "A5", "sine", 1.0, 1.0, None, None)
    track1.addNote(1, 3, "C5", "sine", 1.0, 1.0, None, None)

    track2.addNote(1, 0, "C5", "sine", 1.0, 5.0, None, None)


    track1.addNote(2, 0, "D5", "sine", 1.0, 3.0, None, None)
    track1.addNote(2, 1, "C5", "sine", 1.0, 1.0, None, None)
    track1.addNote(2, 2, "F5", "sine", 1.0, 1.0, None, None)
    track1.addNote(2, 3, "A4", "sine", 1.0, 1.0, None, None)

    track2.addNote(2, 0, "A4", "sine", 1.0, 5.0, None, None)


    track1.addNote(3, 0, "C5", "sine", 1.0, 3.0, None, None)
    track1.addNote(3, 1, "B4", "sine", 1.0, 3.0, None, None)

    track2.addNote(3, 0, "E4", "sine", 1.0, 3.0, None, None)
    track2.addNote(3, 0, "G4", "sine", 1.0, 3.0, None, None)

    # line 3
    track1.addNote(4, 0, "A5", "sine", 1.0, 3.0, None, None)
    track1.addNote(4, 1, "G5", "sine", 1.0, 1.0, None, None)
    track1.addNote(4, 2, "C6", "sine", 1.0, 1.0, None, None)
    track1.addNote(4, 3, "E5", "sine", 1.0, 1.0, None, None)

    track2.addNote(4, 0, "E5", "sine", 1.0, 5.0, None, None)


    track1.addNote(5, 0, "F5", "sine", 1.0, 3.0, None, None)
    track1.addNote(5, 1, "E5", "sine", 1.0, 1.0, None, None)
    track1.addNote(5, 2, "A5", "sine", 1.0, 1.0, None, None)
    track1.addNote(5, 3, "C5", "sine", 1.0, 1.0, None, None)

    track2.addNote(5, 0, "C5", "sine", 1.0, 5.0, None, None)


    track1.addNote(6, 0, "D5", "sine", 1.0, 3.0, None, None)
    track1.addNote(6, 1, "A5", "sine", 1.0, 1.0, None, None)
    track1.addNote(6, 2, "B5", "sine", 1.0, 1.0, None, None)
    track1.addNote(6, 3, "C6", "sine", 1.0, 1.0, None, None)

    track2.addNote(6, 0, "F4", "sine", 1.0, 4.0, None, None)


    track1.addNote(7, 0, "C6", "sine", 1.0, 3.0, None, None)
    track1.addNote(7, 1, "B5", "sine", 1.0, 3.0, None, None)

    track2.addNote(7, 0, "G5", "sine", 1.0, 6.0, None, None)

elif METROID == 2:

    # format is
    # ...  addNote(measure, startingBeat, instrument, volume, length, filter, cutoff)
    track1.addNote(3, 0, "F4", "sawtooth", 1.0, 1.0, None, None)
    track1.addNote(3, 1, "E4", "trumpet", 0.5, 1.0, None, None)
    track1.addNote(3, 2, "D4", "sawtooth", 1.0, 1.0, None, None)
    track1.addNote(3, 3, "C4", "sawtooth", 1.0, 1.0, None, None)
    track1.addNote(3, 4, "C4", "sawtooth", 1.0, 1.0, None, None)

    #track1.addNote(3, 1, "C4", "sine", 0.5, 1.0, None, None)

    track1.addNote(0, 0, "F3", "sawtooth", 1.0, 1.0, None, None)
    track1.addNote(0, 1, "E3", "sine", 0.5, 1.0, None, None)
    track1.addNote(0, 2, "D3", "sawtooth", 1.0, 1.0, None, None)
    track1.addNote(0, 3, "C3", "sine", 0.5, 1.0, None, None)

    track1.addNote(5, 0, "C4", "sine", 1, 3.0, None, None)

    #print(track1.noteList)
    #print(track1.noteNameList)


    track2.addNote(3, 0, "F5", "sawtooth", 1.0, 1.0, None, None)
    track2.addNote(3, 1, "E5", "sine", 0.5, 1.0, None, None)
    track2.addNote(3, 2, "D5", "sawtooth", 1.0, 1.0, None, None)
    track2.addNote(3, 3, "C5", "sine", 0.5, 1.0, None, None)

    track2.addNote(7, 0, 'D4', 'sawtooth', 0.5, 4.0, None, None)

    track3.addNote(3, 0, "A5", "sawtooth", 1.0, 1.0, None, None)
    track3.addNote(3, 1, "B5", "sine", 0.5, 1.0, None, None)
    track3.addNote(3, 2, "G5", "sawtooth", 1.0, 1.0, None, None)
    track3.addNote(3, 3, "A5", "sine", 0.5, 1.0, None, None)

    #track1.clearMeasure(0)
    #track1.clearMeasure(3)


trackList.append(track1)
trackList.append(track2)
trackList.append(track3)
trackList.append(track4)
trackList.append(track5)

if PLAYBACK:
    for track in trackList:
        track.playBack()

# determine where all tracks are blank (to prevent excessive silence at the end)
lastMeasureIndex = 0
for track in trackList:
    flag = 0
    for i in range(len(track.noteNameList) - 1, lastMeasureIndex - 1, -1):
        for j in range(len(track.noteNameList[i]) - 1, -1, -1):
            #print(i, j)
            #print(track.noteNameList[i], flag)
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
    sound1 = track.noteList[0][0]
    for measureNum in range(len(track.noteList)):
        if len(track.noteList[measureNum]) == 1 and measureNum == 0:  # if the first measure contains one note
            sound2 = 0  # 0 so that the only sound in measure 1 isn't doubled in amplitude
            newSound = sound1 + sound2
            sound1 = newSound
        elif len(track.noteList[measureNum]) == 1:  # if non-first measure is only one note long
            sound2 = track.noteList[measureNum][0]
            newSound = sound1 + sound2
            sound1 = newSound
        elif measureNum == 0:  # cover for rest of 1st measure cases
            for note in range(1, len(track.noteList[measureNum])):
                sound2 = track.noteList[measureNum][note]
                newSound = sound1 + sound2
                sound1 = newSound
        else:
            for note in range(0, len(track.noteList[measureNum])):
                sound2 = track.noteList[measureNum][note]
                newSound = sound1 + sound2
                sound1 = newSound
    s = 'TrackTestNum' + str(trackList.index(track)) + '.wav'
    newSound.export(s, format='wav')
    trackWavs.append(newSound)


# print(trackWavs)
track1 = trackWavs[0]
for i in range(1, len(trackWavs)):
    track2 = trackWavs[i]
    combinedTrack = track1.overlay(track2, position = 0)
    track1 = combinedTrack
combinedTrack.export('CombinedTest.wav', format='wav')

