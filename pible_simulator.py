"""
Reinforcement learning.
The RL is in RL_brain.py.
"""

import numpy as np
import datetime
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

SC_Real_min = 0; SC_Real_max = 100; SC_norm_max = 10; SC_norm_min = 0; SC_norm_min_die = 4; SC_Volt_min = 2.1; SC_Volt_max = 5.5; SC_size = 1
Light_Real_min = 0; Light_Real_max= 2000; Light_max = 10; Light_min = 0

I_sleep = 0.0000032; I_BLE_Sens_1 = 0.000210; Time_BLE_Sens_1 = 6.5
V_Solar_200lux = 1.5; I_Solar_200lux = 0.000031; Light_used = 0   # It was 1.5
time_temp = 3600; SC_Pure_init = 97  # 85 for 1 min, 95 for 10 min, 97 for 1 h

Light_hist_1 = []; Perf_hist_1 = []; Time_hist_1 = []; SC_norm_hist_1 = []; SC_Pure_hist_1 = []; SC_temp_hist_1 = []
Light_hist_2 = []; Perf_hist_2 = []; Time_hist_2 = []; SC_norm_hist_2 = []; SC_Pure_hist_2 = []; SC_temp_hist_2 = []
Light_hist_3 = []; Perf_hist_3 = []; Time_hist_3 = []; SC_norm_hist_3 = []; SC_Pure_hist_3 = []; SC_temp_hist_3 = []


Light_hist = []; Perf_hist = []; Time_hist = []; SC_norm_hist = []; SC_Pure_hist = []; SC_temp_hist = []
with open('1min-Discharge.txt') as f:
    content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
counta = 0
time_temp = 200; SC_Pure_init = 97
for i in range(0,len(content)):
    Splitted = content[i].split("|"); Date = Splitted[0].split(" ")
    Split_Date = Date[0].split("/"); Year = int(Split_Date[2]); Day = int(Split_Date[1]); Month = int(Split_Date[0])

    Time = Date[1].split(":"); curr_time_orig = int(Time[0]); curr_time_h = int(Time[0]); curr_time_m = int(Time[1])

    if i == 0:
        init_h = (Day * 24) + curr_time_h;
        curr_time_h = 0;
    else:
        curr_time_h = (Day * 24) + curr_time_h - init_h

    #curr_time_m = min(T_m_List, key=lambda x:abs(x-self.curr_time_m))
    curr_time = datetime.datetime(Year,Month,Day,curr_time_orig,curr_time_m)
    #end_time = datetime.datetime(2018,2,2,curr_time_h,curr_time_m)
    if len(Splitted) > 7:
        Light_Pure = int(Splitted[8])
        if Light_Pure > Light_Real_max:
            Light_Pure = Light_Real_max

        Light_Pure = Light_used * 200
        Light = (((Light_Pure - Light_Real_min) * (Light_max - Light_min)) / (Light_Real_max - Light_Real_min)) + Light_min

        SC_Pure = int(Splitted[5])
        SC_norm = (((SC_Pure - SC_Real_min) * (SC_norm_max - SC_norm_min)) / (SC_Real_max - SC_Real_min)) + SC_norm_min

        perf_Pure = Splitted[4]
        perf = int(perf_Pure);

        if i == 0:
            print SC_Pure
            SC_temp = (SC_Pure_init * 54)/1000.0 #92.01 for 1 min
            Energy_Rem = SC_temp * SC_temp * 0.5 * SC_size
            Volt_Rem = np.sqrt((2*Energy_Rem)/SC_size)
            print SC_temp

        Energy_Used = ((time_temp - Time_BLE_Sens_1) * Volt_Rem * I_sleep) + (Time_BLE_Sens_1 * Volt_Rem * I_BLE_Sens_1)
        Energy_Prod = time_temp * V_Solar_200lux * I_Solar_200lux * Light_used

        Energy_Rem = Energy_Rem - Energy_Used + Energy_Prod

        Volt_Rem = np.sqrt((2*Energy_Rem)/SC_size)
        counta += 1
        if SC_Pure is not 0 and counta == 50:
            counta = 0
            Light_hist_1.append(Light); SC_norm_hist_1.append(SC_norm);  SC_Pure_hist_1.append((SC_Pure/100.0) * 5.4); Time_hist_1.append(curr_time_h); SC_temp_hist_1.append(Volt_Rem)


with open('10min-Discharge.txt') as f:
    content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
Light_hist = []; Perf_hist = []; Time_hist = []; SC_norm_hist = []; SC_Pure_hist = []; SC_temp_hist = []
time_temp = 600; SC_Pure_init = 98
counta = 0
for i in range(0,len(content)):
    Splitted = content[i].split("|"); Date = Splitted[0].split(" ")
    Split_Date = Date[0].split("/"); Year = int(Split_Date[2]); Day = int(Split_Date[1]); Month = int(Split_Date[0])

    Time = Date[1].split(":"); curr_time_h = int(Time[0]); curr_time_m = int(Time[1]); curr_time_orig = int(Time[0]);

    if i == 0:
        init_h = (Day * 24) + curr_time_h;
        curr_time_h = 0;
    else:
        curr_time_h = (Day * 24) + curr_time_h - init_h

    #curr_time_m = min(T_m_List, key=lambda x:abs(x-self.curr_time_m))
    curr_time = datetime.datetime(Year,Month,Day,curr_time_orig,curr_time_m)
    #end_time = datetime.datetime(2018,2,2,curr_time_h,curr_time_m)
    if len(Splitted) > 7:
        Light_Pure = int(Splitted[8])
        if Light_Pure > Light_Real_max:
            Light_Pure = Light_Real_max

        Light_Pure = Light_used * 200
        Light = (((Light_Pure - Light_Real_min) * (Light_max - Light_min)) / (Light_Real_max - Light_Real_min)) + Light_min

        SC_Pure = int(Splitted[5])
        SC_norm = (((SC_Pure - SC_Real_min) * (SC_norm_max - SC_norm_min)) / (SC_Real_max - SC_Real_min)) + SC_norm_min

        perf_Pure = Splitted[4]
        perf = int(perf_Pure);

        if i == 0:
            SC_temp = (SC_Pure_init * 54)/1000.0 #92.01 for 1 min
            Energy_Rem = SC_temp * SC_temp * 0.5 * SC_size
            Volt_Rem = np.sqrt((2*Energy_Rem)/SC_size)

        Energy_Used = ((time_temp - Time_BLE_Sens_1) * Volt_Rem * I_sleep) + (Time_BLE_Sens_1 * Volt_Rem * I_BLE_Sens_1)
        Energy_Prod = time_temp * V_Solar_200lux * I_Solar_200lux * Light_used

        Energy_Rem = Energy_Rem - Energy_Used + Energy_Prod

        Volt_Rem = np.sqrt((2*Energy_Rem)/SC_size)

        #time.sleep(5)
        counta = counta + 1
        if (SC_Pure is not 0) and (counta % 17 == 0):
            Light_hist_2.append(Light); SC_norm_hist_2.append(SC_norm);  SC_Pure_hist_2.append((SC_Pure/100.0) * 5.4); Time_hist_2.append(curr_time_h); SC_temp_hist_2.append(Volt_Rem)

#with open('1h-Discharge.txt') as f:
with open('5sec-Discharge.txt') as f:
    content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
Light_hist = []; Perf_hist = []; Time_hist = []; SC_norm_hist = []; SC_Pure_hist = []; SC_temp_hist = []
#time_temp = 3600; SC_Pure_init = 100 # for 1 hour
time_temp = 15; SC_Pure_init = 102

counta = 0
for i in range(0,len(content)):
    Splitted = content[i].split("|"); Date = Splitted[0].split(" ")
    Split_Date = Date[0].split("/"); Year = int(Split_Date[2]); Day = int(Split_Date[1]); Month = int(Split_Date[0])

    Time = Date[1].split(":"); curr_time_h = int(Time[0]); curr_time_m = int(Time[1]); curr_time_orig = int(Time[0]);

    if i == 0:
        init_h = (Day * 24) + curr_time_h;
        curr_time_h = 0;
    else:
        curr_time_h = (Day * 24) + curr_time_h - init_h

    #curr_time_m = min(T_m_List, key=lambda x:abs(x-self.curr_time_m))
    curr_time = datetime.datetime(Year,Month,Day,curr_time_orig,curr_time_m)
    #end_time = datetime.datetime(2018,2,2,curr_time_h,curr_time_m)
    if len(Splitted) > 7:
        Light_Pure = int(Splitted[8])
        if Light_Pure > Light_Real_max:
            Light_Pure = Light_Real_max

        Light_Pure = Light_used * 200
        Light = (((Light_Pure - Light_Real_min) * (Light_max - Light_min)) / (Light_Real_max - Light_Real_min)) + Light_min

        SC_Pure = int(Splitted[5])
        SC_norm = (((SC_Pure - SC_Real_min) * (SC_norm_max - SC_norm_min)) / (SC_Real_max - SC_Real_min)) + SC_norm_min

        perf_Pure = Splitted[4]
        perf = int(perf_Pure);

        if i == 0:
            print SC_Pure
            SC_temp = (SC_Pure_init * 54)/1000.0 #92.01 for 1 min
            Energy_Rem = SC_temp * SC_temp * 0.5 * SC_size
            Volt_Rem = np.sqrt((2*Energy_Rem)/SC_size)
            print SC_temp

        Energy_Used = ((time_temp - Time_BLE_Sens_1) * Volt_Rem * I_sleep) + (Time_BLE_Sens_1 * Volt_Rem * I_BLE_Sens_1)
        Energy_Prod = time_temp * V_Solar_200lux * I_Solar_200lux * Light_used

        Energy_Rem = Energy_Rem - Energy_Used + Energy_Prod

        Volt_Rem = np.sqrt((2*Energy_Rem)/SC_size)

        counta += 1
        if SC_Pure is not 0 and counta % 200 == 0:
            Light_hist_3.append(Light); SC_norm_hist_3.append(SC_norm);  SC_Pure_hist_3.append((SC_Pure/100.0) * 5.4); Time_hist_3.append(curr_time_h); SC_temp_hist_3.append(Volt_Rem)


#Start Plotting
fig, ax = plt.subplots(1)
plt.figure(figsize=(10.0, 3.0))

plt.subplot(1, 3, 2)

fig.autofmt_xdate()
plt.plot(Time_hist_1, SC_Pure_hist_1, 'r^', label = 'SC_Volt Real', markersize = 10)
plt.plot(Time_hist_1, SC_temp_hist_1, 'k+', label = 'SC_Volt Simulated', markersize = 15)
#plt.plot(Time_hist, SC_Pure_hist, 'b*')
xfmt = mdates.DateFormatter('%H')
ax.xaxis.set_major_formatter(xfmt)
ax.tick_params(axis='both', which='major', labelsize=15)
legend = ax.legend(loc='center right', shadow=True)
plt.legend(loc=9, prop={'size': 10})
plt.title('Discharge\n 1 min Sense-Rate', fontsize=15)
plt.ylabel('Super Capacitor Voltage[V]', fontsize=15)
plt.xlabel('Time [h]', fontsize=20)
plt.grid(True)


plt.subplot(1, 3, 3)
fig.autofmt_xdate()
#plt.plot(Time_hist, Light_hist, 'b', label = 'Light')
plt.plot(Time_hist_2, SC_Pure_hist_2, 'r^', label = 'SC_Volt Real', markersize = 10)
plt.plot(Time_hist_2, SC_temp_hist_2, 'k+', label = 'SC_Volt Simulated', markersize = 15)
#plt.plot(Time_hist, SC_Pure_hist, 'b*')
xfmt = mdates.DateFormatter('%H')
ax.xaxis.set_major_formatter(xfmt)
ax.tick_params(axis='both', which='major', labelsize=10)
legend = ax.legend(loc='center right', shadow=True)
plt.legend(loc=9, prop={'size': 10})
plt.title('Discharge\n 10 mins Sense-Rate', fontsize=15)
plt.ylabel('Super Capacitor Voltage[V]', fontsize=15)
plt.xlabel('Time [h]', fontsize=20)
plt.grid(True)
#fig.savefig('Images-Auto/' + Text + '.png', bbox_inches='tight')

plt.subplot(1, 3, 1)
fig.autofmt_xdate()
#plt.plot(Time_hist, Light_hist, 'b', label = 'Light')
plt.plot(Time_hist_3, SC_Pure_hist_3, 'r^', label = 'SC_Volt Real', markersize = 13)
plt.plot(Time_hist_3, SC_temp_hist_3, 'k+', label = 'SC_Volt Simulated', markersize = 18)
#plt.plot(Time_hist, SC_Pure_hist, 'b*')
xfmt = mdates.DateFormatter('%m-%d-%y %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
ax.tick_params(axis='both', which='major', labelsize=10)
legend = ax.legend(loc='center right', shadow=True)
plt.legend(loc=9, prop={'size': 10})
plt.title('Discharge\n 15 sec Sense-Rate', fontsize=15)
plt.ylabel('Super Capacitor Voltage[V]', fontsize=15)
plt.xlabel('Time [h]', fontsize=20)
plt.grid(True)
#fig.savefig('Images-Auto/' + Text + '.png', bbox_inches='tight')

plt.show()
plt.close(fig)
