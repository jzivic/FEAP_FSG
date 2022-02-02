from SimulationsData import *

import pandas as pd
from matplotlib import pyplot as plt


# all_data = pd.read_pickle("//home/josip/PycharmProjects/FEAP_FSG/podaci_analize.pickle")
# simulation_names = ["prava_025_14", "prava_030_14", "prava_035_14", "prava_040_14" ]



# simulation_names = ["prava_Newt_5",  "Newt_5_4nodes", "Newt_5_NS", "prava_Newt_6",
#                     "prava_Newt_55_n", "prava_BC_n2", "prava_BC_s2",  "prava_Casson_1"]



simulation_names = [
                    "AAA_Newt_snizena_65",
                    "AAA_Newt_snizena_75",
                    "AAA_Newt_snizena_85",
                    ]




all_data = pd.read_pickle(pickle_name)
times = [200]


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


            def plot_contours():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, inner_cont, c=color, label=simul)
                plt.plot(Z_cont, ILT_cont, linestyle=':', c=color)
                # plt.plot(z, outer_cont, linestyle='--', c=color)
                plt.title(str(trenutak)+". korak")
                plt.ylabel("Radius [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.ylim([9,18])
                plt.xlim([0,250])
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            plot_contours()


            def plot_stress():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, S22_cont, c=color, label=simul)
                plt.title(str(trenutak)+". korak")
                plt.ylabel("Stress S22 [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.xlim([0,250])
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # plot_stress()


            def debljina_stijenke():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, vein_thickness, linestyle='-', c=color, label=simul)
                plt.title("Debljina stijenke: "+ str(trenutak) + ". korak")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # debljina_stijenke()

            def debljina_ILTa():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(Z_cont, ILT_thickness, c=color, label=simul)
                plt.title("Debljina ILTa: "+ str(trenutak)+ ". korak")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # debljina_ILTa()

        plt.show()

# time_analysis(times)




r = 13.5
wanted_D = r*2

def diameter_analysis():
    for simul in simulation_names:

        nearest_diameter = min (all_data.loc[simul]["D_max"], key=lambda x: abs(x-wanted_D))         # najbliža vrijednost
        index = list(all_data.loc[simul]["D_max"]).index(nearest_diameter)
        time = all_data.loc[simul]["timeStep"][index]
        print(time, simul)

        inner_cont = all_data.loc[simul]["inner_contours"][index]
        ILT_cont = all_data.loc[simul]["ILT_contours"][index]
        outer_cont = all_data.loc[simul]["outer_contours"][index]
        Z_cont = all_data.loc[simul]["Z_contours"][index]
        ILT_thickness = all_data.loc[simul]["ILT_thickness_contours"][index]
        vein_thickness = all_data.loc[simul]["vein_thickness_contours"][index]
        S22_cont = all_data.loc[simul]["S22_contours"][index]


        def plot_contours():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, inner_cont, c=color, label=(simul+", TS: "+str(time)))
            plt.plot(Z_cont, ILT_cont, linestyle=':', c=color)
            # plt.plot(z, outer_cont, linestyle='--', c=color)
            # plt.title(str(trenutak) + ". korak")
            plt.ylabel("Radius [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            # plt.ylim([9, 18])
            plt.xlim([0, 250])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        plot_contours()


        def plot_stress():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, S22_cont, c=color, label=(simul+", TS: "+str(time)))
            # plt.title(str(trenutak) + ". korak")
            plt.ylabel("Stress S22 [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.xlim([0, 250])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # plot_stress()


        def debljina_stijenke():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, vein_thickness, linestyle='-', c=color, label=(simul+", TS: "+str(time)))
            plt.title("Debljina stijenke: ")
            plt.ylabel("Thickness [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # debljina_stijenke()
    

        def debljina_ILTa():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(Z_cont, ILT_thickness, c=color, label=(simul+", TS: "+str(time)))
            plt.title("Debljina ILTa: ")
            plt.ylabel("Thickness [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # debljina_ILTa()


    plt.show()

# diameter_analysis()


print(all_data.loc["AAA_Newt_snizena_85"])




simulation_names = [
                    "AAA_Newt_snizena_85",
                    ]


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
            plt.title("Rast D: ")
            plt.ylabel("D [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_D()


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
            plt.ylabel("S22_max [N]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        rast_S22()




        # plt.show()






growth_over_time()



































