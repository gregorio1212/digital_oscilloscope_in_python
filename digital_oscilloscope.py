 # @file digital_oscilloscope.py
 # @author Gregório da Luz
 # @date January 2021
 # @brief digital_oscilloscope plotting ADC values from .txt file
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np
import scipy.fftpack

class Oscilloscope:
    def __init__(self):
        self.fig = plt.figure(1)
        self.ax, self.axfft = self.fig.subplots(1, 2, sharey=True)
        plt.xlabel("time [s]")
        plt.ylabel("Voltage [V]")
        plt.title('digital_oscilloscope')
        self.ax.set_xlabel("time [s]")
        self.ax.set_ylabel("Voltage [V]")
        self.ax.set_title('digital_oscilloscope')
        self.axfft.set_xlabel("frequency [Hz]")
        self.axfft.set_ylabel("Voltage [V]")
        self.axfft.set_title('digital_oscilloscope fft')
        #defining the cursor for plot 1
        self.cursor1 = Cursor(self.ax, horizOn = True, vertOn=True, color='red', linewidth=1, useblit=True)
        self.cursor2 = Cursor(self.axfft, horizOn = True, vertOn=True, color='green', linewidth=1, useblit=True)
        self.ax.grid()
        self.axfft.grid()
        #Creating the annotation framework for plot 1
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(-40,40),textcoords="offset points", bbox=dict(boxstyle="round4", fc="grey", ec="k", lw=2), arrowprops=dict(arrowstyle="-|>"))
        self.annot.set_visible(False)

    def draw(self, filename):
        freq_s = 900.0
        delta_t = 1.0/freq_s
        ADC_data_ar = []
        num_samples = 500
        time_ar = np.linspace(0.0, num_samples*delta_t, num_samples)
        freq_ar = np.linspace(0.0, freq_s, num_samples)
        #5 V - 10 bits ADC 5/1023=0.0048
        bit_multiplier = 0.0048
        #filling the ADC array
        with open(filename, 'r') as ADC_file:
            for i in time_ar:
                temp = int(ADC_file.readline(),16)*bit_multiplier
                ADC_data_ar.append(temp)
        ADC_fft_data_ar = np.abs(scipy.fftpack.fft(ADC_data_ar))/num_samples
        self.ax.plot(time_ar, ADC_data_ar, color='blue')
        self.axfft.plot(freq_ar, ADC_fft_data_ar, color='blue')


oscope = Oscilloscope()

#Function for storing and showing the clicked values FOR PLOT 1
coord = []
#variable to clean coord after two points FOR PLOT 1
control = 0
def onclick(event):
    global coord
    global control
    if control == 2:
        coord = []
        control = 0
    coord.append((event.xdata, event.ydata))
    x = event.xdata
    y = event.ydata
    oscope.annot.xy = (x,y)
    text = "({:.2g},{:.2g})".format( x,y )
    oscope.annot.set_text(text)
    oscope.annot.set_visible(True)
    oscope.fig.canvas.draw() #redraw the figure
    if control == 1:
        # Unzipping the coord list in two different arrays
        x1, y1 = zip(*coord)
        diff_x = format(abs(x1[0]-x1[1]),'.4f')
        diff_y = format(abs(y1[0]-y1[1]),'.4f')
        print("distance x = "+str(diff_x))
        print("distance y = "+str(diff_y))
    control +=1

oscope.fig.canvas.mpl_connect('button_press_event', onclick)

oscope.draw('ADC_data.txt')
plt.show()
