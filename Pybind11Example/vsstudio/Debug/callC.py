
import numpy as np
import matplotlib.pyplot as plt
import time
from numpy import random
import timeit
n_bins=40
sampelsN = []
dataNo=[]
Error=[]
duration_fft = []
duration_dft = []
DFT_list=[]
FFT_list=[]
for i in range(3):
    sampelsN.append([random.randint(1,10000) for _ in range(2**(4+i*3))])

for i in range(3):
    start = timeit.default_timer()
    DFT_list.append(sampelsN[i])
    end = timeit.default_timer()
    duration_dft.append(end-start)
    time.sleep(1)
    start = timeit.default_timer()
    FFT_list.append(sampelsN[i])
    end = timeit.default_timer()
    duration_fft.append(end-start)

    Error.append([np.square(np.subtract(DFT_list[i],FFT_list[i])).mean()])

print(f'Time Difference in FFT:\n{duration_fft}')
print(f'Time Difference in DFT:\n{duration_dft}')

'''
fig, (ax1, ax2) = plt.subplots(2)
ax1.set_ylabel("Time(s)")
ax1.set_xlabel("DATA SIZE")
for i in range(3):
    ax1.plot(sampelsN[i],duration_fft[i])
    ax1.plot(sampelsN[i],duration_dft[i])
ax1.legend(["FFT(N*log(N))", "DFT(N^2)"])
ax2.set_ylim(0,2)
ax2.set_ylabel("ERROR")
ax2.set_xlabel("DATA SIZE")
for i in range(3):

    ax2.plot(sampelsN[i],Error[i])
plt.show()


'''
