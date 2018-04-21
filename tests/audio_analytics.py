import wave
import sys
import matplotlib.pyplot as plt
import numpy as np
import peakutils
from sklearn.preprocessing import normalize

#FILE_NAME = "audio-siri/kanye_test.wav"
#FILE_NAME = "audio-siri/Choppa_test.wav"
FILE_NAME = "audio-siri/hackthon_test.wav"
#FILE_NAME = "audio-siri/Siri_test1.wav"

class AudioInformation:
    def __init__(self, file_name):
        self.file = wave.open(file_name, "rb")
        self.array_of_time = np.array([])
        self.data = self.setData()
        self.framerate = self.setFramerate()
        self.baseG = self.setBaseGraph()
        self.total_time = (self.baseG.size/float(self.framerate))*0.5
        self.time_per_value = self.total_time / self.baseG.size
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
        f_str += "\n" + str(self.data.size) + "bytes"
        f_str += "\n" + str(self.total_time) + " total time"
        f_str += "\n" + str(self.time_per_value) + " time per value"

        return f_str

    def plot_audio(self):
        Time=np.linspace(0, self.ampl.size/self.framerate, num=self.ampl.size)
        print ("Max value -> ", max(self.ampl))
        print ("Min value -> ", min(self.ampl))
        print ("norm Len -> ", self.normalized.size)

        plt.figure(1)
        plt.title('Signal Wave...')
        plt.subplot(2,1,1)
        plt.plot(self.normalized)
        plt.subplot(2,1,2)
        plt.plot(self.baseG)
        plt.show()

    def setData(self):
        return np.array(self.file.readframes(-1))

    def setAmpl(self):
        array = np.array([])

        print ("Len -> ", self.baseG.size)

        # gets indexes of all peaks in sound wave
        indexes = np.array(peakutils.indexes(self.baseG, thres=0.02/max(self.baseG),
                min_dist=1400))
        print indexes[0]
        self.array_of_time = np.append(self.array_of_time, indexes[0])
        #self.array_of_time = [(y - x) for (x, y) in zip(indexes[:-1], indexes[1:])]

        # gets time between values
        for i in range(1, indexes.size):
            value = indexes[i] - indexes[i-1]
            self.array_of_time = np.append(self.array_of_time, value)

        print self.array_of_time
        self.array_of_time = [x * self.time_per_value for x in
            self.array_of_time]
        print self.array_of_time
        #print self.array_of_time
        #print sum(self.array_of_time)
        final = np.take(self.baseG, indexes)
        return final

    def setBaseGraph(self):
        return np.array(np.fromstring(self.data, 'Int16').astype(float))

    def setFramerate(self):
        return self.file.getframerate()

    def setNormalized(self):
        return np.array((self.ampl -
            min(self.ampl))/(max(self.ampl)-min(self.ampl)))

if __name__ == "__main__":
    test = AudioInformation(sys.argv[1])
    print (test)
    test.plot_audio()
