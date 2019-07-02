"""
Pible Simulator
"""

import numpy as np
import datetime
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys

# Parameter to change
sens_time_orig = 900 # Sensing data every "sens_time_orig" seconds.
SC_perc_init = 100 # Super Capacitor initial voltage. Put "100" for maximum capacity at the beginning of the experiment
light_lux = 250 # Average of light the solar panel receive during the "light_hours_per day"
light_hours_per_day = 8 #starting from 8AM the system receive "light_lux" light for "light_hours_per_day" time
days_simulators = 4 # Leave the simulaor running for this amount of time unless the node dies before such time
PIR = False # PIR active and used to detect people
PIR_events = 200 # Number of PIR events detected during a day. This could happen also when light is not on

# DO NOT MODIFY!  POWER CONSUMPTION PARAMETERS! Change them only if you change components.
SC_perc_min = 0; SC_perc_max = 100.0; SC_norm_max = 10; SC_norm_min = 0; SC_norm_min_die = 4; SC_volt_min = 2.3; SC_volt_max = 5.5; SC_size = 1.5
light_real_min = 0; light_real_max= 2000; light_max = 10; light_min = 0

i_wake_up_advertise = 0.00006; time_wake_up_advertise = 11
i_BLE_comm = 0.00025; time_BLE_comm = 4
i_BLE_sens = ((i_wake_up_advertise * time_wake_up_advertise) + (i_BLE_comm * time_BLE_comm))/(time_wake_up_advertise + time_BLE_comm)
time_BLE_sens = time_wake_up_advertise + time_BLE_comm

i_sleep = 0.0000032; i_BLE_sens = 0.000210; time_BLE_sens = 6.5
i_PIR_detect = 0.000102; PIR_detect_time = 2.5

if PIR == True:
    i_sleep = 0.0000042

v_solar_200_lux = 1.5; i_solar_200_lux = 0.000031; # It was 1.5
p_solar_1_lux = (v_solar_200_lux * i_solar_200_lux) / 200.0


# Starting Simulator
SC_volt = (SC_perc_init/SC_perc_max) * SC_volt_max
SC_perc = SC_perc_init
energy_rem = SC_volt * SC_volt * 0.5 * SC_size
curr_time = datetime.datetime.now()
curr_time = curr_time.replace(month=1, day=1, hour=0, minute=0, second=0)
light = light_lux

if PIR == True and PIR_events == 0:
    PIR_time_orig = sys.maxsize
elif PIR == True:
    PIR_time_orig = (24*60*60)/PIR_events # events happenig every "PIR_time" seconds
else:
    PIR_time_orig = sys.maxsize
    PIR_events = 0

sens_time = sens_time_orig
PIR_time = PIR_time_orig

light_hist = []; time_hist = []; SC_norm_hist = []; SC_perc_hist = []; SC_volt_hist = []; PIR_hist = []
while True:

    #light_norm = (((light - light_real_min) * (light_max - light_min)) / (light_real_max - light_real_min)) + light_min
    #SC_norm = (((SC_volt - SC_perc_min) * (SC_norm_max - SC_norm_min)) / (SC_perc_max - SC_perc_min)) + SC_norm_min

    if int(curr_time.hour) >= 8 and int(curr_time.hour) <= 8 + light_hours_per_day:
        light = light_lux
    else:
        light = 0

    if PIR == True and PIR_time <= sens_time: # PIR detected ans sensing
        energy_used = ((PIR_time - time_BLE_sens) * SC_volt * i_sleep) + (time_BLE_sens * SC_volt * i_BLE_sens) + (i_PIR_detect * SC_volt * PIR_detect_time)
        #print("PIR", PIR_time)
        energy_prod = PIR_time * p_solar_1_lux * light
        detect = 1
    else:
        energy_used = ((sens_time - time_BLE_sens) * SC_volt * i_sleep) + (time_BLE_sens * SC_volt * i_BLE_sens)
        energy_prod = sens_time * p_solar_1_lux * light
        detect = 0
        #print("sens", sens_time)

    # Update energy value for next iteration
    energy_rem = energy_rem - energy_used + energy_prod
    SC_volt = np.sqrt((2*energy_rem)/SC_size)

    # Set the energy upperbound
    if SC_volt > SC_volt_max:
        SC_volt = SC_volt_max

    energy_rem = SC_volt * SC_volt * 0.5 * SC_size
    SC_perc = (SC_volt/SC_volt_max) * 100

    # Save values in a list
    light_hist.append(light); SC_perc_hist.append(SC_perc); time_hist.append(curr_time); SC_volt_hist.append(SC_volt); PIR_hist.append(detect)
    # SC_norm_hist.append(SC_norm)

    if PIR == True and sens_time < PIR_time: # serving Sensing
        delta = sens_time
        PIR_time -= delta
        sens_time = sens_time_orig
    elif PIR == True and PIR_time <= sens_time: # serving PIR
        delta = PIR_time
        sens_time -= delta
        PIR_time = PIR_time_orig
    else:
        delta = sens_time_orig

    curr_time += datetime.timedelta(0, delta)
    days = int(curr_time.day)

    if SC_volt <= SC_volt_min or days > days_simulators:
        break

    #print(sens_time, PIR_time)
    #time.sleep(2)
print("node lasted [days]: " + str(curr_time.day))

#Start Plotting
plt.figure(1)
plt.figure(1)
plt.subplot(311)
plt.title(('Simulation while sensing every {0} sec and PIR {1} with {2} events').format(sens_time_orig, PIR, PIR_events))
plt.plot(time_hist, light_hist, 'b-', label = 'SC Percentage', markersize = 10)
plt.ylabel('Light [lux]', fontsize=15)
plt.legend(loc=9, prop={'size': 10})
plt.grid(True)
plt.subplot(312)
plt.plot(time_hist, SC_volt_hist, 'r.', label = 'SC Voltage', markersize = 15)
plt.ylabel('Super Capacitor\nVoltage [V]', fontsize=15)
plt.legend(loc=9, prop={'size': 10})
plt.ylim(2.2,5.6)
plt.grid(True)
plt.subplot(313)
plt.plot(time_hist, PIR_hist, 'k.', label = 'PIR detection', markersize = 15)
plt.ylabel('PIR [boolean]', fontsize=15)
plt.xlabel('Time [h]', fontsize=20)
plt.legend(loc=9, prop={'size': 10})
plt.ylim(-0.25, 1.25)
plt.grid(True)
plt.show()

exit()

fig, ax = plt.subplots(2)
fig.autofmt_xdate()
plt.plot(time_hist, light_hist, 'b^', label = 'SC Percentage', markersize = 10)
plt.plot(time_hist, SC_volt_hist, 'k+', label = 'SC Voltage', markersize = 15)
#plt.plot(Time_hist, SC_Pure_hist, 'b*')
xfmt = mdates.DateFormatter('%m-%d %H:%M')
ax.xaxis.set_major_formatter(xfmt)
ax.tick_params(axis='both', which='major', labelsize=15)
legend = ax.legend(loc='center right', shadow=True)
plt.legend(loc=9, prop={'size': 10})
plt.title('Discharge\n ' + str(time_passed) + ' sec sensing-rate', fontsize=15)
plt.ylabel('Super Capacitor Voltage[V]', fontsize=15)
plt.xlabel('Time [h]', fontsize=20)
plt.grid(True)

plt.show()
