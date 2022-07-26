import os, math, itertools
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt


# input = "//home/josip/foamOpen/cases/turbulencija/casson_2/ulazF_ax.csv"
# output = "//home/josip/foamOpen/cases/turbulencija/casson_2/output.csv"

# input = "//home/josip/foamOpen/cases/turbulencija/casson_2/ulazF_ax.csv"

input = "//home/josip/feap/FSG/automatizacija_39/tawss_turbulent_Newt_5/prototipCase_foam/ulazF_ax.csv"




wholeDoc_input = open(input, "r").readlines()
input_len = sum([1 for i in wholeDoc_input])


turb_lenght = 0.001     # ovako naštimano poklapa sa filipovim podacima
intensity = 0.03
viscosity = 3.3e-6
radius = 0.01


time, Q, velocity, k, nut = [], [], [], [], []
Reynolds, turb_energy, omega = [], [], []





for n in range(input_len):


    line = wholeDoc_input[n].strip().split()
    if n==0: continue

    t, flow, v = float(line[0]), float(line[1]), float(line[2])
    time.append(t), Q.append(flow), velocity.append(v)

    Re = abs(v)*radius / viscosity
    k = 1.5 * (intensity*v)**2
    omg = math.sqrt(k) / ((0.09**0.25) * turb_lenght)

    Reynolds.append(Re), turb_energy.append(k), omega.append(omg)

    print(k, omg)
    # print(omg)






