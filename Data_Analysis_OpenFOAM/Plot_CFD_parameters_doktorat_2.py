import matplotlib.pyplot as plt
import pandas as pd

font = {'family' : 'Times New Roman',
        'size'   : 22}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'



picture_save = False
already_averaged = False

viscosity = 5e-6*1060






cases_directory = {

        # "//home/josip/foamOpen/Doktorat/TURBULENT/Newt_turb_53": {53: [10]},
        # "//home/josip/foamOpen/Doktorat/LAMINAR/Newt_5": {53: [10]},

        # "//home/josip/foamOpen/Doktorat/LAMINAR/casson": {53: [10]},
        # "//home/josip/foamOpen/Doktorat/LAMINAR/Newt_45": {53: [10]},

        # "//home/josip/foamOpen/Doktorat/LAMINAR/Newt_4":     {53: [10]},
        # "//home/josip/foamOpen/Doktorat/LAMINAR/Newt_5":     {53: [10]},
        # "//home/josip/foamOpen/Doktorat/LAMINAR/Newt_6":     {53: [10]},
        # "//home/josip/foamOpen/Doktorat/LAMINAR/BC":         {53: [10]},


        # "//home/josip/feap/FSG/automatizacija_39/from_0": {1:[4]}
        # "//home/josip/feap/FSG/automatizacija_38/TAWSS/casson": {58: [3]},   # 34, 58

        # "//home/josip/feap/FSG/automatizacija_39/tawss_turbulent_Newt_1":   {20: [7]},
        "//home/josip/feap/FSG/automatizacija_38/TAWSS/Newt_50_4":          {22: [2]}

}



name_dictionary = {
                # "Newt_turb_53":     "turbulent",
                # "Newt_5":           "laminar",

                # "casson": "Casson",

                # "Newt_4":           "$\\nu=4\mathrm{x}10^{-6}$ m$^2$/s",
                # "Newt_45":         "$\\nu=4.5\mathrm{x}10^{-6}$ m$^2$/s",
                # "Newt_5":           "$\\nu=5\mathrm{x}10^{-6}$ m$^2$/s",
                # "Newt_6":           "$\\nu=6\mathrm{x}10^{-6}$ m$^2$/s",

                # "Newt_45": "Newtonian",
                # "casson": "Casson",
                # "BC": "Bird-Carreau",

                # "casson": "",
                # "from_0": "",
                "tawss_turbulent_Newt_1": "turbulent",
                "Newt_50_4": "laminar"

}




class VadenjePodataka_FOAM_novo:

    def __init__(self, god="n"):

        self.data_dict = {"simulation_name":[], "r":[], "z":[], "TAWSS":[], "OSI":[],"ECAP":[], "shear_rate":[], }
        for simulation_case in cases_directory:                                 # case
            self.simulation_name = simulation_case.split("/")[-1]

            for sim_broj in cases_directory[simulation_case]:                   # simulacijaX
                for foam_time in cases_directory[simulation_case][sim_broj]:    # 2
                    self.koo_file = simulation_case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/koordinate"

                    if already_averaged == True:
                        self.TAWSS_file = simulation_case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/TAWSS"
                        self.OSI_file = simulation_case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/OSI"
                        self.ECAP_file = simulation_case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/ECAP"
                    elif already_averaged == False:
                        self.TAWSS_file = simulation_case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/TAWSS_avg"
                        self.OSI_file = simulation_case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/OSI_avg"
                        self.ECAP_file = simulation_case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/ECAP_avg"

                    self.Koordinate_reading()
                    self.TAWSS_shear_rate_reading()
                    self.OSI_reading()
                    self.ECAP_reading()
                    self.data_dict["simulation_name"].append(self.simulation_name)
        self.data_DF = pd.DataFrame(self.data_dict)




        real_days = lambda sim_number: (100 + sim_number * 3) * 10
        self.fig = plt.figure(figsize=(4.6, 6.2), dpi=100)
        self.fig.subplots_adjust(left=0.21, right=0.86, top=0.95, bottom=0.15)

        plt.clf()
        plt.ylim(50, 200)
        plt.ylabel("$z$ [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')


        # self.Plot_radius()
        # self.Plot_TAWSS()
        # self.Plot_OSI()
        self.Plot_ECAP()
        # self.Plot_shear_rate_Avg()

        if picture_save == False:
            plt.show()


    #     # self.Plot_shear_rate_Average()
    #     # self.Plot_shear_rate_cycle()
    #     # plt.show()
    #
    #
    #     def prosjecan_shear_rate():
    #         sim = 1
    #         sh_avg = []
    #         for z,sr in zip(self.data_DF["z"][sim], self.data_DF["shear_rate"][sim]):
    #             if z > 80 and z < 180:
    #                 sh_avg.append(sr)
    #         shear_avg = sum(sh_avg)/len(sh_avg)
    #         print(shear_avg)
    #
    #         delta, z_coord = [], []
    #         for n in range(len(self.data_DF["z"][sim])):
    #             z = self.data_DF["z"][sim]
    #             sh = self.data_DF["shear_rate"][sim]
    #
    #             if z[n] > 80 and z[n] < 180:
    #
    #
    #                 d = abs((sh[n]+sh[n-1]))/2 * (z[n]-z[n-1])
    #                 delta.append(d)
    #                 z_coord.append(z[n])
    #
    #         shear_mean = sum(delta) / (z_coord[-1] - z_coord[0])
    #         print(shear_mean)
    #
    #
    #
    #


    def Koordinate_reading(self):
        r, z = [], []
        zapKoo = False
        for red in open(self.koo_file).readlines():
            red = red.strip()
            if red == "(":
                zapKoo = True
                continue
            if red == ")":
                zapKoo = False
                continue
            if zapKoo == True:
                red = red.strip("(", ).strip(")").split()
                r.append(float(red[0])*1000)
                z.append(float(red[2])*1000)

        self.data_dict["r"].append(r)
        self.data_dict["z"].append(z)
    def TAWSS_shear_rate_reading(self):
        TAWSS, shear_rate = [], []
        write_TAWSS = False
        for red in open(self.TAWSS_file).readlines():
            red = red.strip()
            if red =="(":
                write_TAWSS = True
                continue
            if red ==")":
                write_TAWSS = False
                continue
            if write_TAWSS == True:
                TAWSS.append(float(red))
                shear_rate.append(float(red)/viscosity)
        self.data_dict["TAWSS"].append(TAWSS)
        self.data_dict["shear_rate"].append(shear_rate)
    def OSI_reading(self):
        OSI = []
        write_OSI = False
        for red in open(self.OSI_file).readlines():
            red = red.strip()
            if red =="(":
                write_OSI = True
                continue
            if red ==")":
                write_OSI = False
                continue
            if write_OSI == True:
                OSI.append(float(red))
        self.data_dict["OSI"].append(OSI)
    def ECAP_reading(self):
        ECAP = []
        write_ECAP = False
        for red in open(self.ECAP_file).readlines():
            red = red.strip()
            if red =="(":
                write_ECAP = True
                continue
            if red ==")":
                write_ECAP = False
                continue
            if write_ECAP == True:
                ECAP.append(float(red))
        self.data_dict["ECAP"].append(ECAP)



    def Plot_radius(self):
        n_count = 0
        for simulation_case in cases_directory:  # case
            for sim_broj in cases_directory[simulation_case]:                   # simulacijaX
                for foam_time in cases_directory[simulation_case][sim_broj]:    # 2
                    plt.plot(self.data_DF["r"][n_count], self.data_DF["z"][n_count])#, label="$s=$"+str(real_days(sim))+" days")
                    n_count +=1
                    print(3)

        plt.xlabel("$r$ [mm]")
        plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                   handlelength=1.8, borderaxespad=0.05)
        if picture_save == True:
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/radius.png", dpi=300)


    def Plot_TAWSS(self):
        n_count = 0
        for simulation_case in cases_directory:  # case
            for sim_broj in cases_directory[simulation_case]:                   # simulacijaX
                for foam_time in cases_directory[simulation_case][sim_broj]:    # 2
                    # plt.plot(self.data_DF["TAWSS"][n_count], self.data_DF["z"][n_count])#, label="$s=$"+str(real_days(sim))+" days")
                    plt.plot(self.data_DF["TAWSS"][n_count], self.data_DF["z"][n_count],
                             label=name_dictionary[self.data_DF["simulation_name"][n_count]])
                    n_count +=1

        plt.xlabel("TAWSS [Pa]")
        plt.figtext(0.07, 0.05, "$b)$")
        plt.axvline(x=0.4, linestyle='--', color="red")
        plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                   handlelength=1.8, borderaxespad=0.05)
        if picture_save == True:
            self.fig.savefig("//home/josip/feap/FSG/slike/FSG_model/TAWSS.png", dpi=300)


    def Plot_OSI(self):
        n_count = 0
        for simulation_case in cases_directory:  # case
            for sim_broj in cases_directory[simulation_case]:                   # simulacijaX
                for foam_time in cases_directory[simulation_case][sim_broj]:    # 2
                    plt.plot(self.data_DF["OSI"][n_count], self.data_DF["z"][n_count],
                             label=name_dictionary[self.data_DF["simulation_name"][n_count]])
                    n_count +=1

        plt.xlim(0.18, 0.53)
        plt.xlabel("OSI [-]")
        plt.figtext(0.07, 0.05, "$d)$")
        plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                   handlelength=1.8, borderaxespad=0.05)
        if picture_save == True:
            self.fig.savefig("//home/josip/feap/FSG/slike/FSG_model/OSI.png", dpi=300)

    def Plot_ECAP(self):
        n_count = 0
        for simulation_case in cases_directory:  # case
            for sim_broj in cases_directory[simulation_case]:                   # simulacijaX
                for foam_time in cases_directory[simulation_case][sim_broj]:    # 2
                    plt.plot(self.data_DF["ECAP"][n_count], self.data_DF["z"][n_count],
                             label=name_dictionary[self.data_DF["simulation_name"][n_count]])
                    n_count +=1

        # plt.xlim(0.5, 1.5)
        plt.xlabel("ECAP [-]")
        plt.figtext(0.07, 0.05, "$e)$")
        plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                   handlelength=1.8, borderaxespad=0.05)

        if picture_save == True:
            self.fig.savefig("//home/josip/feap/FSG/slike/FSG_model/ECAP.png", dpi=300)










"""            def ILT_inner_cont_2_inLine():
                print(index)
                adj_left, adj_bottom = 0.25, 0.15
                fig_x, fig_y = 5.2, 7.2

                fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)

                color = next(plt.gca()._get_lines.prop_cycler)['color']
                plt.plot(inner_cont, Z_cont, c=color, label="inner wall")
                plt.plot(ILT_cont, Z_cont, linestyle=':', c=color, label="ILT wall")

                # plt.title("ILT and inner contours")
                plt.ylabel("$z$ [mm]")
                plt.xlabel("$r$ [mm]")
                # plt.text(5, -15, "$a)$")
                plt.xlim([7, 18])
                plt.ylim(40, 210)
                plt.text(5, 20, "$b)$")
                # fig.subplots_adjust(left=adj_left, bottom=adj_bottom)
                fig.subplots_adjust(left=0.20, top=0.91, bottom=0.15, right=0.91)
                plt.grid(which='both', linestyle='--', linewidth='0.5')
                plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                           handlelength=1.8,  borderaxespad=0.05)

                # ovo zakomentirati ako želim sve odjednom plotati
                if picture_save == True:
                    fig.savefig(diagramsDir + 'ILT_inner_cont.png', dpi=300)
                elif picture_save == False:
                    plt.show()
"""





    # def Plot_shear_rate(self):
    #     fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
    #     plt.clf()
    #     plt.plot(self.data_DF["shear_rate"], self.data_DF["z"],  label=self.simulation_name)
    #     plt.axvline(x=140, linestyle='--', color="blue", label='Casson')
    #     plt.axvline(x=160, linestyle='--', color="red", label='Newt')
    #
    #     plt.title("MAX shear rate, 2800. day")
    #     plt.ylabel("$z$ [mm]")
    #     plt.xlabel("shear rate [1/s]")
    #     # plt.text(0.2, 20, "$d)$")
    #
    #     plt.grid(which='both', linestyle='--', linewidth='0.5')
    #     fig = plt.gcf()
    #     fig.subplots_adjust(left=adj_left, right=adj_right, bottom=adj_bottom)
    #     if picture_save == True:
    #         fig.subplots_adjust(left=adj_left)
    #         fig.subplots_adjust(bottom=adj_bottom)
    #         fig.savefig("//home/josip/feap/FSG/slike/FSG_model/shear_rate.png", dpi=300)
    #     elif picture_save == False:
    #         plt.show()


    # def Plot_shear_rate_Avg(self):
    #     fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
    #     plt.clf()
    #     real_days = lambda sim_number: (100 + sim_number*3)*10
    #     n_count = 0
    #     for simulation_case in cases_directory:  # case
    #         for sim_broj in cases_directory[simulation_case]:                   # simulacijaX
    #             for foam_time in cases_directory[simulation_case][sim_broj]:    # 2
    #                 plt.plot(self.data_DF["shear_rate"][n_count], self.data_DF["z"][n_count])#, label="$s=$"+str(real_days(sim))+" days")
    #                 n_count +=1
    #     plt.ylim(50,200)
    #     plt.xlim(50,200)
    #
    #     plt.axvline(x=140, linestyle='--', color="grey")
    #     plt.axvline(x=160, linestyle='--', color="grey")
    #
    #     plt.ylabel("$z$ [mm]")
    #     plt.xlabel("TASR [1/s]")
    #
    #     plt.text(85, 190, "C")
    #     plt.text(147, 190, "T")
    #     plt.text(180, 190, "N")
    #     # plt.text(20, 30, "$a)$")
    #
    #
    #     plt.grid(which='both', linestyle='--', linewidth='0.5')
    #     fig = plt.gcf()
    #     fig.subplots_adjust(left=adj_left, right=adj_right, bottom=adj_bottom)
    #
    #     if picture_save == True:
    #         fig.subplots_adjust(left=adj_left)
    #         fig.subplots_adjust(bottom=adj_bottom)
    #         plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
    #                    handlelength=1.8, bbox_to_anchor=(1.033, -0.032))
    #         fig.savefig("//home/josip/feap/FSG/slike/FSG_model/shear_rate_Avg.png", dpi=300)
    #     elif picture_save == False:
    #         plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
    #                    handlelength=1.8, bbox_to_anchor=(-1.10, -0.04))
    #         plt.show()
    #
    #
    # def Plot_shear_rate_cycle(self):
    #     adj_left, adj_right, adj_top, adj_bottom = 0.18, 0.92, 0.91, 0.15
    #
    #     fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
    #     plt.clf()
    #     real_days = lambda sim_number: (100 + sim_number*3)*10
    #     n_count = 0
    #     abc = ["A", "B", "C"]
    #     for sim in simulations_times.keys():
    #         for moment in simulations_times[sim]:
    #             plt.plot(self.data_DF["shear_rate"][n_count], self.data_DF["z"][n_count], label="$t=$"+str(round((moment-1),2))+"s")
    #             n_count +=1
    #
    #     plt.ylim(50,200)
    #     plt.xlim(-50, 700)            # za TASR
    #
    #     plt.axvline(x=140, linestyle='--', color="grey")
    #     plt.axvline(x=160, linestyle='--', color="grey")
    #
    #     plt.ylabel("$z$ [mm]")
    #     plt.xlabel("Shear rate [1/s]")
    #     plt.figtext(0.24,0.86, "C" )         # bolja pozicija texta !!a
    #     plt.figtext(0.363,0.86, "T" )         # bolja pozicija texta !!a
    #     plt.figtext(0.51,0.86, "N" )         # bolja pozicija texta !!a
    #
    #     plt.text(-150, 30, "$b)$")
    #
    #     plt.grid(which='both', linestyle='--', linewidth='0.5')
    #     fig = plt.gcf()
    #     fig.subplots_adjust(left=adj_left, right=adj_right, top=adj_top, bottom=adj_bottom)
    #
    #     if picture_save == True:
    #         fig.subplots_adjust(left=adj_left)
    #         fig.subplots_adjust(bottom=adj_bottom)
    #         plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
    #                    handlelength=1.8, bbox_to_anchor=(1.03, 0.772))
    #         fig.savefig("//home/josip/feap/FSG/slike/FSG_model/shear_rate_cycle.png", dpi=300)
    #     elif picture_save == False:
    #         plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
    #                    handlelength=1.8, bbox_to_anchor=(1.033, 0.75))
    #                    # handlelength=1.8, bbox_to_anchor=(1.026, -0.026))
    #
    #         plt.show()



p9 = VadenjePodataka_FOAM_novo()




















