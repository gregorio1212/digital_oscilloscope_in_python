 # @file digital_oscilloscope.py
 # @author Gregório da Luz
 # @date January 2021
 # @brief digital_oscilloscope plotting ADC values from .txt file
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np
import scipy.fftpack

ADC_file = open("ADC_data.txt","r")
freq_s = 900.0
delta_t = 1.0/freq_s
ADC_data_ar = []
num_samples = 500
time_ar = np.linspace(0.0, num_samples*delta_t, num_samples)
#5 V - 10 bits ADC 5/1023=0.0048
bit_multiplier = 0.0048

#filling the ADC array
for i in time_ar:
    temp = int(ADC_file.readline(),16)*bit_multiplier
    ADC_data_ar.append(temp)
#plot 1
fig = plt.figure(1)
ax = fig.subplots()
ax.plot(time_ar,ADC_data_ar,color='blue')
plt.xlabel("time [s]")
plt.ylabel("Voltage [V]")
plt.title('digital_oscilloscope')
ax.grid()

#defining the cursor for plot 1
cursor = Cursor(ax, horizOn = True, vertOn=True, color='red', linewidth=1, useblit=True)

#Creating the annotation framework for plot 1
annot = ax.annotate("", xy=(0,0), xytext=(-40,40),textcoords="offset points", bbox=dict(boxstyle="round4", fc="grey", ec="k", lw=2), arrowprops=dict(arrowstyle="-|>"))
annot.set_visible(False)

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
    annot.xy = (x,y)
    text = "({:.2g},{:.2g})".format( x,y )
    annot.set_text(text)
    annot.set_visible(True)
    fig.canvas.draw() #redraw the figure
    if control == 1:
        # Unzipping the coord list in two different arrays
        x1, y1 = zip(*coord)
        diff_x = format(abs(x1[0]-x1[1]),'.4f')
        diff_y = format(abs(y1[0]-y1[1]),'.4f')
        print("distance x = "+str(diff_x))
        print("distance y = "+str(diff_y))
    control +=1

fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
