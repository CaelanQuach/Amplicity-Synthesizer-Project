import random #Used for random number generation
import thinkdsp #Used for generating sine waves
from pydub import AudioSegment #Used to convert sine waves into sound
from pydub.playback import play #Used to play sound in python
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
                 "Ab5": 830.61,"A5": 880.00,"Bb5": 932.33,"B5": 987.77,}
#Generates a random set of coefficients to be used for Fourier Sound Synthesis
randomCoefficients = []
for i in range(0,8):
    randomCoefficients.append(random.uniform(-1,1))

#The coefficients represent the amplitude of the corresponding harmonic
fourierCoefficients = {
    "sine": [0,1,0,0,0,0,0,0],"sawtooth":[0,0.6366,0,-0.2122,0,0.1273,0,-0.0909],
    "trumpet":[0.1155,0.3417,0.1789,0.1232,0.0678,0.0473,0.0260,0.0045,0.0020], "random": randomCoefficients,
    "test":[0,-0.25,0.25,0.866,0,0,0,0]
}
#Actual sound synthesis part:
#Function that creates an AudioSegment of a certain note
#Amp is relative amplitude
#Beats is length of note relative to a quarter note at 120 BPM
#Filter can be low-pass or high-pass depending on the cutoff frequency given
#Filename doesn't really matter in this composition because I will be reading in the sound signal back into...
def createNote(noteName="A4", type = "sine", amp = 0.5, beats = 0.5, filter = None, cutoff = None, filename="defaultFilename"):
    #Initializing values, let signal be empty first
    frequency = noteFrequency[noteName]
    duration = beats /2
    signal = thinkdsp.SinSignal(freq=0)

    #Add harmonics to the signal according to their Fourier Synthesis Coefficients
    for i in range(0,8):
        signal += thinkdsp.SinSignal(freq=frequency*i,amp=amp*fourierCoefficients[type][i], offset=0)
    #Convert signal into wave to .wav file to AudioSegment to be mixed and played by the program
    wave = signal.make_wave(duration=duration, start=0, framerate=44100)
    wave.write(filename=filename)
    audio = AudioSegment.from_wav(filename)
    print("Creating note {} at {} for {} beats ###THERE WAS MORE TO THIS PRINT STATEMENT I JUST CANNOT SEE IT".format(noteName,str(frequency),str(beats)))
    #Adding filters
    if filter == "lowPass":
        audio = audio.low_pass_filter(cutoff)
        print("Applying Low-Pass Filter")
    if filter == "highPass":
        audio = audio.high_pass_filter(cutoff)
    return audio



#Example Notes
A4 = createNote(noteName="A4", type = "test", amp = 1, beats = 1, filter = None, cutoff = None)# This line of code wasn't here, but I had it for bugtesting purposes, filename="defaultFilename")
B4 = createNote(noteName="B4", type = "test", amp = 1, beats = 1, filter = None, cutoff = None)# This line of code wasn't here, but I had it for bugtesting purposes, filename="defaultFilename")
C5 = createNote(noteName="C5", type = "test", amp = 1, beats = 1, filter = None, cutoff = None)# This line of code wasn't here, but I had it for bugtesting purposes, filename="defaultFilename")
D5 = createNote(noteName="D5", type = "test", amp = 1, beats = 1, filter = None, cutoff = None)# This line of code wasn't here, but I had it for bugtesting purposes, filename="defaultFilename")
E5 = createNote(noteName="E5", type = "test", amp = 1, beats = 1, filter = None, cutoff = None)# This line of code wasn't here, but I had it for bugtesting purposes, filename="defaultFilename")
F5 = createNote(noteName="F5", type = "test", amp = 1, beats = 1, filter = None, cutoff = None)# This line of code wasn't here, but I had it for bugtesting purposes, filename="defaultFilename")
G5 = createNote(noteName="G5", type = "test", amp = 1, beats = 1, filter = None, cutoff = None)# This line of code wasn't here, but I had it for bugtesting purposes, filename="defaultFilename")
A5 = createNote(noteName="A5", type = "test", amp = 1, beats = 1, filter = None, cutoff = None)# This line of code wasn't here, but I had it for bugtesting purposes, filename="defaultFilename")

track1 = [A4, B4, C5, D5, E5, F5, G5, A5]




for note in track1:
    play(note)