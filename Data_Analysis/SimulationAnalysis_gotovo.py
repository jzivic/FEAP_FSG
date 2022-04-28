from SimulationsData import *

import pandas as pd
from matplotlib import pyplot as plt



pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_25.pickle"

simulation_names = {

        # "a3=30",
        # "a3=40",
        # "ac=16",
        # "ac=25",
        # "ae=1",
        # "ae=4",

        # "ab=100",
        # "ab=900",

        "tawss":
                ["tawss=020",
                "tawss=025",
                "tawss=030",
                "tawss=035",
                "tawss=040"
                # "tawss=045",
                # "tawss=050",
                ],

        "strujanje":
        [
            "BC",
            "Casson",
            "Newt_5",
            "Newt_6",
            "Newt_33",
        ],

        # "no_ILT",

        "debljina_elementa":
            [
                "debljina_010",
                "debljina_015",
                "debljina_020",
                "debljina_025",
            ]

}



# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_26.pickle"
# simulation_names = [
            # "03",
#             "04",
#             "05",
#             "07",
#             "09",
#             "12",
# ]



all_data = pd.read_pickle(pickle_name)



times = [222]
def time_analysis(times):
    for trenutak in times:
        for simul in simulation_names.values():
            print(simul)

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
                plt.title(str(trenutak)+". TS")
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




font = {'family' : 'Times New Roman',
        'size'   : 20}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'


r = 16
wanted_D = r*2

def diameter_analysis():
    plt.figure(figsize=(7, 14), dpi=100)


    for simul in simulation_names.values():
        nearest_diameter = min(all_data.loc[simul]["D_inner_max"], key=lambda x: abs(x-wanted_D))         # najbliža vrijednost
        index = list(all_data.loc[simul]["D_inner_max"]).index(nearest_diameter)
        time = all_data.loc[simul]["timeStep"][index]
        days = [i*10 in all_data.loc[simul]["timeStep"][index]]
        # print(time, simul)

        print(days)

        inner_cont = all_data.loc[simul]["inner_contours"][index]
        ILT_cont = all_data.loc[simul]["ILT_contours"][index]
        outer_cont = all_data.loc[simul]["outer_contours"][index]
        Z_cont = all_data.loc[simul]["Z_contours"][index]
        ILT_thickness_cont = all_data.loc[simul]["ILT_thickness_contours"][index]
        vein_thickness = all_data.loc[simul]["vein_thickness_contours"][index]
        S22_cont = all_data.loc[simul]["S22_contours"][index]



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

            fig = plt.gcf()
            fig.subplots_adjust(left=0.20)
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(1.026, -0.0153))

        vertical_contours()

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

    plt.show()

diameter_analysis()




def growth_over_time():
    plt.figure(figsize=(8, 6), dpi=100)


    for simul in simulation_names:

        timeStep = all_data.loc[simul]["timeStep"]
        days = [i*10 for i in all_data.loc[simul]["timeStep"]]
        D_inner_max = all_data.loc[simul]["D_inner_max"]
        H = all_data.loc[simul]["H"]

        S22_max = all_data.loc[simul]["S22_max"]
        ILT_thickness_max = all_data.loc[simul]["ILT_thickness_max"]
        vein_thickness_max = all_data.loc[simul]["vein_thickness_max"]

        ILT_surface = all_data.loc[simul]["ILT_surface"]


        def rast_D():
            plt.plot(timeStep, D_inner_max, label=(simul))
            # plt.plot(timeStep, D_inner_max, )
            plt.title("Inner diameter growth ")
            plt.ylabel("D [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_D()


        def rast_H():
            plt.plot(timeStep, H, label=(simul))
            plt.title("H growth: ")
            plt.ylabel("H [mm]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_H()


        def rast_S22():
            plt.plot(timeStep, S22_max, label=(simul))
            plt.title("S22 growth")
            plt.ylabel("S22 [kPa]")
            plt.xlabel("timeStep [-]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()
        # rast_S22()


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
            fig.subplots_adjust(left=0.13)
            fig.subplots_adjust(bottom=0.13)
            plt.legend(loc='upper left', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(-0.021, 1.028))

        ILT_surface_f()



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









