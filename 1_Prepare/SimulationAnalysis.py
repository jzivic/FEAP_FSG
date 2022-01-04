import pandas as pd
from matplotlib import pyplot as plt

vremena = [300]

all_data = pd.read_pickle("//home/josip/PycharmProjects/FEAP_FSG/podaci_analize.pickle")
simulations = ["prava_025_14", "prava_030_14", "prava_035_14", "prava_040_14" ]




def vremenska_analiza(vremena):


    for trenutak in vremena:


        for sim in all_data.index:


            inner_cont = all_data.loc[sim]["inner_contours"][trenutak]
            ILT_cont = all_data.loc[sim]["ILT_contours"][trenutak]
            outer_cont = all_data.loc[sim]["outer_contours"][trenutak]
            z = all_data.loc[sim]["z"][trenutak]

            color = next(plt.gca()._get_lines.prop_cycler)['color']

            plt.plot(z, inner_cont, c=color)
            plt.plot(z, ILT_cont, linestyle=':', c=color)



            # plt.gca().set_prop_cycle(None)

        # p1.plot(R_inn, z_inn, linestyle='-', color=col2[n], zorder=2, label=legend_ABC[n] + "- Inner cont.")


        plt.show()







vremenska_analiza(vremena)