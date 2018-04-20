import wave
import matplotlib.pyplot as plt
import numpy as np
import peakutils
from sklearn.preprocessing import normalize

FILE_NAME = "audio-siri/kanye_test.wav"

class AudioInformation:
    def __init__(self, file_name):
        self.file = wave.open(file_name, "r")
        self.data = self.setData()
        self.framerate = self.setFramerate()
        self.baseG = self.setBaseGraph()
        self.ampl = self.setAmpl()
        self.normalized = self.setNormalized()

    def __str__(self):
        f_str = ""
        if self.file.getnchannels() == 1:
            f_str = "mono,"
        else:
            f_str = "stereo,"

        f_str += str(self.file.getsampwidth()*8) + "bits,"
        f_str += str(self.framerate) + "Hz sampling rate"
        f_str += "\n" + str(len(self.data)) + "bytes"

        return f_str

    def plot_audio(self):
        Time=np.linspace(0, len(self.ampl)/self.framerate, num=len(self.ampl))

        print "Max value -> ", max(self.ampl)
        print "Min value -> ", min(self.ampl)
        print "norm Len -> ", len(self.normalized)

        plt.figure(1)
        plt.title('Signal Wave...')
        plt.subplot(2,1,1)
        plt.plot(self.normalized)
        plt.subplot(2,1,2)
        plt.plot(self.baseG)
        plt.show()

    def setData(self):
        return self.file.readframes(-1)

    def setAmpl(self):
        print "Len -> ", len(self.baseG)
        indexes = peakutils.indexes(self.baseG, thres=0.02/max(self.baseG), min_dist=1200)
        final = np.take(self.baseG, indexes)
        return final

    def setBaseGraph(self):
        return np.fromstring(self.data, 'Int16').astype(float)

    def setFramerate(self):
        return self.file.getframerate()

    def setNormalized(self):
        return (self.ampl - min(self.ampl))/(max(self.ampl)-min(self.ampl))

if __name__ == "__main__":
    test = AudioInformation(FILE_NAME)
    print test
    test.plot_audio()
