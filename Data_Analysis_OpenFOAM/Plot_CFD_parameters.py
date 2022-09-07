import matplotlib.pyplot as plt
import pandas as pd

font = {'family' : 'Times New Roman',
        'size'   : 20}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'

# case = "//home/josip/feap/FSG/automatizacija_38/TAWSS/casson"
case = "//home/josip/feap/FSG/automatizacija_38/TAWSS/Newt_50_4"


sim_broj = 60

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
        foam_time = 2
        foam_time = 1.3
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


        self.data_dict = {"r":[], "z":[], "TAWSS":[], "OSI":[],"ECAP":[], "shear_rate":[] }
        self.Koordinate_reading()
        self.TAWSS_reading()
        self.OSI_reading()
        self.ECAP_reading()
        self.calc_shear_rate()


        self.data_DF = pd.DataFrame(self.data_dict)


        ##self.Plot_radius()
        # self.Plot_TAWSS()
        # self.Plot_OSI()
        # self.Plot_ECAP()
        self.Plot_shear_rate()

        # print(self.data_DF)


    def Koordinate_reading(self):
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

                self.data_dict["r"].append(float(red[0])*1000)
                self.data_dict["z"].append(float(red[2])*1000)
    def TAWSS_reading(self):
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
                self.data_dict["TAWSS"].append(float(red))
    def OSI_reading(self):
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
                self.data_dict["OSI"].append(float(red))
    def ECAP_reading(self):
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
                self.data_dict["ECAP"].append(float(red))

    def calc_shear_rate(self):
        shear_rate = [i/viscosity for i in self.data_dict["TAWSS"]]
        self.data_dict["shear_rate"] = shear_rate



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



    # def dupli_graf(self, ):
    #     fig, graf_tawss = plt.subplots()
    #
    #     color = 'tab:red'
    #     graf_tawss.set_xlabel('tawss', color=color)
    #     graf_tawss.set_ylabel('z')
    #
    #     graf_tawss.plot(tawss, z, color=color)
    #     graf_tawss.tick_params(axis='x', labelcolor=color)
    #
    #     graf_radius = graf_tawss.twiny()
    #
    #     color = 'tab:blue'
    #     graf_radius.set_xlabel('radius', color=color)  # we already handled the x-label with ax1
    #     graf_radius.plot(rad, z, color=color)
    #     graf_radius.tick_params(axis='x', labelcolor=color)
    #
    #     fig.tight_layout()  # otherwise the right y-label is slightly clipped
    #     plt.show()









p9 = VadenjePodataka_FOAM(case)




















