import pandas as pd
from matplotlib import pyplot as plt


all_data = pd.read_pickle("//home/josip/PycharmProjects/FEAP_FSG/podaci_analize.pickle")


times = [300]
simulation_names = ["prava_025_14", "prava_030_14", "prava_035_14", "prava_040_14" ]

# simulation_names = ["prava_025_14" ]


# print(all_data["timeStep"])
# print(all_data.loc["prava_025_14"]["timeStep"])

a = all_data.loc["prava_025_14"].D
b = all_data.loc["prava_025_14"].timeStep



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
            z = all_data.loc[simul]["z"][index]

            ILT_thickness = all_data.loc[simul]["ILT_thickness_contours"][index]
            vein_thickness = all_data.loc[simul]["vein_thickness_contours"][index]


            def crtanje_kontura():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(z, inner_cont, c=color, label=simul)
                plt.plot(z, ILT_cont, linestyle=':', c=color)
                # plt.plot(z, outer_cont, linestyle='--', c=color)
                plt.title(str(trenutak)+". korak")
                plt.ylabel("Radius [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.ylim([9,18])
                plt.xlim([0,250])
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # crtanje_kontura()

            def debljina_stijenke():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(z, vein_thickness, linestyle='-', c=color, label=simul)
                plt.title("Debljina stijenke: "+ str(trenutak) + ". korak")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # debljina_stijenke()

            def debljina_ILTa():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(z, ILT_thickness, c=color, label=simul)
                plt.title("Debljina ILTa: "+ str(trenutak)+ ". korak")
                plt.ylabel("Thickness [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()
            # debljina_ILTa()

        plt.show()

# time_analysis(times)

r = 12
wanted_D = r*2

def diameter_analysis():
    for simul in simulation_names:

        nearest_diameter = min (all_data.loc[simul]["D"], key=lambda x: abs(x-wanted_D))         # najbliža vrijednost
        index = list(all_data.loc[simul]["D"]).index(nearest_diameter)
        time = all_data.loc[simul]["timeStep"][index]
        print(time, simul)


        inner_cont = all_data.loc[simul]["inner_contours"][index]
        ILT_cont = all_data.loc[simul]["ILT_contours"][index]
        outer_cont = all_data.loc[simul]["outer_contours"][index]
        z = all_data.loc[simul]["z"][index]

        ILT_thickness = all_data.loc[simul]["ILT_thickness_contours"][index]
        vein_thickness = all_data.loc[simul]["vein_thickness_contours"][index]


        def crtanje_kontura():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(z, inner_cont, c=color, label=simul)
            plt.plot(z, ILT_cont, linestyle=':', c=color)
            # plt.plot(z, outer_cont, linestyle='--', c=color)
            # plt.title(str(trenutak) + ". korak")
            plt.ylabel("Radius [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            # plt.ylim([9, 18])
            plt.xlim([0, 250])
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()

        # crtanje_kontura()

        def debljina_stijenke():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(z, vein_thickness, linestyle='-', c=color, label=simul)
            plt.title("Debljina stijenke: ")
            plt.ylabel("Thickness [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()

        debljina_stijenke()
    
    
        def debljina_ILTa():
            color = next(plt.gca()._get_lines.prop_cycler)['color']
            plt.plot(z, ILT_thickness, c=color, label=simul)
            plt.title("Debljina ILTa: ")
            plt.ylabel("Thickness [mm]")
            plt.xlabel("Axial coordinate $z$ [mm]")
            plt.grid(which='both', linestyle='--', linewidth='0.5')
            plt.legend()

        # debljina_ILTa()





    plt.show()

diameter_analysis()






