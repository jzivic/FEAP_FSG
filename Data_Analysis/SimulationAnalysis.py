from SimulationsData import *

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.animation as ani




pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_25.pickle"
auto_name = "automatizacija_25"
simulation_names = [
            # "a3=30",
            # "a3=40",
            # "ac=16",
            # "ac=25",
            # "ae=1",
            # "ae=4",
            # "ab=100",
            # "ab=900",
            #
            # "tawss=020",
            # "tawss=025",
            # "tawss=030",
            # "tawss=035",
            # "tawss=040",
            # "tawss=045",
            # "tawss=050",
            #
            # "BC",
            # "Casson",
            # "Newt_5",
            # "Newt_6",
            # "Newt_33",
            #
            # "turb_Newt_3",
            # "turbulent_Newt_3",
            # "turbulent_Newt_5",
            # "turbulent_Newt_6",
            # "turbulent_Casson",


            # "debljina_010",
            # "debljina_015",
            # "debljina_020",
            # "debljina_025",

            # "i4=102",
            # "i4=108",
            # "i4=114",
            "i4=120",
            # "i4=126",
            # "i4=132",
            #
            # "stari_case_provjera_pocetak_2",
            # "no_ILT"
]









# diagramsDir = "//home/josip/feap/FSG/slike/auto_25/krutost/"
# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_26.pickle"
# simulation_names = [
#
#                 "stiffness_low",
#                 # "stiffness_low_01",
#                 # "stiffness_low_05",
#                 # "stiffness_low_10",
#                 # "stiffness_low_25",
#                 "stiffness_low_50",
#                 # "stiffness_low_75",
#                 "stifness_normal",
#
# ]










# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_29.pickle"
# simulation_names = [
#         "a3=30",
#         "a3=40",
#         "ac=16",
#         "ac=25",
#         "ae=1",
#         "ae=4",
#         "flow_laminar_BC",
#         "flow_laminar_Casson",
#         "flow_laminar_Newt_3",
#         "flow_laminar_Newt_5",
#         "flow_laminar_Newt_6",
#         "flow_turbulent_BC",
#         "flow_turbulent_Casson",
#         "flow_turbulent_Newt_3",
#         "flow_turbulent_Newt_5",
#         "flow_turbulent_Newt_6",
#         "tawss_025",
#         "tawss_030",
#         "tawss_035",
#         "tawss_040",
#         "tawss_045",
#         "tawss_050"
# ]


# podaci_dict = {
#                 "//home/josip/feap/FSG/automatizacija_33/radial/":
#                 ["radial_a3_30",
#                 "radial_a3_40",
#                 "radial_tawss_35_d02",
#                 "radial_tawss_40_d01",
#                 "radial_tawss_40_d02",
#                 "radial_tawss_45_d02"]
#           }

# auto_name = "automatizacija_33"
# simulation_names = [
#
#                # "radial_a3_30",
#                # "radial_a3_40",
#                # "radial_tawss_35_d02",
#                # "radial_tawss_40_d01",
#                # "radial_tawss_40_d02",
#                "radial_tawss_45_d02",
#
#                 # "3D_a3=30",
#                 # "3D_a3=40",
#                 # "3D_tawss_35_d_02",
#                 # "3D_tawss_40_d_01",
#                 # "3D_tawss_40  _d_02",
#                 "3D_tawss_45_d_02",
#
# ]


# auto_name = "auto_FSG_usporedba"
# simulation_names = [
#
#         "x3_2_a3_20",
#          # "x3_2_a3_30",
#          # "x3_2_a3_40",
#
#         "x3_3_a3_20",
#          # "x3_3_a3_30",
#          # "x3_3_a3_40",
#
#         # "a3_30",
#         #  "a3_40",
#          "Casson"
# ]


# auto_name = "automatizacija_biochemo"
# simulation_names = [
#
#             # "3D_a3_30",
#             # "3D_a3_40",
#             # "3D_tawss_35_d_02",
#             # "3D_tawss_40_d_01",
#             # "3D_tawss_40_d_02",
#             # "3D_tawss_45_d_02",
#
#             # "radial_a3_30",
#             # "radial_a3_40",
#             # "radial_tawss_35_d02",
#             # "radial_tawss_40_d01",
#             "radial_tawss_40_d02",
#             # "radial_tawss_45_d02",
#
#             # "a3_30",
#             # "a3_40",
#             # "Casson",
#
#             "standard_3D",
#
# ]


# auto_name = "automatizacija_avg_vs_NOavg"
# simulation_names = [
#                 "x3_2_a3_20_novo",
#                 "x3_2_a3_20",
# ]


chosen_layer = 1







picture_save = False
#
pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/" + auto_name +  ".pickle"
all_data = pd.read_pickle(pickle_name)
#
diagramsDir = "//home/josip/feap/FSG/slike/"+auto_name+"/prestretch/"
# diagramsDir = "//home/josip/feap/FSG/slike/proba/"


times = [230]
def time_analysis(times):
    for trenutak in times:
        for simul in simulation_names:
            # Ako AAA nije nastala preskače sve
            if trenutak not in all_data.loc[simul].timeStep:
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



            def stress_by_layers():
                # color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(range(1,8), S22_by_layer, label=simul)
                plt.title("Stress by layers")
                plt.ylabel("Stress S22 [kPa]")
                plt.xlabel("Radial layer")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()

            # stress_by_layers()




            def ILT_inner_outer_cont():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, inner_cont, c=color, label=simul)
                plt.plot(Z_cont, ILT_cont, linestyle=':', c=color)
                # plt.plot(z, outer_cont, linestyle='--', c=color)
                plt.title(str(trenutak)+". TS")
                plt.ylabel("Radius [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                # plt.ylim([9,18])
                plt.xlim([0,250])
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # ILT_inner_outer_cont()
            def stress_cont():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, S22_cont, c=color, label=simul)
                plt.title(str(trenutak)+". TS")
                plt.ylabel("Stress S22 [kPa]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.xlim([0,250])
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # stress_cont()
            def ILT_thickness_f():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, ILT_thickness_cont, c=color, label=simul)
                plt.title("ILT thickness: "+ str(trenutak)+ ". TS")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # ILT_thickness_f()
            def vein_thickness_f():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, vein_thickness_cont, linestyle='-', c=color, label=simul)
                plt.title("Vein thickness: "+ str(trenutak) + ". TS")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # vein_thickness_f()

        plt.show()

# time_analysis(times)







# fig = plt.figure(figsize=(7, 14), dpi=100)
fig = plt.figure()

def animate_radial_stress_by_layers(i_help=int):

    # one_simulation = all_data.loc["i4=120"]
    one_simulation = all_data.loc["i4=132"]
    times = range(max(one_simulation.loc["timeStep"]))

    # print(one_simulation)


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

    plt.plot(range(1,8), S22_by_layer, linestyle=':', color=color, label="ajaj", linewidth='2')

    plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
               handlelength=1.8, bbox_to_anchor=(1.026, -0.0153))


# animator_cont = ani.FuncAnimation(fig, animate_radial_stress_by_layers, interval=5)
# plt.show()



# animate_radial_stress_by_layers(2)












font = {'family' : 'Times New Roman',
        'size'   : 25}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'


r = 14
wanted_D = r*2


assert chosen_layer in range(1,8), print("Čvor nije u rasponu 1-7 !!!")
def diameter_analysis():
    plt.figure(figsize=(7, 14), dpi=100)
    fig = plt.gcf()

    for simul in simulation_names:
        nearest_diameter = min(all_data.loc[simul]["D_inner_max"], key=lambda x: abs(x-wanted_D))         # najbliža vrijednost
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
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(inner_cont, Z_cont, c=color, label=(simul))
            plt.plot(ILT_cont, Z_cont, linestyle=':', c=color, )

            plt.title("Contours")
            plt.xlabel("Radius $r$ [mm]")
            plt.ylabel("Axial coordinate $z$ [mm]")
            plt.ylim([0, 250])
            plt.xlim([7, 18])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            # plt.legend()

            fig.subplots_adjust(left=0.20)
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(1.026, -0.0153))
            if picture_save == True:
                fig.savefig(diagramsDir + 'vertical_contours.png', dpi=300)
        vertical_contours()


        def stress_cont():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            # plt.plot(Z_cont, S22_cont, c=color, label=(simul+", TS: "+str(time)))
            plt.plot(S22_cont, Z_cont, c=color, label=(simul+", TS: "+str(time)))
            # plt.title(str(trenutak) + ". korak")
            plt.xlabel("Stress S22 [kPa]")
            plt.ylabel("Axial coordinate $z$ [mm]")
            plt.ylim([0, 250])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()

            fig.subplots_adjust(left=0.20)
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(1.026, -0.0153))
            if picture_save == True:
                fig.savefig(diagramsDir + 'stress_cont.png', dpi=300)
        # stress_cont()


        def ILT_thickness_f():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, ILT_thickness_cont, c=color, label=(simul+", TS: "+str(time)))
            plt.title("ILT thickness, D="+str(wanted_D)+"mm")
            plt.ylabel("Thickness [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # ILT_thickness_f()
        def vein_thickness_f():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, vein_thickness, linestyle='-', c=color, label=(simul+", TS: "+str(time)))
            plt.title("Vein thickness: ")
            plt.ylabel("Thickness [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # vein_thickness_f()
    if picture_save == False:
        plt.show()

# diameter_analysis()




def growth_over_time():
    # plt.figure(figsize=(8, 6), dpi=100)

    for simul in simulation_names:
        timeStep = all_data.loc[simul]["timeStep"]
        days = [i*10 for i in all_data.loc[simul]["timeStep"]]
        D_inner_max = all_data.loc[simul]["D_inner_max"]
        H = all_data.loc[simul]["H"]
        S22_max = np.array(all_data.loc[simul]["S22_max"])[:,chosen_layer-1]
        Z_S22_is_max = [i["height"] for i in all_data.loc[simul]["Z_S22_is_max"]]

        ILT_thickness_max = all_data.loc[simul]["ILT_thickness_max"]
        vein_thickness_max = all_data.loc[simul]["vein_thickness_max"]
        ILT_surface = all_data.loc[simul]["ILT_surface"]



        def rast_D():
            plt.plot(days, D_inner_max, label=(simul))
            # plt.plot(timeStep, D_inner_max, )
            plt.title("Inner diameter growth ")
            plt.ylabel("D [mm]")
            plt.xlabel("Days [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            fig = plt.gcf()
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            plt.legend(loc='upper left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(-0.021, 1.028))
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_D.png', dpi=300)
        # rast_D()


        def rast_H():
            plt.plot(days, H, label=(simul))
            plt.title("H growth: ")
            plt.ylabel("H [mm]")
            plt.xlabel("Days [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            fig = plt.gcf()
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            plt.legend()
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_H.png', dpi=300)
        # rast_H()


        def rast_S22():
            plt.plot(days, S22_max, label=(simul))
            plt.title("S22 growth,  " + str(chosen_layer) + ". layer")
            plt.ylabel("S22 [kPa]")
            plt.xlabel("Days [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            fig = plt.gcf()
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            plt.legend(loc='upper left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(-0.021, 1.028))
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_S22.png', dpi=300)
        # rast_S22()


        def rast_Z_max_naprezanja():
            plt.plot(days, Z_S22_is_max, label=(simul))
            plt.title("Rast pozicije maksimalnog S22 max ")
            plt.ylabel("Z for S22 max [mm]")
            plt.xlabel("Days [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            fig = plt.gcf()
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            plt.legend(loc='upper left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(-0.021, 1.028))
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_Z_for_S22_max.png', dpi=300)
        rast_Z_max_naprezanja()



        def ILT_thickness():
            plt.plot(timeStep, ILT_thickness_max, label=(simul))
            plt.title("Max ILT thickness ")
            plt.ylabel("ILT thickness [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            # plt.legend()
        # ILT_thickness()


        def ILT_surface_f():
            plt.plot(days, ILT_surface, label=(simul))
            plt.title("ILT surface")
            plt.ylabel("ILT surface [mm$^2$]")
            plt.xlabel("Days [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            # plt.legend()
            fig = plt.gcf()
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            plt.legend(loc='upper left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(-0.021, 1.028))
            if picture_save == True:
                fig.savefig(diagramsDir + 'rast_ILT_surface_f.png', dpi=300)

        # ILT_surface_f()



        # Ima li ovo smisla???
        def rast_vein_thickness():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(timeStep, vein_thickness_max, label=(simul))
            plt.title("Vein thickness growth")
            plt.ylabel("Vein thickness [mm]")
            plt.xlabel("Time Step [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_vein_thickness()

    if picture_save == False:
        plt.show()

# growth_over_time()




























########################################33

"""
staro

        def vertical_contours():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            # plt.plot(Z_cont, inner_cont, c=color, label="inner cont")
            # plt.plot(Z_cont, ILT_cont, linestyle=':', c=color, label="ILT cont")
            # plt.plot(Z_cont, outer_cont, linestyle='--', c=color, label="outer cont")

            # plt.plot(inner_cont, Z_cont, c=color, label="inner cont")
            plt.plot(inner_cont, Z_cont, c=color, label=(simul))
            # plt.plot(inner_cont, Z_cont, c=color, label=(simul+", TS: "+str(time)))
            # plt.plot(ILT_cont, Z_cont, linestyle=':', c=color, label="ILT cont")
            plt.plot(ILT_cont, Z_cont, linestyle=':', c=color, )
            # plt.plot(outer_cont, Z_cont, linestyle='--', c=color)
            # plt.plot(outer_cont, Z_cont, linestyle='--', c=color, label="outer cont")

            fig = plt.gcf()
            fig.subplots_adjust(left=0.20)

            plt.title("Contours")
            plt.xlabel("Radius $r$ [mm]")
            plt.ylabel("Axial coordinate $z$ [mm]")
            plt.ylim([0, 250])
            plt.xlim([7, 18])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            # plt.legend()
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(1.026, -0.0153))

        vertical_contours()
"""






a = all_data.loc["i4=120"]

# print(a)

S22_max = np.array(all_data.loc["i4=120"]["S22_max"])


a = np.array(all_data.loc["i4=120"]["S22_max"])[:,]


# print(a)











