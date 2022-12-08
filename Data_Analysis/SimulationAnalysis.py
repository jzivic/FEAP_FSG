from SimulationsData import *

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.animation as ani


picture_save = False
sinonimi_u_legendi = True


sinonimi_25 = {
    # "a3_30":0,
    # "a3_40":0,
    # "ab=900":0,

    "Casson":0,
    "BC": 0,

    "Newt_5":0,
    "Newt_6":0,
    "Newt_33": "Newt,  $\\nu=3.3\mathrm{x}10^{-6}$ m$^2$/s",

    # "tawss=030":0,
    # "tawss=035":0,
    # "tawss=040":0,
    # "tawss=045":0,
    # "tawss=050":0,

}
sinonimi_36 = {

                # "tawss=030" : "staro",
                # "tawss=035" : "staro",
                # "tawss=040" : "staro",
                # "tawss=045" : "staro",
                # "tawss=050" : "staro",

                 # "tawss_le_030":0,
                 # "tawss_le_035":0,
                 "tawss_le_040": "TAWSS",
                 # "tawss_le_045":0,
                 # "tawss_le_04625":0,
                 # "tawss_le_0475":0,
                 # "tawss_le_04825":0,
                 # "tawss_le_050":0,

                 ###"osi_gt_0375":0,
                 ###"osi_gt_0400":0,
                 ###"osi_gt_0425":0,
                 ###"osi_gt_0450":0,
                 # "osi_gt_04625":0,              # najsličniji

                 # "osi_gt_04675":0,
                 # "osi_gt_04725":0,
                 # "osi_gt_0475":0,

                # "osi_gt_046250_from_0": 0,
                #  "osi_gt_04650_from_0": 0,
                #  "osi_gt_04675_from_0_2": 0,          # NOVO, VRTI SE
                 # "osi_gt_04750_from_0_2": 0,          # NOVO, VRTI SE


                 ##"osi_gt_0500":0,

                 # "osi_le_0250":     "OSI",
                 # "osi_le_0275":0,
                 # "osi_le_0300":0,
                 # "osi_le_0325":0,
                 # "osi_le_0350_2":0,


                 # "ecap_gt_145":0,
                # "ecap_gt_14625_2":0,
                # "ecap_gt_14750_2":0,
                # "ecap_gt_14825_3":0,


                 "ecap_gt_150_2":0,               # NAJSLIČNIJI tawss=0.4
                 # "ecap_gt_150_from_0":0,

                 # "ecap_gt_155":0,
                 # "ecap_gt_160":0,

                 ###"ecap_gt_14625":0,
                 ###"ecap_gt_14750": 0,
                 ###"ecap_gt_14825":0,

                # "ecap_le_080":0,
                # "ecap_le_075": 0,
                # "ecap_le_070": "ECAP",
                # "ecap_le_065":0,

}
sinonimi_37 = {

                # "tawss_le_030":0,
                # "tawss_le_035":0,
                "tawss_le_040":"TAWSS",
                # "tawss_le_045":0,
                # "tawss_le_0475":0,
                # "tawss_le_0475":0,
                # "tawss_le_04825":0,
                # "tawss_le_050":0,

                ###  "osi_f70_gt_04700":0,
                # "osi_f0_gt_04650":0,
                # "osi_f0_gt_04625":"osi",
                # "osi_f0_gt_04600":0,
                "osi_f0_gt_04575":"OSI",                    # NAJSLIČNIJI tawss=0.4
                # "osi_f0_gt_04550":0,

                # "ecap_f0_gt_150":0,
                # "ecap_f0_gt_151":0,
                # "ecap_f0_gt_152":0,
                # "ecap_f0_gt_153":0,
                "ecap_f0_gt_154": "ECAP",             # NAJSLIČNIJI tawss=0.4
                # "ecap_f0_gt_155":0,
                # "ecap_f0_gt_156":0,
                # "ecap_f0_gt_157":0,
                # "ecap_f0_gt_158":0,
                # "ecap_f0_gt_159":0,
                # "ecap_f0_gt_160":0,

}


sinonimi_38 = {
                    ###"Newt_33": "$\\nu=3.3\mathrm{x}10^{-6}$ m$^2$/s",
                    ###"Newt_45": "$\\nu=4.5\mathrm{x}10^{-6}$ m$^2$/s",


                    # "BC":"Bird-Carreau",
                    # "casson":"Casson",
                    # "Newt_40_2": "$\\nu=4\mathrm{x}10^{-6}$ m$^2$/s",
                    # "Newt_50_4":"$\\nu=5\mathrm{x}10^{-6}$ m$^2$/s",
                    # "Newt_60_4":"$\\nu=6\mathrm{x}10^{-6}$ m$^2$/s",

                    # "tawss=030":"TAWSS=0.30 Pa",
                    # "tawss=035":"TAWSS=0.35 Pa",
                    # "tawss=040":"TAWSS=0.40 Pa",
                    # "tawss=045":"TAWSS=0.45 Pa",
                    # "tawss=050": "TAWSS=0.50 Pa",

                    "casson":"$z_{\mathrm{up}}-z_{\mathrm{down}}$= 20 mm",
                    "a3=30":"$z_{\mathrm{up}}-z_{\mathrm{down}}$= 30 mm",
                    "a3=40":"$z_{\mathrm{up}}-z_{\mathrm{down}}$= 40 mm",

                    # "casson": "$\Delta z_{\mathrm{MED}}={\mathrm{20mm}}$",
                    # "a3=30": "$\Delta z_{\mathrm{MED}}={\mathrm{30mm}}$",
                    # "a3=40": "$\Delta z_{\mathrm{MED}}={\mathrm{40mm}}$",

                    # "Newt_50_4":"laminar",
                    # "tawss_turbulent_Newt_5": "turbulent",

}

sinonimi_usporedba_FSG = {
    "casson":   "FSG",
    "noFSG":    "noFSG",

}





auto_name = "automatizacija_usporedba_FSG"
sinonimi = sinonimi_usporedba_FSG


pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/" + auto_name +  ".pickle"
all_data = pd.read_pickle(pickle_name)

#            viskoznost tawss  geometrija

# diagramsDir = "//home/josip/feap/FSG/slike/"+auto_name+"/geometrija/"
diagramsDir = "//home/josip/feap/FSG/slike/FSG_model/"



def parameter_averaging(input_list):  # osrednjavanjeee!!
    n_neighb = 30
    if n_neighb % 2 == 0:
        n_neighb += 1
    average_list = list(input_list)
    start_index = int((n_neighb - 1) / 2)  # početni index da se izbjegnu rubovi
    for n in range(start_index, (len(input_list) - start_index), 1):
        neighbours = [input_list[(n - start_index) + i] for i in range(n_neighb)]
        parameter_avg = sum(neighbours) / len(neighbours)
        average_list[n] = parameter_avg
    return average_list
ts_from_sim = lambda sim: 100 + (sim-1)*3




graf_slovo="a"
# times = [ts_from_sim(6), ts_from_sim(22)]
times = [ts_from_sim(5)]
# times = [116, 251]

chosen_layer = 1

# 3 (2) u jednom redu
font = {'family': 'Times New Roman',
        'size': 25}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'


def time_analysis(times):
    fig_x, fig_y = 5.2, 7.2
    fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
    adj_left, adj_right, adj_top, adj_bottom = 0.21, 0.86, 0.95, 0.15
    fig.subplots_adjust(left=adj_left, top=adj_top, bottom=adj_bottom)
    plt.ylim(40, 210)  # turbulencija
    plt.grid(which='both', linestyle='--', linewidth='0.5')


    for trenutak in times:
        for simul in sinonimi.keys():

            if trenutak not in all_data.loc[simul].timeStep:        # Ako AAA nije nastala preskače sve
                continue

            index = all_data.loc[simul]["timeStep"].index(trenutak)
            inner_cont = all_data.loc[simul]["inner_contours"][index]
            ILT_cont = all_data.loc[simul]["ILT_contours"][index]
            outer_cont = all_data.loc[simul]["outer_contours"][index]
            Z_cont = all_data.loc[simul]["Z_contours"][index]
            ILT_thickness_cont = all_data.loc[simul]["ILT_thickness_contours"][index]
            vein_thickness_cont = all_data.loc[simul]["vein_thickness_contours"][index]
            S22_cont = all_data.loc[simul]["S22_contours"][index][:,chosen_layer]
            height_S22_is_max = all_data.loc[simul]["Z_S22_is_max"][trenutak]["height"]
            index_S22_is_max = all_data.loc[simul]["Z_S22_is_max"][trenutak]["index"]
            S22_by_layer = all_data.loc[simul]["S22_contours"][index][index_S22_is_max]
            Z_foam_cont = all_data.loc[simul]["Z_foam_cont"][index]
            TAWSS = all_data.loc[simul]["TAWSS"][index]
            OSI, ECAP = TAWSS, TAWSS


            def vertical_contours():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(inner_cont, Z_cont, c=color, label=(sinonimi[simul]))
                plt.plot(ILT_cont, Z_cont, linestyle=':', c=color, )
                plt.ylabel("$z$ [mm]")
                plt.xlabel("$r$ [mm]")
                plt.figtext(0.1,0.065, "$a)$" )         # bolja pozicija texta !!a
                # plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                #            handlelength=1.8, borderaxespad=0.05)
                if picture_save == True:
                    fig.savefig(diagramsDir + 'vertical_contours.png', dpi=300)

            def stress_by_layers():
                font = {'family': 'Times New Roman',
                        'size': 20}
                plt.rc('font', **font)
                plt.rcParams['mathtext.fontset'] = 'stix'
                fig = plt.figure(figsize=(6, 5), dpi=100)
                fig.subplots_adjust(left=0.18, top=0.91, bottom=0.15, right=0.91)
                plt.grid(which='both', linestyle='--', linewidth='0.5')

                plt.plot(range(1,8), S22_by_layer, label=(sinonimi[simul]))
                plt.xlabel("Radial layer [-]")
                plt.ylabel("${\sigma}_{22{\mathrm{max}}}$ [Pa]")
                plt.xlim([0, 8])
                plt.figtext(0.1,0.065, "$a)$" )         # bolja pozicija texta !!a
                if picture_save == True:
                    fig.savefig(diagramsDir + '/stress_through_layers_'+str(times[0]), dpi=300)

            def ILT_inner_cont():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(inner_cont, Z_cont, c=color, label="inner wall")
                plt.plot(ILT_cont, Z_cont, linestyle=':', c=color, label="ILT wall")

                plt.ylabel("$z$ [mm]")
                plt.xlabel("$r$ [mm]")
                plt.figtext(0.1,0.065, "$a)$" )         # bolja pozicija texta !!a
                plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                           handlelength=1.8, borderaxespad=0.05)
                if picture_save == True:
                    fig.savefig(diagramsDir + 'ILT_inner_cont.png', dpi=300)

            def stress_cont():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(S22_cont, Z_cont, c=color, label=(sinonimi[simul]))
                plt.ylabel("$z$ [mm]")
                plt.xlabel("${\sigma}_{22}$ [Pa]")
                plt.figtext(0.1,0.065, "$b)$" )         # bolja pozicija texta !!a

                # plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                #            handlelength=1.8, borderaxespad=0.05)
                if picture_save == True:
                    fig.savefig(diagramsDir + 'stress_cont.png', dpi=300)

            def ILT_thickness_f():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(ILT_thickness_cont, Z_cont, c=color, label=(sinonimi[simul]))
                plt.ylabel("$d_{\mathrm{ ILT}}$ [mm]")
                plt.xlabel("$z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                           handlelength=1.8, borderaxespad=0.05)
                if picture_save == True:
                    fig.savefig(diagramsDir + 'ILT_th.png', dpi=300)

            # vertical_contours()
            # ILT_thickness_f()
            # ILT_inner_cont()
            stress_cont()
            # stress_by_layers()
            3
            # def dupli_graf_TAWSS():
            #
            #     Z_cont_DG, inner_cont_DG, ILT_cont_DG  = Z_cont, inner_cont, ILT_cont
            #     Z_cont_DG.append(Z_cont_DG[-1])
            #     inner_cont_DG.append(inner_cont_DG[-1])
            #     ILT_cont_DG.append(ILT_cont_DG[-1])
            #
            #     # print(len(inner_cont_DG), inner_cont_DG)
            #     # print(len(inner_cont_DG), inner_cont_DG)
            #
            #     fig, graf_radius = plt.subplots(figsize=(5,5))
            #     color_r = 'tab:blue'
            #     graf_radius.set_xlabel('$r$ [mm]', color=color_r)  # we already handled the x-label with ax1
            #     graf_radius.set_ylabel('$z$ [mm]')
            #     graf_radius.plot(inner_cont_DG, Z_cont_DG, color=color_r, label="inner wall")
            #     graf_radius.plot(ILT_cont_DG, Z_cont_DG,linestyle=':', color=color_r, label="ILT wall")
            #
            #     graf_radius.tick_params(axis='x', labelcolor=color_r)
            #     graf_radius.set_xlim([8, 15])
            #     graf_radius.set_ylim([50, 200])
            #
            #     graf_tawss = graf_radius.twiny()
            #     color_tawss = 'tab:red'
            #     graf_tawss.set_xlabel('TAWSS [Pa]', color=color_tawss)
            #     # graf_tawss.plot(TAWSS, Z_cont_DG, color=color_tawss)
            #     graf_tawss.axvline(x=0.4, linestyle='--', color="red", label='axvline - full height')
            #     graf_tawss.tick_params(axis='x', labelcolor=color_tawss)
            #
            #     # plt.grid(which='both', linestyle='--', linewidth='0.5')
            #
            #     graf_tawss.set_xlim([0.3, 0.7])
            #     graf_tawss.set_ylim([50, 200])
            #
            #     if graf_slovo == "a":
            #         graf_radius.text(7, 15, "$a)$")
            #         plt.title("$s$ = 1000 days\n")
            #
            #     elif graf_slovo == "b":
            #         graf_radius.text(7, 15, "$b)$")
            #         plt.title("$s$ = 1120 days\n")
            #         graf_radius.axhline(y=127.5, linestyle='--', color="grey")
            #         graf_radius.axhline(y=117, linestyle='--', color="grey")
            #
            #     elif graf_slovo == "c":
            #         graf_radius.text(7, 15, "$c)$")
            #         plt.title("$s$ = 1150 days\n")
            #         graf_radius.axhline(y=127.5, linestyle='--', color="grey")
            #         graf_radius.axhline(y=116.5, linestyle='--', color="grey")
            #
            #     elif graf_slovo == "d":
            #         graf_radius.text(7, 15, "$d)$")
            #         plt.title("$s$ = 2170 days\n")
            #
            #     fig.tight_layout()
            #     # fig.subplots_adjust(left=0.2, bottom=0.22, top=0.85)
            #     fig.subplots_adjust(left=0.2, bottom=0.22, top=0.70)
            #
            #     if picture_save == True:
            #         fig.savefig(diagramsDir + 'dupli_graf_TAWSS_'+str(trenutak)+'.png', dpi=300)
            #
            #     elif picture_save == False:
            #         plt.show()
            # # dupli_graf_TAWSS()
            #
            # def dupli_graf_OSI():
            #     Z_cont_DG, inner_cont_DG, ILT_cont_DG  = Z_cont, inner_cont, ILT_cont
            #     Z_cont_DG.append(Z_cont_DG[-1])
            #     inner_cont_DG.append(inner_cont_DG[-1])
            #     ILT_cont_DG.append(ILT_cont_DG[-1])
            #
            #     fig, graf_radius = plt.subplots(figsize=(4.2,7.4))
            #     color_r = 'tab:blue'
            #     graf_radius.set_xlabel('$r$ [mm]', color=color_r)  # we already handled the x-label with ax1
            #     graf_radius.set_ylabel('$z$ [mm]')
            #     graf_radius.plot(inner_cont_DG, Z_cont_DG, color=color_r, label="inner wall")
            #     graf_radius.plot(ILT_cont_DG, Z_cont_DG,linestyle=':', color=color_r, label="ILT wall")
            #
            #     graf_radius.tick_params(axis='x', labelcolor=color_r)
            #     graf_radius.set_ylim([50, 200])
            #     # graf_radius.set_xlim([6.5, 15])
            #
            #     graf_osi = graf_radius.twiny()
            #     color_tawss = 'tab:red'
            #     graf_osi.set_xlabel('OSI [-]', color=color_tawss)
            #     graf_osi.plot(TAWSS, Z_cont_DG, color=color_tawss)
            #
            #     graf_osi.axvline(x=0.253, linestyle='--', color="red", label='axvline - full height')
            #     graf_osi.tick_params(axis='x', labelcolor=color_tawss)
            #     # plt.grid(which='both', linestyle='--', linewidth='0.5')
            #     # graf_osi.set_xlim([0.1,None])
            #     # graf_osi.set_ylim([50, 200])
            #
            #
            #     if graf_slovo == "a":
            #         graf_radius.text(9.5, 32, "$a)$")
            #         plt.title("$s$ = 1300 days\n")
            #         graf_radius.axhline(y=86, linestyle='--', color="grey")
            #         graf_radius.axhline(y=91, linestyle='--', color="grey")
            #
            #     elif graf_slovo == "b":
            #         graf_radius.text(8.5, 32, "$b)$")
            #         plt.title("$s$ = 1600 days\n")
            #
            #     elif graf_slovo == "c":
            #         graf_radius.text(3.8, 32, "$c)$")
            #         plt.title("$s$ = 2350 days\n")
            #
            #     fig.tight_layout()
            #     fig.subplots_adjust(left=0.21, bottom=0.13, top=0.80)
            #
            #     if picture_save == True:
            #         fig.savefig(diagramsDir + 'dupli_graf_OSI_'+graf_slovo+'.png', dpi=100)
            #
            #     elif picture_save == False:
            #         plt.show()
            # # dupli_graf_OSI()
            #
            # def dupli_graf_ECAP():
            #     Z_cont_DG, inner_cont_DG, ILT_cont_DG  = Z_cont, inner_cont, ILT_cont
            #     Z_cont_DG.append(Z_cont_DG[-1])
            #     inner_cont_DG.append(inner_cont_DG[-1])
            #     ILT_cont_DG.append(ILT_cont_DG[-1])
            #
            #     fig, graf_radius = plt.subplots(figsize=(4.2,7.4))
            #     color_r = 'tab:blue'
            #     graf_radius.set_xlabel('$r$ [mm]', color=color_r)  # we already handled the x-label with ax1
            #     graf_radius.set_ylabel('$z$ [mm]')
            #     graf_radius.plot(inner_cont_DG, Z_cont_DG, color=color_r, label="inner wall")
            #     graf_radius.plot(ILT_cont_DG, Z_cont_DG,linestyle=':', color=color_r, label="ILT wall")
            #
            #     graf_radius.tick_params(axis='x', labelcolor=color_r)
            #     # graf_radius.set_xlim([6.5, 15])
            #     graf_radius.set_ylim([50, 200])
            #
            #     graf_ecap = graf_radius.twiny()
            #     color_ecap = 'tab:red'
            #     graf_ecap.set_xlabel('ECAP [-]', color=color_ecap)
            #     graf_ecap.plot(ECAP, Z_cont_DG, color=color_ecap)
            #
            #     graf_ecap.axvline(x=0.715, linestyle='--', color="red", label='axvline - full height')
            #     graf_ecap.tick_params(axis='x', labelcolor=color_ecap)
            #     # plt.grid(which='both', linestyle='--', linewidth='0.5')
            #     # graf_ecap.set_xlim([0.1,None])
            #     # graf_ecap.set_ylim([50, 200])
            #
            #
            #     if graf_slovo == "a":
            #         graf_radius.text(9.5, 32, "$a)$")
            #         plt.title("$s$ = 1180 days\n")
            #         graf_radius.axhline(y=84, linestyle='--', color="grey")
            #         graf_radius.axhline(y=91, linestyle='--', color="grey")
            #
            #     elif graf_slovo == "b":
            #         graf_radius.text(8.5, 32, "$b)$")
            #         plt.title("$s$ = 1600 days\n")
            #
            #     elif graf_slovo == "c":
            #         graf_radius.text(3.8, 32, "$c)$")
            #         plt.title("$s$ = 2350 days\n")
            #
            #     # fig.tight_layout()
            #     fig.subplots_adjust(left=0.21, bottom=0.13, top=0.80)
            #
            #     if picture_save == True:
            #         fig.savefig(diagramsDir + 'dupli_graf_ecap_'+graf_slovo+'.png', dpi=100)
            #
            #     elif picture_save == False:
            #         plt.show()
            # # dupli_graf_ECAP()

    if picture_save == False:
        plt.show()

# time_analysis(times)



# fig = plt.figure(figsize=(7, 14), dpi=100)
# fig = plt.figure()
def animate_radial_stress_by_layers(i_help=int):

    # one_simulation = all_data.loc["i4=120"]
    one_simulation = all_data.loc["Casson"]
    times = range(max(one_simulation.loc["timeStep"]))

    for trenutak in times:
        if trenutak not in one_simulation.timeStep:
            continue

        index_S22_is_max = one_simulation["Z_S22_is_max"][trenutak]["index"]
        S22_by_layer = one_simulation["S22_contours"][i_help][index_S22_is_max]

    plt.clf()
    color = next(plt.gca()._get_lines.prop_cycler)['color']
    plt.title(str(i_help*10)+" day")
    plt.xlabel("Radial layer ")
    plt.ylabel("Stress [Pa]")
    plt.ylim([80, 450])
    plt.grid(which='both', linestyle='--', linewidth='0.5')

    plt.plot(range(1,8), S22_by_layer, linestyle=':', color=color, label=".", linewidth='2')

    plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
               handlelength=1.8, bbox_to_anchor=(1.026, -0.0153))
# fig = plt.figure()
# animator_cont = ani.FuncAnimation(fig, animate_radial_stress_by_layers, interval=5)
# plt.show()







radii = [16]
diameters = [ i*2 for i in radii]

assert chosen_layer in range(1,8), print("Čvor nije u rasponu 1-7 !!!")

def diameter_analysis():
    fig_x, fig_y = 5.2, 7.2
    fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
    adj_left, adj_right, adj_top, adj_bottom = 0.21, 0.86, 0.95, 0.15
    fig.subplots_adjust(left=adj_left, top=adj_top, bottom=adj_bottom)
    # plt.ylim(40, 210)  # turbulencija
    plt.ylim((30, 210))

    plt.grid(which='both', linestyle='--', linewidth='0.5')

    for r in radii:
        for simul in sinonimi.keys():

            nearest_diameter = min(all_data.loc[simul]["D_inner_max"], key=lambda x: abs(x-r*2))         # najbliža vrijednost
            index = list(all_data.loc[simul]["D_inner_max"]).index(nearest_diameter)
            time = all_data.loc[simul]["timeStep"][index]
            inner_cont = all_data.loc[simul]["inner_contours"][index]
            ILT_cont = all_data.loc[simul]["ILT_contours"][index]
            outer_cont = all_data.loc[simul]["outer_contours"][index]
            Z_cont = all_data.loc[simul]["Z_contours"][index]
            ILT_thickness_cont = all_data.loc[simul]["ILT_thickness_contours"][index]
            vein_thickness = all_data.loc[simul]["vein_thickness_contours"][index]
            S22_cont = all_data.loc[simul]["S22_contours"][index][:,chosen_layer]

            def vertical_contours():
                print(index)
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(inner_cont, Z_cont, c=color, label=(sinonimi[simul]))
                plt.plot(ILT_cont, Z_cont, linestyle=':', c=color, )
                # plt.xlim([9.5, 15.11])
                plt.xlabel("$r$ [mm]")
                plt.ylabel("$z$ [mm]")
                plt.figtext(0.1,0.065, "$b)$" )
                plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.03, handletextpad=0.1,
                           handlelength=0.8, borderaxespad=0.05)
                if picture_save == True:
                    fig.savefig(diagramsDir + 'vertical_contours_'+str(r)+'.png', dpi=400)

            def ILT_inner_cont():
                print(index)
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(inner_cont, Z_cont, c=color, label="inner wall")
                plt.plot(ILT_cont, Z_cont, linestyle=':', c=color, label="ILT wall")
                # plt.xlim([8, 17])
                plt.ylabel("$z$ [mm]")
                plt.xlabel("$r$ [mm]")
                plt.figtext(0.1,0.065, "$b)$" )
                plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                           handlelength=1.8,  borderaxespad=0.05)
                if picture_save == True:
                    fig.savefig(diagramsDir + 'ILT_inner_cont_'+str(r)+'.png', dpi=300)

            def stress_cont():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                if sinonimi_u_legendi == False:
                    plt.plot(S22_cont, Z_cont, c=color, label=(simul + ", TS: " + str(time)))
                elif sinonimi_u_legendi == True:
                    plt.plot(S22_cont, Z_cont, c=color, label=(sinonimi[simul] ))
                plt.ylabel("$z$ [mm]")
                plt.xlabel("${\sigma}_{22}$ [Pa]")
                plt.figtext(0.1,0.065, "$b)$" )
                # plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                #            handlelength=1.8,  borderaxespad=0.05)
                if picture_save == True:
                    fig.savefig(diagramsDir + 'stress_cont_'+str(r)+'.png', dpi=300)

            def ILT_thickness_f():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                # plt.plot(ILT_thickness_cont, Z_cont, c=color, label=(simul+", TS: "+str(time)))
                plt.plot(ILT_thickness_cont, Z_cont, c=color, label=(sinonimi[simul]))
                plt.ylabel("$d_{\mathrm{ ILT}}$ [mm]")
                plt.xlabel("$z$ [mm]")
                plt.figtext(0.1,0.065, "$a)$" )
                plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.03, handletextpad=0.1,
                           handlelength=0.8, borderaxespad=0.05)                # SUPER FORA!!!
                if picture_save == True:
                    fig.savefig(diagramsDir + 'ILT_thickness.png', dpi=300)

            def vein_thickness_f():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(vein_thickness, Z_cont, linestyle='-', c=color, label=(sinonimi[simul]))

                plt.ylabel("Vein thickness [mm]")
                plt.xlabel("$z$ [mm]")
                plt.figtext(0.1,0.065, "$a)$" )
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.03, handletextpad=0.1,
                           handlelength=0.8, borderaxespad=0.05)                # SUPER FORA!!!
                if picture_save == True:
                    fig.savefig(diagramsDir + 'vein_thickness_f.png', dpi=300)


            # ILT_inner_cont()
            vertical_contours()
            # stress_cont()
            # ILT_thickness_f()
            # vein_thickness_f()        #?????

    if picture_save == False:
        plt.show()

# diameter_analysis()




def growth_over_time():
    font = {'family': 'Times New Roman',
            'size': 20}
    plt.rc('font', **font)
    plt.rcParams['mathtext.fontset'] = 'stix'

    fig = plt.figure(figsize=(6, 5), dpi=100)
    fig.subplots_adjust(left=0.18, top=0.91, bottom=0.15, right=0.91)
    plt.grid(which='both', linestyle='--', linewidth='0.5')

    for simul in sinonimi.keys():
        timeStep = all_data.loc[simul]["timeStep"]
        days = [i*10 for i in all_data.loc[simul]["timeStep"]]
        D_inner_max = all_data.loc[simul]["D_inner_max"]
        H = all_data.loc[simul]["H"]
        S22_max = np.array(all_data.loc[simul]["S22_max"])[:,chosen_layer-1]
        S22_max_1 = np.array(all_data.loc[simul]["S22_max"])[:,1-1]
        S22_max_7 = np.array(all_data.loc[simul]["S22_max"])[:,7-1]
        Z_S22_is_max = [i["height"] for i in all_data.loc[simul]["Z_S22_is_max"]]


        Z_S22_is_max_averaged = parameter_averaging(Z_S22_is_max)

        S22_max_abs = [i["S22"] for i in all_data.loc[simul]["S22_Z_max_abs"]]
        Z_S22_abs_is_max = [i["height"] for i in all_data.loc[simul]["S22_Z_max_abs"]]
        Z_S22_abs_is_max_averaged = parameter_averaging(Z_S22_abs_is_max)

        ILT_thickness_max = all_data.loc[simul]["ILT_thickness_max"]
        vein_thickness_max = all_data.loc[simul]["vein_thickness_max"]
        ILT_surface = all_data.loc[simul]["ILT_surface"]
        Volume_ILT = all_data.loc[simul]["Volume_ILT"]


        def rast_D():
            plt.plot(days, D_inner_max, label=(sinonimi[simul]))
            plt.ylabel("$D_{\mathrm{max}}$ [mm]")
            plt.xlabel("$s$ [days]")
            plt.figtext(0.1,0.065, "$a)$" )         # bolja pozicija texta !!
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, borderaxespad=0.05)
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_D.png', dpi=400)

        def rast_S22_1():
            if sinonimi_u_legendi == False:
                plt.plot(days, S22_max_1, label=(simul))
            elif sinonimi_u_legendi == True:
                plt.plot(days, S22_max_1, label=(sinonimi[simul]))
            plt.ylabel("${\sigma}_{22{\mathrm{max}}}$ [Pa]")
            plt.xlabel("$s$ [days]")
            plt.figtext(0.1,0.065, "$c)$" )         # bolja pozicija texta !!
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, borderaxespad=0.05)
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_S22_1.png', dpi=400)

        def ILT_volume_f():
            plt.plot(days, Volume_ILT, label=(sinonimi[simul]))
            plt.ylabel("$V_{\mathrm{ILT}}$ [cm$^3$]")
            plt.xlabel("$s$ [days]")
            plt.figtext(0.1,0.065, "$c)$" )         # bolja pozicija texta !!
            plt.legend(loc='upper left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, borderaxespad=0.05)
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_Volume_ILT.png', dpi=400)

        def rast_H():
            plt.plot(days, H, label=(sinonimi[simul]))
            plt.ylabel("$H$ [mm]")
            plt.xlabel("$s$ [days]")
            plt.figtext(0.1,0.065, "$d)$" )         # bolja pozicija texta !!
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8,borderaxespad=0.05)
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_H.png', dpi=400)

        def rast_S22_7():
            plt.plot(days, S22_max_7, label=(sinonimi[simul]))
            # plt.ylabel("${\sigma}_{22}$ [Pa]")
            plt.ylabel("\sigma_{22}_{\mathrm{max}}}$ [mm]")
            plt.xlabel("$s$ [days]")
            plt.figtext(0.1,0.065, "$a)$" )         # bolja pozicija texta !!
            # plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
            #            handlelength=1.8, borderaxespad=0.05)
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_S22_7.png', dpi=300)

        # rast_S22_7()
        def rast_Z_max_naprezanja():
            plt.plot(days, Z_S22_is_max_averaged, label=(sinonimi[simul]))
            plt.ylabel("$H_{D_{\mathrm{max}}}$ [mm]")
            plt.xlabel("$s$ [days]")
            plt.figtext(0.1,0.065, "$a)$" )         # bolja pozicija texta !!
            plt.legend(loc='upper left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, borderaxespad=0.05)
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_Z_for_S22_max.png', dpi=300)

        def rast_Z_over_S22_abs():
            plt.plot(days, Z_S22_abs_is_max_averaged, label=(sinonimi[simul]))
            plt.ylabel("$H_{{\sigma_{22}}_{\mathrm{max}}}$ [mm]")
            plt.xlabel("$s$ [days]")
            plt.figtext(0.1,0.065, "$c)$" )         # bolja pozicija texta !!
            # plt.legend(loc='upper left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
            #            handlelength=1.8, borderaxespad=0.05)
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_H_S22_max.png', dpi=300)

        def ILT_thickness():
            plt.plot(days, ILT_thickness_max, label=(sinonimi[simul]))
            plt.ylabel("$d_{\mathrm{ ILT}}$ [mm]")
            plt.xlabel("$s$ [days]")
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, borderaxespad=0.05)
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_ILT_th.png', dpi=300)
        # ILT_thickness()

        def ILT_surface_f():
            plt.plot(days, ILT_surface, label=(sinonimi[simul]))
            plt.title("ILT surface")
            plt.ylabel("ILT surface [mm$^2$]")
            plt.xlabel("$s$ [days]")
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, borderaxespad=0.05)
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_ILT_surface_f.png', dpi=300)
        # ILT_surface_f()

        # rast_D()
        # ILT_volume_f()
        # rast_S22_1()
        # rast_H()
        rast_Z_max_naprezanja()
        # rast_Z_over_S22_abs()


    if picture_save == False:
        plt.show()

growth_over_time()


































