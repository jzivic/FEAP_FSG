import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


all_data = pd.read_pickle("//home/josip/PycharmProjects/FEAP_FSG/podaci_analize.pickle")


vremena = [200]
simulation_names = ["prava_025_14", "prava_030_14", "prava_035_14", "prava_040_14" ]


# print(all_data["timeStep"])
# print(all_data.loc["prava_025_14"]["inner_contours"])

# print(all_data.timeStep)
# print(len(all_data.loc["prava_035_14"].inner_contours))


def vremenska_analiza(vremena):

    for simul in simulation_names:
        # for sim in all_data.index:
        timeSteps = list(all_data.loc[simul].timeStep)
        # print(timeSteps)


        for n_tren in range(len(vremena)):

            uvjet = vremena[n_tren] in timeSteps

            if uvjet == False:
                continue
                


            inner_cont = all_data.loc[simul]["inner_contours"][n_tren]
            ILT_cont = all_data.loc[simul]["ILT_contours"][n_tren]
            outer_cont = all_data.loc[simul]["outer_contours"][n_tren]
            z = all_data.loc[simul]["z"][n_tren]

            ILT_thickness = all_data.loc[simul]["ILT_thickness_contours"][n_tren]
            vein_thickness = all_data.loc[simul]["vein_thickness_contours"][n_tren]




            def crtanje_kontura():
                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(z, inner_cont, c=color, label=simul)
                plt.plot(z, ILT_cont, linestyle=':', c=color)
                # plt.plot(z, outer_cont, linestyle='--', c=color)
                plt.title( str(n_tren)+". korak")
                plt.ylabel("Radius [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.ylim([5,25])
                plt.xlim([0,250])
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()

            # try:
            #     crtanje_kontura()
            # except IndexError:
            #     pass
            crtanje_kontura()
            plt.show()
        #
        #     def debljina_stijenke():
        #         color = next(plt.gca()._get_lines.prop_cycler)['color']
        #         plt.plot(z, vein_thickness, linestyle='-', c=color, label=simul)
        #         plt.title("Debljina stijenke: "+ str(n_tren)+ ". korak")
        #         plt.ylabel("Thickness [mm]")
        #         plt.xlabel("Axial coordinate $z$ [mm]")
        #         plt.grid(which='both', linestyle='--', linewidth='0.5')
        #         plt.legend()
        #
        #     # try:
        #     #     debljina_stijenke()
        #     # except IndexError:
        #     #     pass
        #
        #
        #
        #
        #     def debljina_ILTa():
        #         color = next(plt.gca()._get_lines.prop_cycler)['color']
        #         plt.plot(z, ILT_thickness, c=color, label=simul)
        #         plt.title("Debljina ILTa: "+ str(n_tren)+ ". korak")
        #         plt.ylabel("Thickness [mm]")
        #         plt.xlabel("Axial coordinate $z$ [mm]")
        #         plt.grid(which='both', linestyle='--', linewidth='0.5')
        #         plt.legend()
        #
        #     # try:
        #     #     debljina_ILTa()
        #     # except IndexError:
        #     #     pass
        #
        #
        #
        # plt.show()







vremenska_analiza(vremena)