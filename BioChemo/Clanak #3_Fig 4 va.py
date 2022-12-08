from user_functions.Classes_Functions import ReadNodeFile2
from user_functions.Classes_Functions import ReadContourFiles
import matplotlib.pyplot as plt

# Set working directory
# work_dir = r"C:\Users\Nino\Desktop\Nino FEAP\FEAP_model_redesign\Analize\Build test - ILT"
# work_dir = work_dir + r"\95 - grafovi za članak\4 - Figure 4"




work_dir = "//home/josip/feap/FSG/automatizacija_40/4_Figure4/"





# Flag for outer nodes
num_of_files = 4
# timestep = [-1,300,400,-1,-1]
timestep = [297,297,297,297,297]

# Starting step of ILT growth
ilt_start_step = [0,49,130,186,230]

# Step in which stress exceeds 0.5 MPa
break_step = [267,0,0,0,0]

# Files paths and names
rin_path = [r"res__NODE_0841_96-1",
            r"res__NODE_0841_96-6",
            r"res__NODE_0841_96-4",
            r"res__NODE_0841_96-2",
            r"res__NODE_0841_91-6"
            ]

inner_path = [r"res__INNER_lines__96-1",
              r"res__INNER_lines__96-6",
              r"res__INNER_lines__96-4",
              r"res__INNER_lines__96-2",
              r"res__INNER_lines__91-6"
              ]

outer_path = [r"res__OUTER_lines__96-1",
              r"res__OUTER_lines__96-6",
              r"res__OUTER_lines__96-4",
              r"res__OUTER_lines__96-2",
              r"res__OUTER_lines__91-6"
              ]

ilt_path = [r"res__ILT_lines__96-1",
            r"res__ILT_lines__96-6",
            r"res__ILT_lines__96-4",
            r"res__ILT_lines__96-2",
            r"res__ILT_lines__91-6"
            ]

# Legend entries
legend1 = ["No ILT",
          r"$R_{lumen} = 10$ mm",
          r"$R_{lumen} = 12$ mm",
          r"$R_{lumen} = 14$ mm",
          r"$R_{lumen} = 16$ mm"
          ]

legend2 = ["No ILT",
          r"$R_{\mathrm{lum}} = 10$ mm",
          r"$R_{\mathrm{lum}} = 12$ mm",
          r"$R_{\mathrm{lum}} = 14$ mm",
          r"$R_{\mathrm{lum}} = 16$ mm"
          ]

# File names for saving plots
fig1_name = work_dir + "/Fig_4_col1"

# Set absolute paths and read files
data = []
datac = []
n = len(rin_path)
for i in range(n):
    abs_path_rin = work_dir + "/" + rin_path[i]
    abs_path_rout = work_dir + "NODE_outer"
    abs_path_inner = work_dir + "/" + inner_path[i]
    abs_path_outer = work_dir + "/" + outer_path[i]
    abs_path_ilt = work_dir + "/" + ilt_path[i]
    data.append(ReadNodeFile2(abs_path_rin, abs_path_rout))
    datac.append(ReadContourFiles(abs_path_inner, abs_path_outer, abs_path_ilt))

# ----------------------------------------------------------------------------------------------------------------------

# Color definition
c1 = '#1f77b4'      # blue
c2 = '#ff7f0e'      # orange
c3 = '#2ca02c'      # green
c4 = '#d62728'      # red
c5 = '#9467bd'      # purple
c6 = '#8c564b'      # brown
c7 = '#e377c2'      # pink
c8 = '#7f7f7f'      # gray
c9 = '#bcdb22'      # light green
c10 = '#17becf'     # cyan
c11 = '#fdbc1d'     # yelow

col1 = ['k', c4, c3, c1, 'k']
linija = ['-','-','-','-','-']
marker_type = ['','o','d','^','s']
symbol_position = [0,280,280,280,280]

# Defining figure
plt.figure(1, [7.0, 4.5], 600)
p1 = plt.subplot2grid((1,12),(0,0),rowspan=1,colspan=6)
p2 = plt.subplot2grid((1,12),(0,8),rowspan=1,colspan=4)
# p1 = plt.subplot2grid((1,12),(0,0),rowspan=1,colspan=5)
# p2 = plt.subplot2grid((1,12),(0,7),rowspan=1,colspan=5)

# Plotting first subplot
for i in [0,3,2,1]:
    x = data[i].time
    y = data[i].radius_rin
    # p1.plot(x, y, color=col1[i], label=legend1[i], linestyle=linija[i], zorder=1)
    p1.plot(x, y, color=col1[i], linestyle=linija[i], zorder=2)
    if i>10:
        p1.scatter(x[break_step[i]], y[break_step[i]], color=col1[i], marker='x', s=30)
    if i>0:
        p1.scatter(x[ilt_start_step[i]], y[ilt_start_step[i]], color=col1[i], marker='o', s=25, zorder=3)
        p1.scatter(x[symbol_position[i]], y[symbol_position[i]], color=col1[i], marker=marker_type[i], s=25,
                   facecolor='w', zorder=3)

# p1.set_xlim(0,5200)
# p1.set_ylim(9,41)
p1.set_xlim(0,3260)
p1.set_ylim(9,24)
p1.set_title("(a)")
p1.set_xlabel("Time [days]")
p1.set_ylabel("Inner wall radius [mm]")
p1.grid(which='both', linestyle='--', linewidth='0.5')
p1.legend(facecolor='w', framealpha=1.0) #, bbox_to_anchor=(1.0,0.8))
p1.spines['top'].set_visible(False)
p1.spines['right'].set_visible(False)

# Plotting second subplot
n = 0
for k in [0,3,2,1]:
    R_ilt = datac[k].R_line1_ilt[timestep[k]]
    R_inn = datac[k].R_line1_inn[timestep[k]]
    z_ilt = datac[k].z_line1_ilt[timestep[k]]
    z_inn = datac[k].z_line1_inn[timestep[k]]
    if k>0:
        # p2.plot(R_ilt, z_ilt, linestyle=':', color=col1[n], label=legend2[n], zorder=2)
        p2.plot(R_ilt, z_ilt, linestyle=':', color=col1[k], zorder=2, label="Thrombus")
        # p2.plot(R_ilt, z_ilt, linestyle=':', color=col1[n], label=legend2[n],
        #          marker=marker_type[k], markersize=4, markerfacecolor='w')
    # p2.plot(R_inn, z_inn, linestyle='-', color=col1[n], label=legend2[n], zorder=2)
    p2.plot(R_inn, z_inn, linestyle='-', color=col1[k], label="Inner wall", zorder=2)
    # p2.plot(R_inn, z_inn, linestyle='-', color=col1[n], label=legend2[n],
    #          marker=marker_type[k], markersize=4, markerfacecolor='w')
    p2.scatter(R_ilt[55+k*3], z_ilt[55+k*3], color=col1[k],marker=marker_type[k], s=25, facecolor='w', zorder=3)
    p2.scatter(R_inn[50+k*3], z_inn[50+k*3], color=col1[k],marker=marker_type[k], s=25, facecolor='w', zorder=3, label=legend2[k])

    n = n + 1

# p2.set_xlim(8,42)
p2.set_xlim(8,21)
p2.set_ylim(75,275)
p2.set_title("(b)")
# p2.set_xlabel("Radius [mmm]")
p2.set_xlabel("Radius [mmm]")
p2.set_ylabel(r"Axial coordinate $z$ [mm]")
p2.grid(which='both', linestyle='--', linewidth='0.5')
p2.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,1.0))
p2.spines['top'].set_visible(False)
p2.spines['right'].set_visible(False)

plt.savefig(fig1_name, bbox_inches='tight')
plt.show()
plt.close(1)

