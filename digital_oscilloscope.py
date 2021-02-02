 # @file digital_oscilloscope.py
 # @author Gregório da Luz
 # @author Maksymilian Mruszczak
 # @date January 2021
 # @brief digital_oscilloscope plotting ADC values from .txt file

from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np
from scipy.fftpack import fft

class Oscilloscope:
    LABEL_STYLE = dict(
            boxstyle = "round",
            ec = (.5, .7, 1.),
            fc = (.7, .9, 1.),
            )

    def __init__(self):
        self.coord = []
        #variable to clean coord after two points FOR PLOT 1
        self.control = 0
        self.fig = plt.figure(1)
        self.ax, self.axfft = self.fig.subplots(1, 2, sharey=True)
        self.ax.set_xlabel("time [s]")
        self.ax.set_ylabel("Voltage [V]")
        self.ax.set_title('digital_oscilloscope')
        self.axfft.set_xlabel("frequency [Hz]")
        self.axfft.set_ylabel("Voltage [V]")
        self.axfft.set_title('digital_oscilloscope fft')
        #defining the cursor for plot 1
        self.cursor = Cursor(self.ax, horizOn = True, vertOn=True, color='red', linewidth=1, useblit=True)
        self.ax.grid()
        self.axfft.grid()
        #Creating the annotation framework for plot 1
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(-40,40),textcoords="offset points", bbox=dict(boxstyle="round4", fc="grey", ec="k", lw=2), arrowprops=dict(arrowstyle="-|>"))
        self.annot.set_visible(False)
        # create labels
        self.file_label = self.fig.text(.05, .95, 'data file path: -', bbox=self.LABEL_STYLE, alpha=.5)
        self.cursor_label = self.fig.text(.5, .95, 'distance: -', bbox=self.LABEL_STYLE, alpha=.5)
        # bind event
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

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
        ADC_fft_data_ar = np.abs(fft(ADC_data_ar))/num_samples
        self.ax.plot(time_ar, ADC_data_ar, color='blue')
        self.axfft.plot(freq_ar, ADC_fft_data_ar, color='red')
        self.file_label.set_text('data file path: %s' % filename)
        plt.draw()

    #Function for storing and showing the clicked values FOR PLOT 1
    def onclick(self, event):
        if self.control == 2:
            self.coord = []
            self.control = 0
        self.coord.append((event.xdata, event.ydata))
        x = event.xdata
        y = event.ydata
        self.annot.xy = (x,y)
        text = "({:.2g},{:.2g})".format( x,y )
        self.annot.set_text(text)
        self.annot.set_visible(True)
        self.fig.canvas.draw() #redraw the figure
        if self.control == 1:
            # Unzipping the coord list in two different arrays
            x1, y1 = zip(*self.coord)
            diff_x = format(abs(x1[0]-x1[1]),'.4f')
            diff_y = format(abs(y1[0]-y1[1]),'.4f')
            print("distance x = "+str(diff_x))
            print("distance y = "+str(diff_y))
            self.cursor_label.set_text('distance: x = %s y = %s' % (diff_x, diff_y))
            plt.draw()
        self.control +=1


if __name__ == '__main__':
    oscope = Oscilloscope()
    oscope.draw('ADC_data.txt')
    plt.show()
