 # @file digital_oscilloscope.py
 # @author Gregório da Luz
 # @date January 2021
 # @brief digital_oscilloscope plotting ADC values from .txt file

ADC_file = open("ADC_data.txt","r")
freq_s = 900
delta_t = 1/freq_s
ADC_data_ar = []
time_ar = []
time = 0
not_end_file = 1

while not_end_file:
    time_ar.append(time)
    time += delta_t
    temp = ADC_file.readline()
    if temp == "" or temp =="\n":
        not_end_file = 0
    else:
        ADC_data_ar.append(temp)

for x in ADC_data_ar:
    print(x)
