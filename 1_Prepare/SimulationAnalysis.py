import pandas as pd
from matplotlib import pyplot as plt


all_data = pd.read_pickle("//home/josip/PycharmProjects/FEAP_FSG/podaci_analize.pickle")


vremena = [312]
simulation_names = ["prava_025_14", "prava_030_14", "prava_035_14", "prava_040_14" ]
# simulation_names = ["prava_025_14", "prava_040_14" ]




def vremenska_analiza(vremena):


    for trenutak in vremena:
        # for sim in all_data.index:
        for simul in simulation_names:





            def crtanje():
                inner_cont = all_data.loc[simul]["inner_contours"][trenutak]
                ILT_cont = all_data.loc[simul]["ILT_contours"][trenutak]
                outer_cont = all_data.loc[simul]["outer_contours"][trenutak]
                z = all_data.loc[simul]["z"][trenutak]


                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(z, inner_cont, c=color, label=simul)
                plt.plot(z, ILT_cont, linestyle=':', c=color)

                # plt.title("TS:", str(trenutak))

                plt.ylim([5,25])
                plt.xlim([0,250])

                plt.ylabel("Radius [mm]")
                plt.xlabel("Axial coordinate $z$ [mm]")
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend()


            try:
                crtanje()
            except IndexError:
                pass



        plt.show()







vremenska_analiza(vremena)