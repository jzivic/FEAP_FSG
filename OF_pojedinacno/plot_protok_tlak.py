import os
import matplotlib.pyplot as plt


pressure = "/home/josip/feap/FSG/automatizacija_34/layer_3/simulacija35/tlakF.csv"
flow = "/home/josip/feap/FSG/automatizacija_34/layer_3/simulacija35/ulazF_ax.csv"


flow = "//home/josip/foamOpen/cases/FSG/cijev/timeVar/cijevCase_3/ulazF.csv"



read_flow = open(flow).readlines()
read_pressure = open(pressure).readlines()




font = {'family' : 'Times New Roman',
        'size'   : 20}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'





time_flow, Q, v = [], [], []
for row in read_flow:
    row = row.strip().split()
    if row[0]=="#":
        continue
    time_flow.append(float(row[0]))
    # Q.append(float(row[1])*0.75e8)
    Q.append(float(row[1])*1e6)
    v.append(float(row[2]))

def Plot_flow():
    fig = plt.figure(dpi=200)
    plt.plot(time_flow, Q)
    plt.title("Volume flow inlet rate ")
    plt.ylabel("Volume flow rate [cm$^{3}$/s]")
    plt.xlabel("Time [sec]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    fig.subplots_adjust(bottom=0.16)  # empty space on the bottom
    fig.subplots_adjust(left=0.16)
    plt.show()

# Plot_flow()



time_pressure, pressure = [], []
for row in read_pressure:
    row = row.strip().split()
    if row[0]=="#":
        continue
    time_pressure.append(float(row[0]))
    pressure.append(float(row[1])*1)

def Plot_pressure():
    fig = plt.figure(dpi=200)
    plt.plot(time_pressure, pressure, label="pressure")
    plt.title("Pressure outlet ")
    plt.ylabel("Pressure [kPa]")
    plt.xlabel("Time [sec]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    fig.subplots_adjust(bottom=0.16)  # empty space on the bottom
    fig.subplots_adjust(left=0.16)
    plt.show()

Plot_pressure()


















