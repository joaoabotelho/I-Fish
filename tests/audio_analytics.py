import wave
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import normalize

FILE_NAME = "audio-siri/Siri_test1.wav"

class AudioInformation:
    def __init__(self, file_name):
        self.file = wave.open(file_name, "rb")
        self.data = self.setData()
        self.framerate = self.setFramerate()
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

        plt.figure(1)
        plt.title('Signal Wave...')
        plt.plot(Time, self.normalized)
        plt.show()

    def setData(self):
        return self.file.readframes(-1)

    def setAmpl(self):
        return np.fromstring(self.data, 'Int16').astype(float)

    def setFramerate(self):
        return self.file.getframerate()

    def setNormalized(self):
        return 2*((self.ampl - min(self.ampl))/(max(self.ampl)-min(self.ampl)))-1

if __name__ == "__main__":
    test = AudioInformation(FILE_NAME)
    print test
    test.plot_audio()
