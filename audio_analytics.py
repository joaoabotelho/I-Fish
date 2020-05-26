import wave
import sys
#import matplotlib.pyplot as plt
import numpy as np
#import peakutils
import time
#from detect_peaks import detect_peaks

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

        print ("BASEG Len -> ", self.baseG.size)
        print (self.__str__())
        # gets indexes of all peaks in sound wave
        begin = time.time()
        indexes = np.array(self.indexes(self.baseG, thres=0, min_dist=2000))
        print("END INDEXES -> ", time.time()-begin)
        print("INDEXES LEN -> ", indexes.size)
        self.array_of_time = np.diff(indexes) * self.time_per_value
        self.array_of_time = np.insert(self.array_of_time, 0,
                self.time_per_value*indexes[0] + 0.06)
        print(self.array_of_time)
        #print sum(self.array_of_time)
        final = np.take(self.baseG, indexes)
        return final

    def setBaseGraph(self):
        base = np.array(np.fromstring(self.data, 'Int16').astype(float))

        #base = base[base >= 0]

        return base

    def setFramerate(self):
        return self.file.getframerate()

    def setNormalized(self):
        norm = np.array((self.ampl -
            min(self.ampl))/(max(self.ampl)-min(self.ampl)))
        return np.array([round(i, 1) for i in norm])

    def indexes(self, y, thres=0.0, min_dist=1):
        if isinstance(y, np.ndarray) and np.issubdtype(y.dtype, np.unsignedinteger):
            raise ValueError("y must be signed")

        thres = thres * (np.max(y) - np.min(y)) + np.min(y)
        min_dist = int(min_dist)

        # compute first order difference
        dy = np.diff(y)

        # propagate left and right values successively to fill all plateau pixels (0-value)
        zeros,=np.where(dy == 0)

        # check if the singal is totally flat
        if len(zeros) == len(y) - 1:
            return np.array([])

        while len(zeros):
            # add pixels 2 by 2 to propagate left and right value onto the zero-value pixel
            zerosr = np.hstack([dy[1:], 0.])
            zerosl = np.hstack([0., dy[:-1]])

            # replace 0 with right value if non zero
            dy[zeros]=zerosr[zeros]
            zeros,=np.where(dy == 0)

            # replace 0 with left value if non zero
            dy[zeros]=zerosl[zeros]
            zeros,=np.where(dy == 0)

        # find the peaks by using the first order difference
        peaks = np.where((np.hstack([dy, 0.]) < 0.)
                         & (np.hstack([0., dy]) > 0.)
                         & (y > thres))[0]

        # handle multiple peaks, respecting the minimum distance
        if peaks.size > 1 and min_dist > 1:
            highest = peaks[np.argsort(y[peaks])][::-1]
            rem = np.ones(y.size, dtype=bool)
            rem[peaks] = False

            for peak in highest:
                if not rem[peak]:
                    sl = slice(max(0, peak - min_dist), peak + min_dist + 1)
                    rem[sl] = True
                    rem[peak] = False

            peaks = np.arange(y.size)[~rem]

        return peaks

if __name__ == "__main__":
    test = AudioInformation(sys.argv[1])
    print (test)
    test.plot_audio()
