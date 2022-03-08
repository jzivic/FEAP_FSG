from SimulationsData import *

import pandas as pd
from matplotlib import pyplot as plt

# barcelona
# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/barcelona.pickle"
# simulation_names = ["a0=1.3","a3=10","a3=40","ab=100","ab=900","ac=1.67","ac=2.4",]
# simulation_names = ["ac=1.67", "ac=2.4",]


# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/podaci_automatizacije_13.pickle"
# simulation_names = ["Newt_5_NS","Newt_6_NS","prava_Casson_NS", "BS_NS" ]

# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_16.pickle"
# simulation_names = [
#                         # "a3=5",
#                         # "a3=40",
#                         "org",
#                         # "pa=0.06",
#                         # "pc=1",
#
#                         # "ac=1.6",  # sve ac, ad izgledaju isto kao org
#                         # "ac=2.8",
#                         # "ad=2.5",
#                         # "ad=4",
#
#                         # "a3=30",
#                         # "pa=0.08",
#                     ]


# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_17.pickle"
# simulation_names = [
#                     # "TAWSS=04_i4=130",
#
#                     # "TAWSS=04_i4=108_i8=08",
#                     # "TAWSS=04_i4=108_i8=065",
#                     # "TAWSS=04_i4=115_i8=08",
#                     "TAWSS=04_i4=115_i8=065",
#
#                     # "TAWSS=035_i4=108_i8=08",
#                     # "TAWSS=035_i4=108_i8=065",
#                     # "TAWSS=035_i4=115_i8=08",
#                     # "TAWSS=035_i4=115_i8=065",
#
#                     # "TAWSS=030_i4=108_i8=08",
#                     # "TAWSS=030_i4=108_i8=065",
#                     # "TAWSS=030_i4=115_i8=08",
#                     # "TAWSS=030_i4=115_i8=065",
#
#                     # "i4=125",
#                     # "i4=120",
#
#                     # "i4=115_",
#                     "i4=115_deb015_",
#                     "i4=115_deb01_",
#                     # "k1=0_i4=115=i8=1_",
#                     # "k1=0_i4=115_i8=08_",
# ]


#
# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_18.pickle"
# simulation_names = [
#         "foam_axial=1_2",
#         # "foam_axial=2",
#         # "foam_axial=3",
#         # "foam_axial=5",
#
#         "restart_200",
#         "restart_250",
#         # "tawss=055",
#
#         # "Newtn_33",
#         # "Newt_detaljno",
#
#         # "foam_axial=3_4nodes",
#         # "foam_axial=2_4nodes",
#
#         # "foam_axial=2_smooth",
#         # "rest_200_smooth",
#
#         # "no_ILT",
#         # "noILT_barcelona",
# ]

# barcelona = False
# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_19.pickle"
# simulation_names = [
#             "avg_1",
#             "avg_smooth_1",
#             "Newt33_avg",
#             "no_average",
#
#             "Newt_5_avg",
#             "Newt_5_avg_smooth",
# ]


# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_20.pickle"
# simulation_names = [
#     "4_nodes",
#     "loop2_4nodes",
#     "loop_1",
#     "loop_2_",
#     "i4=115_loop2",
#     "i4=115_loop2_4nodes",
# ]


pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_22.pickle"
simulation_names = [
    "ax5_i4=108_i8=08",
    "ax_5_novi_avg",
    "feap_5_foam1",
    "feap_5_foam_maloSporije",
    "feap_5_foam_sporije_Josip",
    "feap_5_foam_sporije_Lana",
    "loop2",
    "loop3",
    "restart_150",
    "restart_200",
    "TAWSS_035",
]



all_data = pd.read_pickle(pickle_name)

times = [270]
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
            S22_cont = all_data.loc[simul]["S22_contours"][index]



            def ILT_inner_outer_cont():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, inner_cont, c=color, label=simul)
                plt.plot(Z_cont, ILT_cont, linestyle=':', c=color)
                # plt.plot(z, outer_cont, linestyle='--', c=color)
                plt.title(str(trenutak)+". korak")
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
                plt.title(str(trenutak)+". korak")
                plt.ylabel("Stress S22 [kPa]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.xlim([0,250])
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # stress_cont()


            def ILT_thickness_f():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, ILT_thickness_cont, c=color, label=simul)
                plt.title("Debljina ILTa: "+ str(trenutak)+ ". korak")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # ILT_thickness_f()


            def vein_thickness_f():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, vein_thickness_cont, linestyle='-', c=color, label=simul)
                plt.title("Debljina stijenke: "+ str(trenutak) + ". korak")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # vein_thickness_f()

        plt.show()

# time_analysis(times)







r = 13
wanted_D = r*2

def diameter_analysis():
    for simul in simulation_names:

        nearest_diameter = min(all_data.loc[simul]["D_inner_max"], key=lambda x: abs(x-wanted_D))         # najbliža vrijednost
        index = list(all_data.loc[simul]["D_inner_max"]).index(nearest_diameter)
        time = all_data.loc[simul]["timeStep"][index]
        # print(time, simul)

        inner_cont = all_data.loc[simul]["inner_contours"][index]
        ILT_cont = all_data.loc[simul]["ILT_contours"][index]
        outer_cont = all_data.loc[simul]["outer_contours"][index]
        Z_cont = all_data.loc[simul]["Z_contours"][index]
        ILT_thickness_cont = all_data.loc[simul]["ILT_thickness_contours"][index]
        vein_thickness = all_data.loc[simul]["vein_thickness_contours"][index]
        S22_cont = all_data.loc[simul]["S22_contours"][index]


        def ILT_inner_outer_cont():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, inner_cont, c=color, label=(simul+", TS: "+str(time)))
            plt.plot(Z_cont, ILT_cont, linestyle=':', c=color)
            # plt.plot(Z_cont, outer_cont, linestyle='--', c=color)
            plt.title("Konture")
            plt.ylabel("Radius [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.xlim([0, 250])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        ILT_inner_outer_cont()


        def stress_cont():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, S22_cont, c=color, label=(simul+", TS: "+str(time)))
            # plt.title(str(trenutak) + ". korak")
            plt.ylabel("Stress S22 [kPa]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.xlim([0, 250])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # stress_cont()


        def ILT_thickness_f():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, ILT_thickness_cont, c=color, label=(simul+", TS: "+str(time)))
            plt.title("Debljina ILT-a za D="+str(wanted_D)+"mm")
            plt.ylabel("Thickness [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # ILT_thickness_f()


        def vein_thickness_f():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, vein_thickness, linestyle='-', c=color, label=(simul+", TS: "+str(time)))
            plt.title("Debljina stijenke: ")
            plt.ylabel("Thickness [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # vein_thickness_f()
    
    plt.show()

# diameter_analysis()




def growth_over_time():
    for simul in simulation_names:

        timeStep = all_data.loc[simul]["timeStep"]
        D_inner_max = all_data.loc[simul]["D_inner_max"]
        H = all_data.loc[simul]["H"]

        S22_max = all_data.loc[simul]["S22_max"]
        ILT_thickness_max = all_data.loc[simul]["ILT_thickness_max"]
        vein_thickness_max = all_data.loc[simul]["vein_thickness_max"]

        ILT_surface = all_data.loc[simul]["ILT_surface"]


        def rast_D():
            plt.plot(timeStep, D_inner_max, label=(simul))
            plt.title("Rast D inner: ")
            plt.ylabel("D [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        rast_D()


        def rast_H():
            plt.plot(timeStep, H, label=(simul))
            plt.title("Rast H: ")
            plt.ylabel("H [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_H()


        def rast_S22():
            plt.plot(timeStep, S22_max, label=(simul))
            plt.title("Rast S22: ")
            plt.ylabel("S22 [kPa]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_S22()


        def ILT_thickness():
            plt.plot(timeStep, ILT_thickness_max, label=(simul))
            plt.title("Rast ILT_thickness: ")
            plt.ylabel("ILT thickness [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # ILT_thickness()


        def ILT_surface_f():
            plt.plot(timeStep, ILT_surface, label=(simul))
            plt.title("Rast površine ILT-a: ")
            plt.ylabel("ILT surface [mm$^2$]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # ILT_surface_f()



        # Ima li ovo smisla???
        def rast_vein_thickness():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(timeStep, vein_thickness_max, label=(simul))
            plt.title("Rast vein thickness: ")
            plt.ylabel("vein thickness [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_vein_thickness()

    plt.show()

growth_over_time()






































