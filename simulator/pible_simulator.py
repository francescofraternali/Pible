"""
Pible Simulator
"""

import numpy as np
import datetime
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# Parameter to change
time_passed = 900 # Sensing data every "time_passed" time. In seconds.
SC_perc_init = 100 # Super Capacitor initial voltage. Put "100" for maximum capacity at the beginning of the experiment
light_lux = 250 # Average of light the solar panel receive during the "light_hours_per day"
light_hours_per_day = 8 #starting from 8AM the system receive "light_lux" light for "light_hours_per_day" time
days_simulators = 7 # Leave the simulaor running for this amount of time unless the node dies before such time


# DO NOT MODIFY!  POWER CONSUMPTION PARAMETERS!
SC_perc_min = 0; SC_perc_max = 100.0; SC_norm_max = 10; SC_norm_min = 0; SC_norm_min_die = 4; SC_volt_min = 2.1; SC_volt_max = 5.5; SC_size = 1.5
light_real_min = 0; light_real_max= 2000; light_max = 10; light_min = 0

i_sleep = 0.0000032; i_BLE_sens_1 = 0.000210; time_BLE_sens_1 = 6.5
v_solar_200_lux = 1.5; i_solar_200_lux = 0.000031; # It was 1.5
p_solar_1_lux = (v_solar_200_lux * i_solar_200_lux) / 200.0

light_hist = []; time_hist = []; SC_norm_hist = []; SC_perc_hist = []; SC_volt_hist = []

# Starting Simulator
SC_volt = (SC_perc_init/SC_perc_max) * SC_volt_max
SC_perc = SC_perc_init
energy_rem = SC_volt * SC_volt * 0.5 * SC_size
curr_time = datetime.datetime.now()
curr_time = curr_time.replace(month=1, day=1, hour=0, minute=0, second=0)
light = light_lux

while True:

    light_norm = (((light - light_real_min) * (light_max - light_min)) / (light_real_max - light_real_min)) + light_min
    SC_norm = (((SC_volt - SC_perc_min) * (SC_norm_max - SC_norm_min)) / (SC_perc_max - SC_perc_min)) + SC_norm_min

    energy_used = ((time_passed - time_BLE_sens_1) * SC_volt * i_sleep) + (time_BLE_sens_1 * SC_volt * i_BLE_sens_1)

    if int(curr_time.hour) >= 8 and int(curr_time.hour) <= 8 + light_hours_per_day:
        light = light_lux
    else:
        light = 0

    energy_prod = time_passed * p_solar_1_lux * light

    # Update energy value for next iteration
    energy_rem = energy_rem - energy_used + energy_prod
    #print(light)
    #print("energy used", energy_used)
    #print("energy prod", energy_prod)
    SC_volt = np.sqrt((2*energy_rem)/SC_size)

    if SC_volt > SC_volt_max:
        SC_volt = SC_volt_max

    energy_rem = SC_volt * SC_volt * 0.5 * SC_size

    SC_perc = (SC_volt/SC_volt_max) * 100

    light_hist.append(light); SC_norm_hist.append(SC_norm);  SC_perc_hist.append(SC_perc); time_hist.append(curr_time); SC_volt_hist.append(SC_volt)


    curr_time += datetime.timedelta(0, time_passed)
    days = int(curr_time.day)

    if SC_volt <= SC_volt_min or days > days_simulators:
        break

print("node lasted [days]: " + str(curr_time.day))

#Start Plotting
plt.figure(1)
plt.figure(1)
plt.subplot(211)
plt.title('Discharge\n ' + str(time_passed) + ' sec sensing-rate', fontsize=15)
plt.plot(time_hist, light_hist, 'b^', label = 'SC Percentage', markersize = 10)
plt.ylabel('Light [lux]', fontsize=15)
plt.legend(loc=9, prop={'size': 10})
plt.grid(True)
plt.subplot(212)
plt.plot(time_hist, SC_volt_hist, 'r.', label = 'SC Voltage', markersize = 15)
plt.ylabel('Super Capacitor\nVoltage [V]', fontsize=15)
plt.xlabel('Time [h]', fontsize=20)
plt.legend(loc=9, prop={'size': 10})
plt.grid(True)
plt.show()

fig, ax = plt.subplots(2)

exit()


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
