from BioChemo.user_functions.Classes_Functions import ReadNodeFile2
from BioChemo.user_functions.Classes_Functions import ReadRonodFile
from BioChemo.user_functions.Classes_Functions import ReadResY0File
from BioChemo.user_functions.Classes_Functions import ReadResY0ILTFile
from BioChemo.user_functions.Classes_Functions import ReadMiddleFile
import matplotlib.pyplot as plt


# work_dir = "//home/josip/feap/FSG/automatizacija_33_N_AVERAGE/radial/radial_tawss_40_d01"
# work_dir = "//home/josip/feap/FSG/automatizacija_41/biochemo_1"     # nove verzije s restartom


work_dir = "//home/josip/feap/FSG/automatizacija_41/biochemo_3D"
# work_dir = "//home/josip/feap/FSG/automatizacija_41/biochemo_proba"





# --- Files ---
num_of_files =          1
folder =                "172-"
legend_folder =         "172-"
simulations =           ["22"]

# --- NODE file ---
plot_inner_radius =     False
plot_wall_thickness =   False
plot_stress =           False
plot_target_gr_rate =   False
rin_node =              "0841"
# rin_node =              "1401"
rout_node =             "0847"
# rout_node =             "1047"

# --- RONOD file ---
plot_ronod_node =       False
plot_ronod_axial =      False
ronod_node =            847
ronod_axial_timesteps = [-1]


# --- RES_Y0 file ---
plot_res_y0_ILT =       False
plot_res_y0_radial =    False
# res_y0_z_coordinates =  [175,215,250]
# res_y0_z_coordinates =  [175]
res_y0_z_coordinates =  [150]
plot_res_y0_inner =     True           #1
plot_res_y0_outer =     True
plot_res_y0_time_inn =  False              #2
plot_res_y0_time_out =  False
rin_node_y0 =           [841,1303,1485]
# rin_node_y0 =           [1401]
rout_node_y0 =          [847,1309,1491]
# rout_node_y0 =          [1407]
# res_y0_timesteps =      [50,85]
res_y0_timesteps =      [250, 300, 350]

# --- Flags ---
plot_elas =             False
plot_MMP =              False
plot_coll_and_SMC =     False

# --- MIDDLE file ---
plot_middle_s11 =       False
plot_middle_s22 =       False
plot_middle_s33 =       False
plot_middle_p =         False
middle_timesteps =      [-1]
num_nodes_rad =         847


# Plot titles
plot_title = "172 - biochemo - fuzi"

# File names for saving plots
name = f"172_bio_fuzi_plot_1_{simulations[0]}"

legend_type = 2
legend_v2 = ["172-1, no ILT",
             "172-5, p1~08, wqm0020, K_VV_02_45"
            ]


# Color definition
blue = '#1f77b4'
orange = '#ff7f0e'
green = '#2ca02c'
red = '#d62728'
purple = '#9467bd'
brown = '#8c564b'
pink = '#e377c2'
gray = '#7f7f7f'

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

# Color definition
# col = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
col = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcdb22','#17becf','b', 'g']
# col = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
linija = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
linije_josip = ['-', '--', '-.']
sekcije = ["A", "B", "C"]


color_type = 2
# 1 - different colors for files
# 2 - different colors for timesteps
# 3 - different colors for z





# ==================================================================================================================== #

# File names for saving plots
fig_name_rin = work_dir + "/Inner_diameter_case-" + name
fig_name_wall = work_dir + "/Wall_thickness_case-" + name
fig_name_sin = work_dir + "/Stresses_on_inner_node_case-" + name
fig_name_sout = work_dir + "/Stresses_on_outer_node_case-" + name
fig_name_ronod_node = work_dir + "/Ronod_node_case-" + name
fig_name_ronod_axial = work_dir + "/Ronod_axial_case-" + name
fig_name_res_y0_rad = work_dir + "/ResY0_radial_case-" + name
fig_name_res_y0_vertical = work_dir + "/ResY0_vertical_case-" + name
fig_name_res_y0_time = work_dir + "/ResY0_time_case-" + name
fig_name_middle_s11 = work_dir + "/Middle_line_s11_case-" + name
fig_name_middle_s22 = work_dir + "/Middle_line_s22_case-" + name
fig_name_middle_s33 = work_dir + "/Middle_line_s33_case-" + name
fig_name_middle_p = work_dir + "/Middle_line_p_case-" + name
fig_name_fig2 = work_dir + f"/Figure_2_v1_{simulations[0]}_200z"

# Files paths and names
rin_path = []
rout_path = []
ronod_path = []
res_y0_path = []
res_y0_ILT_path = []
middle_path = []
legend_v1 = []
if num_of_files > len(simulations):
    num_of_files = len(simulations)
for i in range(num_of_files):
    name_in = r"res__NODE_" + rin_node + "_" + folder + simulations[i]
    name_out = r"res__NODE_" + rout_node + "_" + folder + simulations[i]
    name_legend = legend_folder + simulations[i]
    name_ronod = r"res__RONOD_field__" + folder + simulations[i]
    name_res_y0 = r"res__Y0_field__" + folder + simulations[i]
    name_res_ILT_y0 = r"res__ILT_Y0_field__" + folder + simulations[i]
    name_middle = r"res__MIDDLE_line__" + folder + simulations[i]
    rin_path.append(name_in)
    rout_path.append(name_out)
    legend_v1.append(name_legend)
    ronod_path.append(name_ronod)
    res_y0_path.append(name_res_y0)
    res_y0_ILT_path.append(name_res_ILT_y0)
    middle_path.append(name_middle)

# Set absolute paths and read files
data_node = []
data_ronod = []
data_y0 = []
data_y0_ILT = []
data_middle = []
n = len(rin_path)
for i in range(n):
    abs_path_rin = work_dir + "/" + rin_path[i]
    if plot_wall_thickness:
        abs_path_rout = work_dir + "/" + rout_path[i]
    else:
        abs_path_rout = "NODE_outer"
    if plot_inner_radius or plot_wall_thickness:
        data_node.append(ReadNodeFile2(abs_path_rin, abs_path_rout))
    if plot_ronod_node or plot_ronod_axial:
        abs_path_ronod = work_dir + "/" + ronod_path[i]
        data_ronod.append(ReadRonodFile(abs_path_ronod))
    if plot_res_y0_radial or plot_res_y0_inner or plot_res_y0_outer or plot_res_y0_time_inn or plot_res_y0_time_out:
        abs_path_res_y0 = work_dir + "/" + res_y0_path[i]
        data_y0.append(ReadResY0File(abs_path_res_y0))
    if plot_res_y0_ILT:
        abs_path_res_y0_ILT = work_dir + "/" + res_y0_ILT_path[i]
        data_y0_ILT.append(ReadResY0ILTFile(abs_path_res_y0_ILT))
    if plot_middle_p or plot_middle_s11:
        abs_path_middle = work_dir + "/" + middle_path[i]
        data_middle.append(ReadMiddleFile(abs_path_middle))

# -------------------------------------------------------------------------------------------------------------------- #

# Example for printing data: data[simulation_number].print_line(timestep)
if plot_inner_radius:
    data_node[0].print_line(0)
    # data[1].print_line(100)

# -------------------------------------------------------------------------------------------------------------------- #
#  INNER RADIUS  #

if plot_inner_radius:
    plt.figure(1, [6.0, 4.0], 200)
    for i in range(num_of_files):
        x = data_node[i].time
        y = data_node[i].radius_rin
        if legend_type == 2:
            plt.plot(x, y, color=col[i], label=legend_v2[i], linestyle=linija[i])
        else:
            plt.plot(x, y, color=col[i], label=legend_v1[i], linestyle=linija[i])

        if plot_target_gr_rate and i == 1:
            rate1 = []
            rate2 = []
            for j in x:
                rate1.append(2 * j / 365 + 10)
                rate2.append(2.5 * j / 365 + 10)
            plt.plot(x, rate1, color='k', linestyle='--')
            plt.plot(x, rate2, color='k', linestyle='--')

    # plt.xlim(0,10000)
    # plt.ylim(10,50)
    plt.title(plot_title)
    plt.xlabel("Time [days]")
    plt.ylabel("Inner radius [mm]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    # plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,-0.2))
    plt.savefig(fig_name_rin, bbox_inches='tight')
    plt.show()
    plt.close(1)

# -------------------------------------------------------------------------------------------------------------------- #
#  WALL THICKNESS  #

if plot_wall_thickness:
    plt.figure(2, [6.0, 4.0], 200)
    for i in range(num_of_files):
        x = data_node[i].time
        y = data_node[i].wall_thickness
        if legend_type == 2:
            plt.plot(x, y, color=col[i], label=legend_v2[i], linestyle=linija[i])
        else:
            plt.plot(x, y, color=col[i], label=legend_v1[i], linestyle=linija[i])

    # plt.xlim(0,10000)
    # plt.ylim()
    plt.title(plot_title)
    plt.xlabel("Time [days]")
    plt.ylabel("Wall thickness [mm]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,-0.2))
    plt.savefig(fig_name_wall, bbox_inches='tight')
    plt.show()
    plt.close(2)

# -------------------------------------------------------------------------------------------------------------------- #
#  STRESSES  #

if plot_stress:
    plt.figure(3, [7.0, 5.5], 200)
    for i in range(num_of_files):
        x = data_node[i].time
        s11 = data_node[i].S11in
        s22 = data_node[i].S22in
        s33 = data_node[i].S33in
        if legend_type == 2:
            plt.plot(x, s11, color=col[i], linestyle=':', label="S11, " + legend_v2[i])
            plt.plot(x, s22, color=col[i], linestyle='-', label="S22, " + legend_v2[i])
            plt.plot(x, s33, color=col[i], linestyle='--', label="S33, " + legend_v2[i])
        else:
            plt.plot(x, s11, color=col[i], linestyle=':', label="S11, " + legend_v1[i])
            plt.plot(x, s22, color=col[i], linestyle='-', label="S22, " + legend_v1[i])
            plt.plot(x, s33, color=col[i], linestyle='--', label="S33, " + legend_v1[i])

    # plt.xlim(0,10000)
    # plt.ylim(0.07,0.21)
    plt.title(plot_title)
    plt.xlabel("Time [days]")
    plt.ylabel("Stresses on inner node [MPa]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    lgd = plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,1.0))
    plt.savefig(fig_name_sin, bbox_inches='tight')
    plt.show()
    plt.close(3)

if plot_stress and plot_wall_thickness:
    plt.figure(4, [7.0, 5.5], 200)
    for i in range(num_of_files):
        x = data_node[i].time
        s11 = data_node[i].S11out
        s22 = data_node[i].S22out
        s33 = data_node[i].S33out
        if legend_type == 2:
            plt.plot(x, s11, color=col[i], linestyle=':', label="S11, " + legend_v2[i])
            plt.plot(x, s22, color=col[i], linestyle='-', label="S22, " + legend_v2[i])
            plt.plot(x, s33, color=col[i], linestyle='--', label="S33, " + legend_v2[i])
        else:
            plt.plot(x, s11, color=col[i], linestyle=':', label="S11, " + legend_v1[i])
            plt.plot(x, s22, color=col[i], linestyle='-', label="S22, " + legend_v1[i])
            plt.plot(x, s33, color=col[i], linestyle='--', label="S33, " + legend_v1[i])

    # plt.xlim(0,10000)
    # plt.ylim(0.07,0.21)
    plt.title(plot_title)
    plt.xlabel("Time [days]")
    plt.ylabel("Stresses on outer node [MPa]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,1.0))
    plt.savefig(fig_name_sout, bbox_inches='tight')
    plt.show()
    plt.close(4)


# -------------------------------------------------------------------------------------------------------------------- #
#  RES_Y0 and RES_Y0_ILT #

# Defining figure
# plt.figure(11, [8.0, 7.0], 600)
# plt.figure(11, [8.0, 7.0], 100)
# p1 = plt.subplot2grid((12,14),(0,0),rowspan=12,colspan=5)
# p2 = plt.subplot2grid((12,14),(0,7),rowspan=6,colspan=8)

if plot_res_y0_radial:
    # plt.figure(5, [6.0, 4.0], 200)
    tol = 0.5
    for k in range(num_of_files):
        for i in range(len(res_y0_timesteps)):
            for j in range(len(res_y0_z_coordinates)):
                zz = res_y0_z_coordinates[j]
                timestep = res_y0_timesteps[i]
                list_z = data_y0[k].zcoor[timestep-1]
                list_r = data_y0[k].radius[timestep-1]
                list_M_elas = data_y0[k].M_elas[timestep-1]
                list_M_MMP = data_y0[k].M_MMP[timestep-1]
                R = []
                M_elas = []
                M_MMP = []
                for m in range(len(list_z)):
                    z = list_z[m]
                    if z > (zz-tol) and z < (zz+tol):
                        R.append(list_r[m])
                        M_elas.append(list_M_elas[m])
                        M_MMP.append(list_M_MMP[m])

                if color_type == 3:
                    c = j
                elif color_type == 2:
                    c = i
                else:
                    c = k
                if legend_type == 2:
                    if plot_elas:
                        print(timestep, R)
                        plt.plot(R, M_elas, color=col[c], label=f"elas, t{timestep}, "+legend_v2[k], linestyle='--')
                        plt.scatter(R[-1], M_elas[-1], color=col[c], marker='o', s=7)
                    if plot_MMP:
                        plt.plot(R, M_MMP, color=col[c], label=f"MMP, t{timestep}, "+legend_v2[k], linestyle=':')
                        plt.scatter(R[-1], M_MMP[-1], color=col[c], marker='o', s=7)
                else:
                    if plot_elas:
                        plt.plot(R, M_elas, color=col[c], label=f"elas, t{timestep}, " + legend_v1[k], linestyle='--')
                        plt.scatter(R[-1], M_elas[-1], color=col[c], marker='o', s=7)
                    if plot_MMP:
                        plt.plot(R, M_MMP, color=col[c], label=f"MMP, t{timestep}, " + legend_v1[k], linestyle=':')
                        plt.scatter(R[-1], M_MMP[-1], color=col[c], marker='o', s=7)

                if plot_res_y0_ILT:
                    # timestep (zadani za koji crtam)
                    list_timesteps = data_y0_ILT[k].timestep
                    n = -1
                    for m in range(len(list_timesteps)):
                        if int(list_timesteps[m]) == timestep:
                            n = m
                    if n > 0:
                        list_z_ILT = data_y0_ILT[k].zcoor[n]
                        list_r_ILT = data_y0_ILT[k].radius[n]
                        list_M_elas_ILT = data_y0_ILT[k].M_elas[n]
                        list_M_MMP_ILT = data_y0_ILT[k].M_MMP[n]
                        R_ILT = []
                        M_elas_ILT = []
                        M_MMP_ILT = []
                        dot = True
                        for m in range(len(list_z_ILT)):
                            z = list_z_ILT[m]
                            if z > (zz - tol) and z < (zz + tol):
                                if list_M_elas_ILT[m] == 0.0 and list_M_MMP_ILT[m] == 0.0:
                                    dot = False
                                else:
                                    R_ILT.append(list_r_ILT[m])
                                    M_elas_ILT.append(list_M_elas_ILT[m])
                                    M_MMP_ILT.append(list_M_MMP_ILT[m])
                        if plot_elas:
                            plt.plot(R_ILT, M_elas_ILT, color=col[c], linestyle='--')
                            plt.scatter(R_ILT[-1], M_elas_ILT[-1], color=col[c], marker='d', s=15)
                            if dot:
                                plt.scatter(R_ILT[0], M_elas_ILT[0], color=col[c], marker='o', s=7)
                        if plot_MMP:
                            plt.plot(R_ILT, M_MMP_ILT, color=col[c], linestyle=':')
                            plt.scatter(R_ILT[-1], M_MMP_ILT[-1], color=col[c], marker='d', s=15)
                            if dot:
                                plt.scatter(R_ILT[0], M_MMP_ILT[0], color=col[c], marker='o', s=7)
    # plt.xlim(0,10000)
    # plt.ylim(16,24)
    plt.title(plot_title)
    plt.xlabel("Radius [mm]")
    plt.ylabel("Normalized enzyme concentration [g]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    # plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,-0.1))
    plt.savefig(fig_name_res_y0_rad, bbox_inches='tight')
    plt.show()
    plt.close(5)



def plot_enzyme_contour():
    font = {'family': 'Times New Roman',
            'size': 22}
    plt.rc('font', **font)
    plt.rcParams['mathtext.fontset'] = 'stix'

    fig = plt.figure(figsize=(5.2, 7.2), dpi=100)
    fig.subplots_adjust(left=0.21, top=0.95, right = 0.86, bottom=0.15)

    for k in range(num_of_files):
        list_node = data_y0[k].node[0]
        list_z = data_y0[k].zcoor[0]
        inner_nodes = []
        outer_nodes = []
        z0 = 0
        for m in range(len(list_node)):
            if m == 0:
                z0 = list_z[m]
                inner_nodes.append(m)
                pass
            if list_z[m] != z0:
                z0 = list_z[m]
                inner_nodes.append(m)
                outer_nodes.append(m-1)
        outer_nodes.append(len(list_node)-1)

        for i in range(len(res_y0_timesteps)):
            timestep = res_y0_timesteps[i]
            list_z = data_y0[k].zcoor[timestep-1]
            list_M_elas = data_y0[k].M_elas[timestep-1]
            list_M_MMP = data_y0[k].M_MMP[timestep-1]
            z_inn = []
            M_elas_inn = []
            M_MMP_inn = []
            for m in range(len(inner_nodes)):
                z_inn.append(list_z[inner_nodes[m]])
                M_elas_inn.append(list_M_elas[inner_nodes[m]] / 0.001558)
                M_MMP_inn.append(list_M_MMP[inner_nodes[m]])
            z_out = []
            M_elas_out = []
            M_MMP_out = []
            for m in range(len(outer_nodes)):
                z_out.append(list_z[outer_nodes[m]])
                M_elas_out.append(list_M_elas[outer_nodes[m]] / 0.001558)
                M_MMP_out.append(list_M_MMP[outer_nodes[m]])

            if plot_res_y0_outer:
                plt.plot(M_elas_out, z_out, color=c1, linestyle=linije_josip[i],
                        label=r"$r_{\mathrm{out}},$ $\tau=$" + str(timestep * 10) + " d")
            if plot_res_y0_inner:
                plt.plot(M_elas_inn, z_inn, color=c2, linestyle=linije_josip[i],
                         label=r"$r_{\mathrm{in}},$  $\tau=$" + str(timestep * 10) + " d")

    plt.xlim(-2,10)
    plt.ylim(-10,200)
    plt.figtext(0.05, 0.065, "$b)$")
    plt.xlabel("Normalized enzyme concentration")
    plt.ylabel(r"Axial coordinate $z$ [mm]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.03, handletextpad=0.1,
               handlelength=0.8, borderaxespad=0.05)
    plt.savefig(fig_name_res_y0_vertical, bbox_inches='tight', dpi=300)
    plt.show()


# plot_enzyme_contour()

def plot_enzyme_in_time():
    font = {'family': 'Times New Roman',
            'size': 20}
    plt.rc('font', **font)
    plt.rcParams['mathtext.fontset'] = 'stix'

    fig = plt.figure(figsize=(6, 5), dpi=100)
    fig.subplots_adjust(left=0.18, top=0.91, bottom=0.15, right=0.91)
    plt.grid(which='both', linestyle='--', linewidth='0.5')

    for k in range(num_of_files):
        timesteps = data_y0[k].timestep
        for j in range(len(rin_node_y0)):
            time = []
            M_elas_inn = []
            M_elas_out = []
            M_MMP_inn = []
            M_MMP_out = []
            for i in range(len(timesteps)):
                time.append((timesteps[i]-1)*10)
                list_node = data_y0[k].node[i]
                for m in range(len(list_node)):
                    node = list_node[m]
                    if node == rin_node_y0[j]:
                        M_elas_inn.append(data_y0[k].M_elas[i][m] / 0.001558)
                        M_MMP_inn.append(data_y0[k].M_MMP[i][m])
                    if node == rout_node_y0[j]:
                        M_elas_out.append(data_y0[k].M_elas[i][m] / 0.001558)
                        M_MMP_out.append(data_y0[k].M_MMP[i][m])

            plt.plot(time, M_elas_inn, color=col[j], label=r"on $r_{\mathrm{in}}$ at section "+sekcije[j],
                     linestyle="-")

            plt.plot(time, M_elas_out, color=col[j], label=r"on $r_{\mathrm{out}}$ at section "+sekcije[j],
                     linestyle="-.")


    plt.xlim(0,4300)
    plt.ylim(-0.5,12)
    plt.xlabel("Time [days]")
    plt.ylabel("Enzyme concentration")
    plt.figtext(0.1, 0.065, "$a)$")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(loc='upper left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
               handlelength=1.8, borderaxespad=0.05)
    plt.savefig(fig_name_fig2, bbox_inches='tight')
    plt.show()

# plot_enzyme_in_time()


# -------------------------------------------------------------------------------------------------------------------- #
#  RONOD file  #

if plot_ronod_node:
    # plt.figure(8, [6.0, 4.0], 200)
    plt.figure(8, [6.0, 4.0], 100)
    for k in range(num_of_files):
        timesteps = data_ronod[k].timestep
        time = []
        list_M_elastin_0 = data_ronod[k].M_e_seg0[-1]
        list_nodes = data_ronod[k].node[0]
        n = -1
        M_elastin_0 = 10^10
        for m in range(len(list_M_elastin_0)):
            if list_nodes[m] == ronod_node:
                M_elastin_0 = list_M_elastin_0[m]
                n = m
        M_elastin_s = []
        M_coll_s = []
        M_SMC_s = []
        for i in range(len(timesteps)):
            time.append((timesteps[i]-1)*10)
            M_elastin_s.append(data_ronod[k].M_e_segs[i][n] / M_elastin_0)
            M_coll_s.append(data_ronod[k].M_coll[i][n] / data_ronod[k].M_coll[0][n])
            M_SMC_s.append(data_ronod[k].M_SMC[i][n] / data_ronod[k].M_SMC[0][n])

        if ronod_node != 0:
            if legend_type == 2:
                plt.plot(time, M_elastin_s, color=col[k], label=f"Elastin, nd{ronod_node}, " + legend_v2[k], linestyle='-')
                if plot_coll_and_SMC:
                    plt.plot(time, M_coll_s, color=col[k], label=f"Collagen, nd{ronod_node}, " + legend_v2[k], linestyle='--')
                    plt.plot(time, M_SMC_s, color=col[k], label=f"SMC, nd{ronod_node}, " + legend_v2[k], linestyle=':')
                plt.vlines(7300,0,1)
                plt.hlines(0.1,0,10000)
                plt.hlines(0.2,0,10000)
            else:
                plt.plot(time, M_elastin_s, color=col[k], label=f"Elastin, nd{ronod_node}, " + legend_v1[k], linestyle='-')
                if plot_coll_and_SMC:
                    plt.plot(time, M_coll_s, color=col[k], label=f"Collagen, nd{ronod_node}, " + legend_v1[k], linestyle='--')
                    plt.plot(time, M_SMC_s, color=col[k], label=f"SMC, nd{ronod_node}, " + legend_v1[k], linestyle=':')
                plt.vlines(7300,0,1)
                plt.hlines(0.1, 0, 10000)
                plt.hlines(0.2, 0, 10000)

    # plt.xlim(0,10000)
    # plt.ylim(16,24)
    plt.title(plot_title)
    plt.xlabel("Time [days]")
    plt.ylabel("Elastin [current / initial]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    # plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.2, -0.2))
    plt.savefig(fig_name_ronod_node, bbox_inches='tight')
    plt.show()
    plt.close(8)


if plot_ronod_axial:
    plt.figure(9, [4.0, 6.0], 100)
    for k in range(num_of_files):
        for i in range(len(ronod_axial_timesteps)):
            timestep = ronod_axial_timesteps[i]
            list_theta = data_ronod[k].theta[i]
            list_z = data_ronod[k].zcoor[i]
            M_elastin_s = []
            M_coll_s = []
            M_SMC_s = []
            z = []
            for m in range(len(list_theta)):
                if list_theta[m] == 0.0:
                    M_elastin_s.append(data_ronod[k].M_e_segs[timestep-1][m] / data_ronod[k].M_e_seg0[timestep-1][m])
                    M_coll_s.append(data_ronod[k].M_coll[timestep-1][m] / data_ronod[k].M_coll[0][m])
                    M_SMC_s.append(data_ronod[k].M_coll[timestep-1][m] / data_ronod[k].M_SMC[0][m])
                    z.append(list_z[m])

            if color_type == 3:
                c = i
            elif color_type == 2:
                c = i
            else:
                c = k
            if legend_type == 2:
                plt.plot(M_elastin_s, z, color=col[c], label=f"Elastin, t{timestep}, " + legend_v2[k], linestyle='-')
                if plot_coll_and_SMC:
                    plt.plot(M_coll_s, z, color=col[c], label=f"Collagen, t{timestep}, " + legend_v2[k], linestyle='--')
                    plt.plot(M_SMC_s, z, color=col[c], label=f"SMC, t{timestep}, " + legend_v2[k], linestyle=':')
            else:
                plt.plot(M_elastin_s, z, color=col[c], label=f"Elastin, t{timestep}, " + legend_v1[k], linestyle='-')
                if plot_coll_and_SMC:
                    plt.plot(M_coll_s, z, color=col[c], label=f"Collagen, t{timestep}, " + legend_v1[k], linestyle='--')
                    plt.plot(M_SMC_s, z, color=col[c], label=f"SMC, t{timestep}, " + legend_v1[k], linestyle=':')

    # plt.xlim(0,10000)
    # plt.ylim(16,24)
    plt.title(plot_title)
    plt.xlabel("Mass [current / initial]")
    plt.ylabel("z coordinate [mm]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    # plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0, -0.1))
    plt.savefig(fig_name_ronod_axial, bbox_inches='tight')
    plt.show()
    plt.close(9)


# -------------------------------------------------------------------------------------------------------------------- #
#  MIDDLE file  #

if plot_middle_s11:
    plt.figure(10, [6.0, 4.0], 200)
    for k in range(num_of_files):
        for i in range(len(middle_timesteps)):
            x = data_middle[k].x[middle_timesteps[i]]
            ux = data_middle[k].ux[middle_timesteps[i]]
            xx = []
            for j in range(len(x)):
                xx.append(x[j] + ux[j])
            s11 = data_middle[k].S11[middle_timesteps[i]]
            if color_type == 3:
                c = i
            elif color_type == 2:
                c = i
            else:
                c = k
            if legend_type == 2:
                plt.plot(xx, s11, linestyle='-',  color=col[c], label=f"t{middle_timesteps[i]}, " + legend_v2[k])
            else:
                plt.plot(xx, s11, linestyle='-', color=col[c], label=f"t{middle_timesteps[i]}, " + legend_v1[k])

    plt.hlines(y=-0.0108, xmin=10, xmax=20, color='k', linestyle='--')
    # plt.xlim(10,26)
    # plt.ylim(-0.015,0)
    plt.title(plot_title)
    plt.xlabel("Radius [mmm]")
    plt.ylabel("Sigma_r [Mpa]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    # plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.2, -0.1))
    plt.savefig(fig_name_middle_s11, bbox_inches='tight')
    plt.show()
    plt.close(10)

if plot_middle_s22:
    plt.figure(11, [6.0, 4.0], 200)
    for k in range(num_of_files):
        for i in range(len(middle_timesteps)):
            x = data_middle[k].x[middle_timesteps[i]]
            ux = data_middle[k].ux[middle_timesteps[i]]
            xx = []
            for j in range(len(x)):
                xx.append(x[j] + ux[j])
            s22 = data_middle[k].S22[middle_timesteps[i]]
            if color_type == 3:
                c = i
            elif color_type == 2:
                c = i
            else:
                c = k
            if legend_type == 2:
                plt.plot(xx, s22, linestyle='-',  color=col[c], label=f"t{middle_timesteps[i]}, " + legend_v2[k])
            else:
                plt.plot(xx, s22, linestyle='-', color=col[c], label=f"t{middle_timesteps[i]}, " + legend_v1[k])

    # plt.xlim(10,26)
    # plt.ylim(-0.015,0)
    plt.title(plot_title)
    plt.xlabel("Radius [mmm]")
    plt.ylabel("Sigma_theta [Mpa]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    # plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.2, -0.1))
    plt.savefig(fig_name_middle_s22, bbox_inches='tight')
    plt.show()
    plt.close(11)

if plot_middle_s33:
    plt.figure(12, [6.0, 4.0], 200)
    for k in range(num_of_files):
        for i in range(len(middle_timesteps)):
            x = data_middle[k].x[middle_timesteps[i]]
            ux = data_middle[k].ux[middle_timesteps[i]]
            xx = []
            for j in range(len(x)):
                xx.append(x[j] + ux[j])
            s33 = data_middle[k].S33[middle_timesteps[i]]
            if color_type == 3:
                c = i
            elif color_type == 2:
                c = i
            else:
                c = k
            if legend_type == 2:
                plt.plot(xx, s33, linestyle='-',  color=col[c], label=f"t{middle_timesteps[i]}, " + legend_v2[k])
            else:
                plt.plot(xx, s33, linestyle='-', color=col[c], label=f"t{middle_timesteps[i]}, " + legend_v1[k])

    # plt.xlim(10,26)
    # plt.ylim(-0.015,0)
    plt.title(plot_title)
    plt.xlabel("Radius [mmm]")
    plt.ylabel("Sigma_z [Mpa]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    # plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.2, -0.1))
    plt.savefig(fig_name_middle_s33, bbox_inches='tight')
    plt.show()
    plt.close(12)

if plot_middle_p:
    plt.figure(13, [6.0, 4.0], 200)
    for k in range(num_of_files):
        for i in range(len(middle_timesteps)):
            x = data_middle[k].x[middle_timesteps[i]]
            ux = data_middle[k].ux[middle_timesteps[i]]
            xx = []
            # for j in range(num_nodes_rad,len(x)):
            for j in range(len(x)):
                xx.append(x[j] + ux[j])
            s11 = data_middle[k].S11[middle_timesteps[i]]
            s22 = data_middle[k].S22[middle_timesteps[i]]
            s33 = data_middle[k].S33[middle_timesteps[i]]
            pp = []
            # for j in range(num_nodes_rad,len(s11)):
            for j in range(len(s11)):
                pp.append((s11[j] + s22[j] + s33[j]) / 3)
            if color_type == 3:
                c = i
            elif color_type == 2:
                c = i
            else:
                c = k
            if legend_type == 2:
                plt.plot(xx, pp, linestyle='-', color=col[c], label=f"t{middle_timesteps[i]}, " + legend_v2[k])
            else:
                plt.plot(xx, pp, linestyle='-', color=col[c], label=f"t{middle_timesteps[i]}, " + legend_v1[k])

    # plt.xlim(10,26)
    # plt.ylim(-0.015,0.015)
    plt.title(plot_title)
    plt.xlabel("Radius [mmm]")
    plt.ylabel("Tr(S)/3 [Mpa]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    # plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0, -0.1))
    plt.savefig(fig_name_middle_p, bbox_inches='tight')
    plt.show()
    plt.close(13)