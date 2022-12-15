from BioChemo.user_functions.Classes_Functions import ReadNodeFile2
from BioChemo.user_functions.Classes_Functions import ReadRonodFile
from BioChemo.user_functions.Classes_Functions import ReadResY0File
from BioChemo.user_functions.Classes_Functions import ReadResY0ILTFile
from BioChemo.user_functions.Classes_Functions import ReadMiddleFile
import matplotlib.pyplot as plt


work_dir = "//home/josip/feap/FSG/automatizacija_41/biochemo_3D"




# --- Files ---
num_of_files = 1
folder =                "172-"
legend_folder =         "172-"
simulations =           ["22"]

# --- NODE file ---
plot_inner_radius =     False
plot_wall_thickness =   False
plot_stress =           False
plot_target_gr_rate =   False
rin_node =              "0841"
rout_node =             "0847"

# --- RONOD file ---
plot_ronod_node =       False                        #2 radi
plot_ronod_axial =      True                           #1 radi
ronod_nodes =            [847,1309,1491]
ronod_axial_timesteps = [250,300,350]


# --- RES_Y0 file ---
plot_res_y0_ILT =       False
plot_res_y0_radial =    False
# res_y0_z_coordinates =  [175,215,220]
res_y0_z_coordinates =  [150]
plot_res_y0_inner =     False
plot_res_y0_outer =     False
plot_res_y0_time_inn =  False
plot_res_y0_time_out =  False
rin_node_y0 =           [841,1303,1485]
rout_node_y0 =          [847,1309,1491]
# res_y0_timesteps =      [200,300,400]
res_y0_timesteps =      [150]

# --- Flags ---
plot_elas =             True
plot_MMP =              True
plot_coll_and_SMC =     True

# --- MIDDLE file ---
plot_middle_s11 =       False
plot_middle_s22 =       False
plot_middle_s33 =       False
plot_middle_p =         False
middle_timesteps =      [300]
num_nodes_rad =         847


# Plot titles
plot_title = "172 - biochemo - fuzi"

# File names for saving plots
name = "172_bio_fuzi_plot_1"

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
sekcije = ["A", "B", "C"]
linije_josip = ['-', '--', '-.']

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
fig_name_fig2 = work_dir + "/Figure_2_v1"
fig_name_fig3 = work_dir + "/Figure_3_v1"
fig_name_fig4 = work_dir + "/Figure_4_v1"
fig_name_fig5 = work_dir + "/Figure_5_v1"

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
    if plot_middle_p or plot_middle_s11 or plot_middle_s22 or plot_middle_s33:
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

# Defining figure
# plt.figure(14, [8.0, 8.0], 100)
# pa = plt.subplot2grid((12,12),(0,0),rowspan=5,colspan=5)
# pb = plt.subplot2grid((12,12),(0,7),rowspan=5,colspan=5)
# pc = plt.subplot2grid((12,12),(7,0),rowspan=5,colspan=5)
# pd = plt.subplot2grid((12,12),(7,7),rowspan=5,colspan=5)


if plot_stress:
    for i in range(num_of_files):
        x = data_node[i].time
        s11 = data_node[i].S11in
        s22 = data_node[i].S22in
        s33 = data_node[i].S33in
        s22_kpa = []
        s33_kpa = []
        for j in range(len(s22)):
            s22_kpa.append(s22[j]*1000)
            s33_kpa.append(s33[j]*1000)
        pc.plot(x, s22_kpa, color=c2, linestyle='-', label=r"$\sigma_{\theta}$")
        pc.plot(x, s33_kpa, color=c1, linestyle='-', label=r"$\sigma_{z}$")

    # pc.set_xlim(0,10000)
    # pc.set_ylim(0.07,0.21)
    pc.set_title("(c)")
    pc.set_xlabel("Time [days]")
    pc.set_ylabel("Stresses on inner node at the apex [kPa]")
    pc.grid(which='both', linestyle='--', linewidth='0.5')
    # pc.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,1.0))
    pc.legend()
    pc.spines['top'].set_visible(False)
    pc.spines['right'].set_visible(False)


if plot_stress:
    for i in range(num_of_files):
        x = data_node[i].time
        s11 = data_node[i].S11out
        s22 = data_node[i].S22out
        s33 = data_node[i].S33out
        s22_kpa = []
        s33_kpa = []
        for j in range(len(s22)):
            s22_kpa.append(s22[j]*1000)
            s33_kpa.append(s33[j]*1000)
        pd.plot(x, s22_kpa, color=c2, linestyle='-', label=r"$\sigma_{\theta}$")
        pd.plot(x, s33_kpa, color=c1, linestyle='-', label=r"$\sigma_{z}$")

    # pd.set_xlim(0,10000)
    # pd.set_ylim(0.07,0.21)
    pd.set_title("(d)")
    pd.set_xlabel("Time [days]")
    pd.set_ylabel("Stresses on outer node at the apex [kPa]")
    pd.grid(which='both', linestyle='--', linewidth='0.5')
    # pd.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,1.0))
    pd.legend()
    pd.spines['top'].set_visible(False)
    pd.spines['right'].set_visible(False)


# -------------------------------------------------------------------------------------------------------------------- #
#  RES_Y0 and RES_Y0_ILT #

# Defining figure
# plt.figure(11, [7.0, 7.0], 100)
# p1 = plt.subplot2grid((12,12),(0,0),rowspan=12,colspan=5)
# p2 = plt.subplot2grid( (12,12),(0,7),rowspan=6,colspan=6)

# p1 = plt.subplot2grid((12,12),(0,0),rowspan=12,colspan=10)    #1



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
    plt.ylabel("Enzyme concentration [g]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    # plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    plt.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,-0.1))
    plt.savefig(fig_name_res_y0_rad, bbox_inches='tight')
    plt.show()
    plt.close(5)








if 3==2:
    # plt.figure(6, [4.0, 6.0], 200)
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
                if i == 0:
                    p1.plot(M_elas_out, z_out, color=c1, linestyle='-',
                            label=r"on $r_{\mathrm{out}}$ at $\tau = 2000$ days")
                if i == 1:
                    p1.plot(M_elas_out, z_out, color=c1, linestyle='--',
                            label=r"on $r_{\mathrm{out}}$ at $\tau = 3000$ days")
                if i == 2:
                    p1.plot(M_elas_out, z_out, color=c1, linestyle='-.',
                            label=r"on $r_{\mathrm{out}}$ at $\tau = 4000$ days")

            if plot_res_y0_inner:
                if i == 0:
                    p1.plot(M_elas_inn, z_inn, color=c2, linestyle='-',
                             label=r"on $r_{\mathrm{in}}$ at $\tau = 2000$ days")
                if i == 1:
                    p1.plot(M_elas_inn, z_inn, color=c2, linestyle='--',
                            label=r"on $r_{\mathrm{in}}$ at $\tau = 3000$ days")
                if i == 2:
                    p1.plot(M_elas_inn, z_inn, color=c2, linestyle='-.',
                            label=r"on $r_{\mathrm{in}}$ at $\tau = 4000$ days")

    # p1.set_xlim(0,10000)
    p1.set_ylim(75,275)
    p1.set_title("(a)")
    p1.set_xlabel("Enzyme concentration")
    p1.set_ylabel(r"Axial coordinate $z$ [mm]")
    p1.grid(which='both', linestyle='--', linewidth='0.5')
    p1.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(2.5,0.1))
    p1.spines['top'].set_visible(False)
    p1.spines['right'].set_visible(False)
    # p1.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,-0.1))
    # p1.savefig(fig_name_res_y0_vertical, bbox_inches='tight')
    # p1.show()
    # p1.close(6)








if plot_res_y0_time_inn or plot_res_y0_time_out:
    # plt.figure(7, [6.0, 4.0], 200)
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

            if j == 0:
                p2.plot(time, M_elas_inn, color=c4, label=r"on $r_{\mathrm{in}}$ at section A", linestyle='-')
                p2.plot(time, M_elas_out, color=c3, label=r"on $r_{\mathrm{out}}$ at section A", linestyle='-')
            if j == 1:
                p2.plot(time, M_elas_inn, color=c4, label=r"on $r_{\mathrm{in}}$ at section B", linestyle='--')
                p2.plot(time, M_elas_out, color=c3, label=r"on $r_{\mathrm{out}}$ at section B", linestyle='--')
            if j == 2:
                p2.plot(time, M_elas_inn, color=c4, label=r"on $r_{\mathrm{in}}$ at section C", linestyle='-.')
                p2.plot(time, M_elas_out, color=c3, label=r"on $r_{\mathrm{out}}$ at section C", linestyle='-.')

    # p2.xlim(0,10000)
    # p2.ylim(16,24)
    p2.set_title("(b)")
    p2.set_xlabel("Time [days]")
    p2.set_ylabel("Enzyme concentration")
    p2.grid(which='both', linestyle='--', linewidth='0.5')
    # p2.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    p2.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.2, -0.2))
    p2.spines['top'].set_visible(False)
    p2.spines['right'].set_visible(False)
    # p2.savefig(fig_name_res_y0_time, bbox_inches='tight')
    # p2.show()
    # p2.close(7)

# plt.savefig(fig_name_fig2, bbox_inches='tight')
# plt.show()
# plt.close(11)










# -------------------------------------------------------------------------------------------------------------------- #
#  RONOD file  #

# Defining figure
# plt.figure(12, [7.0, 7.0], 600)
# p1 = plt.subplot2grid((12,12),(0,0),rowspan=12,colspan=5)
# p2 = plt.subplot2grid((12,12),(0,7),rowspan=6,colspan=7)

def plot_normMass_inTime():

# if plot_ronod_node:
    font = {'family': 'Times New Roman',
            'size': 20}
    plt.rc('font', **font)
    plt.rcParams['mathtext.fontset'] = 'stix'

    fig = plt.figure(figsize=(6, 5), dpi=100)
    fig.subplots_adjust(left=0.18, top=0.91, bottom=0.15, right=0.91)
    plt.grid(which='both', linestyle='--', linewidth='0.5')

    for k in range(num_of_files):
        for j in range(len(ronod_nodes)):
            ronod_node = ronod_nodes[j]
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

            plt.plot(time, M_elastin_s, color=col[j], label=r"Elastin in section " +sekcije[j],    linestyle='-')
            plt.plot(time, M_coll_s, color=col[j], label=r"Collagen in section "    +sekcije[j],   linestyle='--')
            plt.plot(time, M_SMC_s, color=col[j], label=r"SMC in section "      +sekcije[j],         linestyle=':')


            # if j == 1:
            #     p2.plot(time, M_elastin_s, color=c5, label=r"Elastin in section B", linestyle='-')
            #     p2.plot(time, M_coll_s, color=c5, label=r"Collagen in section B", linestyle='--')
            #     p2.plot(time, M_SMC_s, color=c5, label=r"SMC in section B", linestyle=':')
            # if j == 2:
            #     p2.plot(time, M_elastin_s, color=c9, label=r"Elastin in section C", linestyle='-')
            #     p2.plot(time, M_coll_s, color=c9, label=r"Collagen in section C", linestyle='--')
            #     p2.plot(time, M_SMC_s, color=c9, label=r"SMC in section C", linestyle=':')

    plt.xlim(0,4000)
    plt.ylim(0.2,1.6)
    plt.xlabel("Time [days]")
    plt.ylabel("Normalized mass")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(loc='lower left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
           handlelength=1.8, borderaxespad=0.05)

    # plt.savefig(fig_name_ronod_node, bbox_inches='tight')
    plt.show()
    # plt.close(8)

plot_normMass_inTime()




def plot_normMass_contour():

    font = {'family': 'Times New Roman',
            'size': 22}
    plt.rc('font', **font)
    plt.rcParams['mathtext.fontset'] = 'stix'
    fig = plt.figure(figsize=(5.2, 7.2), dpi=100)
    fig.subplots_adjust(left=0.21, top=0.95, right=0.86, bottom=0.15)


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
                    M_SMC_s.append(data_ronod[k].M_SMC[timestep-1][m] / data_ronod[k].M_SMC[0][m])
                    z.append(list_z[m])

            plt.plot(M_elastin_s, z, color=c1, label=r"Elastin at $\tau=$"+str(timestep*10)+"d", linestyle=linije_josip[i])
            plt.plot(M_coll_s, z, color=c3, label=r"Collagen at $\tau=$"+str(timestep*10)+"d", linestyle=linije_josip[i])
            plt.plot(M_SMC_s, z, color=c2, label=r"SMC at $\tau=$"+str(timestep*10)+"d", linestyle=linije_josip[i])

    plt.ylim(0,200)
    plt.figtext(0.05, 0.065, "$a)$")

    plt.xlabel("Normalized mass")
    plt.ylabel(r"Axial coordinate $z$ [mm]")
    plt.grid(which='both', linestyle='--', linewidth='0.5')
    plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.03, handletextpad=0.1,
               handlelength=0.8, borderaxespad=0.05)
    plt.savefig(work_dir+"normMass_contour", bbox_inches='tight')
    plt.show()


# plot_normMass_contour()


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
    # plt.savefig(fig_name_middle_s11, bbox_inches='tight')
    # plt.show()
    # plt.close(10)

if plot_middle_s22:
    # plt.figure(11, [6.0, 4.0], 200)
    for k in range(num_of_files):
        for i in range(len(middle_timesteps)):
            x = data_middle[k].x[middle_timesteps[i]]
            ux = data_middle[k].ux[middle_timesteps[i]]
            xx = []
            for j in range(len(x)):
                xx.append(x[j] + ux[j])
            s22 = data_middle[k].S22[middle_timesteps[i]]
            s22_kpa = []
            for j in range(len(s22)):
                s22_kpa.append(s22[j]*1000)
            pa.plot(xx, s22_kpa, linestyle='-', color=c9, label=f"t{middle_timesteps[i]}, " + legend_v1[k])

    # plt.set_xlim(10,26)
    # plt.set_ylim(-0.015,0)
    pa.set_title("(a)")
    pa.set_xlabel("Radius [mmm]")
    pa.set_ylabel(r"$\sigma_{\theta}$ [kPa]")
    pa.grid(which='both', linestyle='--', linewidth='0.5')
    # pa.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    pa.spines['top'].set_visible(False)
    pa.spines['right'].set_visible(False)

if plot_middle_s33:
    # plt.figure(12, [6.0, 4.0], 200)
    for k in range(num_of_files):
        for i in range(len(middle_timesteps)):
            x = data_middle[k].x[middle_timesteps[i]]
            ux = data_middle[k].ux[middle_timesteps[i]]
            xx = []
            for j in range(len(x)):
                xx.append(x[j] + ux[j])
            s33 = data_middle[k].S33[middle_timesteps[i]]
            s33_kpa = []
            for j in range(len(s33)):
                s33_kpa.append(s33[j]*1000)
            pb.plot(xx, s33_kpa, linestyle='-', color=c9, label=f"t{middle_timesteps[i]}, " + legend_v1[k])

    # pb.set_xlim(10,26)
    # pb.set_ylim(-0.015,0)
    pb.set_title("(b)")
    pb.set_xlabel("Radius [mmm]")
    pb.set_ylabel(r"$\sigma_{z}$ [kPa]")
    pb.grid(which='both', linestyle='--', linewidth='0.5')
    # pb.legend(facecolor='w', framealpha=1.0, bbox_to_anchor=(1.0,0.8))
    pb.spines['top'].set_visible(False)
    pb.spines['right'].set_visible(False)

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





# plt.savefig(fig_name_fig4, bbox_inches='tight')
# plt.show()
# plt.close(14)