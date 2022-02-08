from SimulationsData import *

import pandas as pd
from matplotlib import pyplot as plt

# barcelona?
# simulation_names = ["a0=1.3","a3=10","a3=40","ab=100","ab=900","ac=1.67","ac=2.4",]


simulation_names = ["Newt_5_NS","Newt_6_NS","prava_Casson_NS",]

# simulation_names = [
#                         "a3=5",
#                         "a3=40",
#                         "org",
#                         "pa=0.06",
#                         "pc=1",
#
#                         # "ac=1.6",  # sve ac, ad izgledaju isto kao org
#                         # "ac=2.8",
#                         # "ad=2.5",
#                         # "ad=4",
#
#                         "a3=30",
#                         "pa=0.08",
#                     ]




times = [200]

all_data = pd.read_pickle(pickle_name)


# print(len(all_data.S22_contours[0]))
# print(len(all_data.inner_contours[0]))



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
            ILT_thickness = all_data.loc[simul]["ILT_thickness_contours"][index]
            vein_thickness = all_data.loc[simul]["vein_thickness_contours"][index]
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
            ILT_inner_outer_cont()


            def stress_cont():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, S22_cont, c=color, label=simul)
                plt.title(str(trenutak)+". korak")
                plt.ylabel("Stress S22 [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.xlim([0,250])
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # stress_cont()


            def vein_thickness():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, vein_thickness, linestyle='-', c=color, label=simul)
                plt.title("Debljina stijenke: "+ str(trenutak) + ". korak")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # vein_thickness()

            def ILT_thickness():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, ILT_thickness, c=color, label=simul)
                plt.title("Debljina ILTa: "+ str(trenutak)+ ". korak")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # ILT_thickness()

        plt.show()
        # plt.savefig(str(trenutak)+'.png')

# time_analysis(times)







r = 13
wanted_D = r*2

def diameter_analysis():
    for simul in simulation_names:

        nearest_diameter = min(all_data.loc[simul]["D_max"], key=lambda x: abs(x-wanted_D))         # najbliža vrijednost
        index = list(all_data.loc[simul]["D_max"]).index(nearest_diameter)
        time = all_data.loc[simul]["timeStep"][index]
        # print(time, simul)

        inner_cont = all_data.loc[simul]["inner_contours"][index]
        ILT_cont = all_data.loc[simul]["ILT_contours"][index]
        outer_cont = all_data.loc[simul]["outer_contours"][index]
        Z_cont = all_data.loc[simul]["Z_contours"][index]
        ILT_thickness = all_data.loc[simul]["ILT_thickness_contours"][index]
        vein_thickness = all_data.loc[simul]["vein_thickness_contours"][index]
        S22_cont = all_data.loc[simul]["S22_contours"][index]



        def ILT_inner_outer_cont():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, inner_cont, c=color, label=(simul+", TS: "+str(time)))
            plt.plot(Z_cont, ILT_cont, linestyle=':', c=color)
            # plt.plot(Z_cont, outer_cont, linestyle='--', c=color)
            # plt.title(str(trenutak) + ". korak")
            plt.ylabel("Radius [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            # plt.ylim([9, 18])
            plt.xlim([0, 250])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # ILT_inner_outer_cont()


        def stress_cont():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, S22_cont, c=color, label=(simul+", TS: "+str(time)))
            # plt.title(str(trenutak) + ". korak")
            plt.ylabel("Stress S22 [kPa]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.xlim([0, 250])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        stress_cont()


        def ILT_thickness_f():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, ILT_thickness, c=color, label=(simul+", TS: "+str(time)))
            plt.title("Debljina ILTa: ")
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

diameter_analysis()






def growth_over_time():
    for simul in simulation_names:

        timeStep = all_data.loc[simul]["timeStep"]
        D_max = all_data.loc[simul]["D_max"]
        H = all_data.loc[simul]["H"]

        S22_max = all_data.loc[simul]["S22_max"]
        ILT_thickness_max = all_data.loc[simul]["ILT_thickness_max"]
        vein_thickness_max = all_data.loc[simul]["vein_thickness_max"]


        def rast_D():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(timeStep, D_max, label=(simul))
            plt.plot(timeStep, D_max, label=(simul))
            plt.title("Rast D: ")
            plt.ylabel("D [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        rast_D()


        def rast_H():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(timeStep, H, label=(simul))
            plt.title("Rast H: ")
            plt.ylabel("H [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_H()


        def rast_S22():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(timeStep, S22_max, label=(simul))
            plt.title("Rast S22: ")
            plt.ylabel("S22 [kPa]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_S22()


        def ILT_thickness():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(timeStep, ILT_thickness_max, label=(simul))
            plt.title("Rast ILT_thickness: ")
            plt.ylabel("ILT thickness [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # ILT_thickness()


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

# growth_over_time()



































