import matplotlib.pyplot as plt 
import numpy as np

# %% time
# t parameters
t_blue = 20
t_cap= 23
t_ramp = 73
t_bb1 = t_cap + t_ramp
t_bb2 = 20
t_sf1 = 73
t_sf2 = 30

# derived parameters
t_bb = t_bb1 + t_bb2
t_sf = t_sf1 + t_sf2
time = np.linspace(-t_blue, t_bb + t_sf, 1000)

# %% intialize plot

fig1, (ax1, ax2, ax3, ax4) = plt.subplots(nrows = 4, ncols = 1,
                                          figsize = (5, 7), sharex = True)
ax4.set_xlabel('time [ms]')

# %% blue MOT beams

blue_beams = np.piecewise(time, [time < 0, time >= 0], [1, 0])

ax1.plot(time, blue_beams)
ax1.grid()
ax1.sharex(ax2)
y_ticks = [0, 1]
y_tick_labels = ['off', 'on']
ax1.set_yticks(y_ticks)
ax1.set_yticklabels(y_tick_labels)

# %% quadropole field gradient

# B parameters
b_blue = 55
b_bb1 = 1.48
b_bb2 = 4.24
b_ramp = (b_bb2 - b_bb1)/t_ramp*(time - t_cap) + b_bb1


def grad_field(t):
    if t < 0:
        return b_blue
    elif (t>=0) & (t<t_cap):
        return b_bb1
    elif (t>=t_cap) & (t<t_bb1):
        return (b_bb2 - b_bb1)/t_ramp*(t - t_cap) + b_bb1
    else:
        return b_bb2


grad_field = [grad_field(t) for t in time]

ax2.grid()
ax2.plot(time, grad_field, color = 'black', label = 'magnetic field gradient')
ax2.set_ylabel('Gradient [G/cm]')

# %% red MOT beams intensity

# red intensity parameters
i_bb1 = 2
i_bb2 = 2
i_dec_start = 0.0259
i_dec_end = 0.0033
i_dec_tau = 16.8
i_dec_time = 73


def red_intensity(t):
    if t < t_bb1:
        return i_bb1
    elif (t >= t_bb1) & (t < t_bb1+t_bb2):
        return i_bb2
    elif (t >= t_bb1+t_bb2) & (t < t_bb1+t_bb2+i_dec_time):
        pre_factor = (i_dec_end - i_dec_start)/(np.exp(-t_sf1/i_dec_tau) - 1)
        value = pre_factor*(np.exp(-(t - t_bb1 - t_bb2)/i_dec_tau) - np.exp(-t_sf1/i_dec_tau)) + i_dec_end
        return value
    else:
        return i_dec_end
    

red_intensity = [red_intensity(t) for t in time]

ax3.grid()
ax3.plot(time, red_intensity, color = 'red', label = '689 intensity')
ax3.set_yscale('log')
ax3.set_ylabel('Intensity [mW]')

# %% red MOT beams frequency

# bb stages
detuning_bb1 = -110*1e3
moddepth_bb1 = 1.72*1e6
moddepth_bb2 = 500e3

# sf stages
freq_dec_start = -780*1e3
freq_dec_tau = 16.0
freq_dec_end = -50e3


def red_frequency(t):
    if t < t_bb1:
        return -moddepth_bb1
    elif (t >= t_bb1) & (t < t_bb1+t_bb2):
        return -moddepth_bb2
    elif (t >= t_bb1+t_bb2) & (t < t_bb1+t_bb2+i_dec_time):
        pre_factor = (freq_dec_end - freq_dec_start)/(np.exp(-t_sf1/freq_dec_tau) - 1)
        value = pre_factor*(np.exp(-(t - t_bb1 - t_bb2)/freq_dec_tau) - np.exp(-t_sf1/freq_dec_tau)) + freq_dec_end
        return value
    else:
        return freq_dec_end
    

red_freqencies = np.array([red_frequency(t) for t in time])

ax4.grid()
ax4.plot(time, red_freqencies/1e6, color = 'red', label = '689 detuning')
ax4.hlines(y = detuning_bb1/1e6, xmin = -t_blue, xmax = t_bb1 + t_bb2, color = 'red')
ax4.vlines(x = t_bb1 + t_bb2, ymin = -moddepth_bb2/1e6, ymax = detuning_bb1/1e6, color = 'red')
ax4.set_ylabel('Detuning [MHz]')

# %% plotting

plt.show()