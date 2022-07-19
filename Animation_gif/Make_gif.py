from SimulationsData import *
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.animation as ani




auto_name = "animacija_FSG"
simulation_names = [
    "Casson",
]



pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/Animation_gif/animacija.pickle"    # folder pickla
all_data = pd.read_pickle(pickle_name)
one_simulation = all_data.loc[simulation_names[0]]



font = {'family' : 'Times New Roman',
        'size'   : 25}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'



fig = plt.figure(figsize=(7, 14), dpi=100)
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(left=0.2, top = 0.95, bottom = 0.1, right=0.95) #ensuring the dates (on the x-axis) fit in the screen




calc_days = lambda i: 10*(104+i*3)


from celluloid import Camera


def animate_func_CONTOURS(i=int):

        plt.clf()
        ILT_cont = one_simulation["ILT_contours"][i]
        inner_cont = one_simulation["inner_contours"][i]
        outer_cont = one_simulation["outer_contours"][i]
        Z_cont = one_simulation["Z_contours"][i]

        TAWSS_cont = one_simulation["TAWSS_contours"][i]

        color = next(plt.gca()._get_lines.prop_cycler)['color']
        plt.title(str(calc_days(i)) + " days")
        plt.xlabel("Radius [mm]")
        plt.ylabel("Axial coordinate $z$ [mm]")
        plt.ylim([50, 200])
        plt.xlim([7, 18])
        plt.grid(which='both', linestyle='--', linewidth='1.5')

        plt.plot(ILT_cont, Z_cont, linestyle=':', color=color, label="ILT", linewidth='3')
        plt.plot(inner_cont, Z_cont, linestyle='--',color=color, label="Inner", linewidth='3')
        plt.plot(outer_cont, Z_cont,  color=color, label="Outer", linewidth='3')

        plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                   handlelength=1.8, bbox_to_anchor=(1.026, -0.0153))


animator_cont = ani.FuncAnimation(fig, animate_func_CONTOURS, interval = 100)
plt.show()
# animator_cont.save('CONTS.gif', writer='imagemagick', fps=1000)



def animate_func_TAWSS(i=int):

        plt.clf()

        Z_cont = one_simulation["Z_contours"][i]
        TAWSS_cont = one_simulation["TAWSS_contours"][i]

        color = next(plt.gca()._get_lines.prop_cycler)['color']
        plt.title(str(calc_days(i)) + " days")
        plt.xlabel("TAWSS [Pa]")
        plt.ylabel("Axial coordinate $z$ [mm]")
        plt.ylim([50, 200])
        plt.xlim([0, 1])
        plt.grid(which='both', linestyle='--', linewidth='1.5')           #0.5

        plt.plot(TAWSS_cont, Z_cont, color=color, linewidth='3')               #1
        plt.axvline(x=0.4, linestyle='--', color="red", label='axvline - full height')  #nema


# animator_TAWSS = ani.FuncAnimation(fig, animate_func_TAWSS, interval=100)
# plt.show()

# animator_TAWSS.save('TAWSS.gif', writer='imagemagick', fps=1000)























# animator.save(r'spremljno.gif')
# animation.save('animation.gif', writer='PillowWriter', fps=2)





















# color = ['red', 'green', 'blue', 'orange']
# fig = plt.figure()
# plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
# plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
# plt.ylabel('No of Deaths')
# plt.xlabel('Dates')


# def buildmebarchart(i=int):
#     plt.legend(df1.columns)
#     p = plt.plot(df1[:i].index, df1[:i].values) #note it only returns the dataset, up to the point i
#     for i in range(0,4):
#         p[i].set_color(color[i]) #set the colour of each curve
# import matplotlib.animation as ani
# animator = ani.FuncAnimation(fig, buildmebarchart, interval = 100)
# plt.show()






