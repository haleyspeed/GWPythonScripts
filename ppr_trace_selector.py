# Author: Haley Speed
# Description: Caluclates the order of traces to be
#    analyzed in Clampfit


# To run script without user input
end = 193
   	# Last Sweep #
intervals = 6	# Number of different interstimulus intervals
repetitions = 5 # Number of sweeps to average per interstimulus interval

for j in range (1, intervals + 1):
    last = end
    traces = ''
    
    for i in range(1, repetitions + 1):
        traces = 't' + str(last) + ',' + traces
        last = last - 6
    
    print(traces) 
    end = end - 1

    j = j + 1
    

