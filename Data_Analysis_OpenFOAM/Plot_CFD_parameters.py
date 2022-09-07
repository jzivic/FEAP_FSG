import matplotlib.pyplot as plt
import pandas as pd

font = {'family' : 'Times New Roman',
        'size'   : 20}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'

# case = "//home/josip/feap/FSG/automatizacija_38/TAWSS/casson"
# case = "//home/josip/feap/FSG/automatizacija_38/TAWSS/Newt_40_2"
case = "//home/josip/feap/FSG/automatizacija_38/TAWSS/Newt_50_4"


# simulations_times = {60:[1.2, 1.3, 2]}     # broj simulacije -> korak u simulaciji

simulations_times = {1:[2], 30:[2], 60:[2]}

simulations_times = {60:[1.25, 1.35, 1.50]}



picture_save = False
already_averaged = True

viscosity = 5e-6*1060


"""VREMENA:
    tawss=0.4 .         sim6
    r=14:               sim 34
    r = 16:             sim 57
"""

adj_left, adj_right, adj_bottom = 0.18, 0.84, 0.15
fig_x, fig_y = 6.6, 6.6



class VadenjePodataka_FOAM:
    def __init__(self, Case, god="n"):
        # foam_time = 2
        # foam_time = 1.3

        self.data_dict = {"r":[], "z":[], "TAWSS":[], "OSI":[],"ECAP":[], "shear_rate":[] }
        # self.data_dict = {"r":[], "z":[], "TAWSS":[], "OSI":[],"ECAP":[]}


        for sim_broj in simulations_times.keys():
            for foam_time in simulations_times[sim_broj]:

                self.simulation_name = Case.split("/")[-1]
                self.koo_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/koordinate"

                if already_averaged == True:
                    self.TAWSS_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/TAWSS"
                    self.OSI_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/OSI"
                    self.ECAP_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/ECAP"

                elif already_averaged == False:
                    self.TAWSS_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/TAWSS_avg"
                    self.OSI_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/OSI_avg"
                    self.ECAP_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/ECAP_avg"


                self.Koordinate_reading()
                self.TAWSS_shear_rate_reading()
                self.OSI_reading()
                self.ECAP_reading()

            self.data_DF = pd.DataFrame(self.data_dict)


            ##self.Plot_radius()
            # self.Plot_TAWSS()
            # self.Plot_OSI()
            # self.Plot_ECAP()
            # self.Plot_shear_rate()
        # self.Plot_shear_rate_Average()
        self.Plot_shear_rate_cycle()



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



    # def Plot_radius(self):
    #     fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
    #
    #     plt.clf()
    #
    #     plt.plot(self.data_DF["r"], self.data_DF["z"], label=self.simulation_name)
    #     plt.title("Radius")
    #     plt.ylabel("$z$ [mm]")
    #     plt.xlabel("$r$ [mm]")
    #     plt.xlim([7, 18])
    #     plt.ylim(40, 210)
    #     plt.text(5.5, 20, "$a)$")
    #     plt.grid(which='both', linestyle='--', linewidth='0.5')
    #     fig = plt.gcf()
    #     fig.subplots_adjust(left=adj_left)
    #     fig.subplots_adjust(bottom=adj_bottom)
    #     if picture_save == True:
    #         fig.subplots_adjust(left=adj_left)
    #         fig.subplots_adjust(bottom=adj_bottom)
    #         fig.savefig("//home/josip/feap/FSG/slike/FSG_model/radius.png", dpi=300)
    #     elif picture_save == False:
    #         plt.show()

    def Plot_TAWSS(self):
        fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
        plt.clf()

        plt.plot(self.data_DF["TAWSS"], self.data_DF["z"], label=self.simulation_name)
        plt.axvline(x=0.4, linestyle='--', color="red", label='axvline - full height')
        plt.xlim(0.35, 0.67)
        plt.ylim(40, 210)

        # plt.title("Time averaged wall shear stress")
        plt.ylabel("$z$ [mm]")
        plt.xlabel("TAWSS [Pa]")
        plt.text(0.3, 20, "$b)$")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig.subplots_adjust(left=adj_left)
        fig.subplots_adjust(bottom=adj_bottom)

        if picture_save == True:
            fig.subplots_adjust(left=adj_left, right=adj_right, bottom=adj_bottom)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/TAWSS.png", dpi=300)

        elif picture_save == False:
            plt.show()
    def Plot_OSI(self):
        fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
        plt.clf()

        plt.plot(self.data_DF["OSI"], self.data_DF["z"],  label=self.simulation_name)
        plt.xlim(0.2, 0.53)
        plt.ylim(40, 210)

        # plt.title("Oscillatory shear index ")
        plt.ylabel("$z$ [mm]")
        plt.xlabel("OSI [-]")
        plt.text(0.15, 20, "$c)$")

        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=adj_left, right=adj_right, bottom=adj_bottom)

        if picture_save == True:
            fig.subplots_adjust(left=adj_left)
            fig.subplots_adjust(bottom=adj_bottom)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/OSI.png", dpi=300)
        elif picture_save == False:
            plt.show()
    def Plot_ECAP(self):
        fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
        plt.clf()
        plt.plot(self.data_DF["ECAP"], self.data_DF["z"],  label=self.simulation_name)
        plt.ylim(0.4, 1.9)
        plt.ylim(40, 210)
        # plt.title("Endothelium cell activation potential")
        plt.ylabel("$z$ [mm]")
        plt.xlabel("ECAP [-]")
        plt.text(0.2, 20, "$d)$")

        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=adj_left, right=adj_right, bottom=adj_bottom)
        if picture_save == True:
            fig.subplots_adjust(left=adj_left)
            fig.subplots_adjust(bottom=adj_bottom)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/ECAP.png", dpi=300)
        elif picture_save == False:
            plt.show()

    def Plot_shear_rate(self):
        fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
        plt.clf()
        plt.plot(self.data_DF["shear_rate"], self.data_DF["z"],  label=self.simulation_name)
        plt.axvline(x=140, linestyle='--', color="blue", label='Casson')
        plt.axvline(x=160, linestyle='--', color="red", label='Newt')

        plt.title("MAX shear rate, 2800. day")
        plt.ylabel("$z$ [mm]")
        plt.xlabel("shear rate [1/s]")
        # plt.text(0.2, 20, "$d)$")

        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=adj_left, right=adj_right, bottom=adj_bottom)
        if picture_save == True:
            fig.subplots_adjust(left=adj_left)
            fig.subplots_adjust(bottom=adj_bottom)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/shear_rate.png", dpi=300)
        elif picture_save == False:
            plt.show()


    def Plot_shear_rate_Average(self):
        fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
        plt.clf()
        real_days = lambda sim_number: (100 + sim_number*3)*10
        n_count = 0
        for sim in simulations_times.keys():
            for moment in simulations_times[sim]:
                plt.plot(self.data_DF["shear_rate"][n_count], self.data_DF["z"][n_count], label="$s=$"+str(real_days(sim))+" days")
                n_count +=1
        plt.ylim(50,200)
        plt.xlim(50,300)

        plt.axvline(x=140, linestyle='--', color="grey")
        plt.axvline(x=160, linestyle='--', color="grey")

        plt.ylabel("$z$ [mm]")
        plt.xlabel("TASR [1/s]")

        plt.text(60, 190, "Casson")
        plt.text(142, 190, "Tr.")
        plt.text(200, 190, "Newtonian")

        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=adj_left, right=adj_right, bottom=adj_bottom)

        if picture_save == True:
            fig.subplots_adjust(left=adj_left)
            fig.subplots_adjust(bottom=adj_bottom)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/shear_rate.png", dpi=300)
        elif picture_save == False:
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(1.026, -0.0253))

            plt.show()


    def Plot_shear_rate_cycle(self):
        fig = plt.figure(figsize=(fig_x, fig_y), dpi=100)
        plt.clf()
        real_days = lambda sim_number: (100 + sim_number*3)*10
        n_count = 0
        abc = ["A", "B", "C"]
        for sim in simulations_times.keys():
            for moment in simulations_times[sim]:
                # plt.plot(self.data_DF["shear_rate"][n_count], self.data_DF["z"][n_count], label="$s=$"+str(round((moment-1),2))+"s")
                plt.plot(self.data_DF["shear_rate"][n_count], self.data_DF["z"][n_count], label=abc[n_count])
                n_count +=1

        plt.ylim(50,200)
        plt.xlim(-50,700)

        plt.axvline(x=140, linestyle='--', color="grey")
        plt.axvline(x=160, linestyle='--', color="grey")

        plt.ylabel("$z$ [mm]")
        plt.xlabel("shear rate [1/s]")

        plt.text(-20, 190, "Casson")
        plt.text(135, 190, "Tr.")
        plt.text(230, 190, "Newt")

        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=adj_left, right=adj_right, bottom=adj_bottom)

        if picture_save == True:
            fig.subplots_adjust(left=adj_left)
            fig.subplots_adjust(bottom=adj_bottom)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/shear_rate.png", dpi=300)
        elif picture_save == False:
            plt.legend(loc='lower right', framealpha=1, labelspacing=0, borderpad=0.1, handletextpad=0.2,
                       handlelength=1.8, bbox_to_anchor=(1.026, 0.795))

            plt.show()





p9 = VadenjePodataka_FOAM(case)




















