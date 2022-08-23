import matplotlib.pyplot as plt
import pandas as pd

font = {'family' : 'Times New Roman',
        'size'   : 20}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'

case = "//home/josip/feap/FSG/automatizacija_38/TAWSS/casson"
# case = "//home/josip/feap/FSG/automatizacija_36/TAWSS/tawss_le_040"

sim_broj = 57

picture_save = False
already_averaged = True




"""VREMENA:
    tawss=0.4 .         sim6
    r=14:               sim 34
    r = 16:             sim 57
"""

adj_left, adj_right, adj_bottom = 0.18, 0.84, 0.15
fig_x, fig_y = 6.6, 6.6

class VadenjePodataka:
    def __init__(self, Case, god="n"):
        foam_time = 2
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




        self.data_dict = {"r":[], "z":[], "TAWSS":[], "OSI":[],"ECAP":[] }
        self.Koordinate_reading()
        self.TAWSS_reading()
        self.OSI_reading()
        self.ECAP_reading()

        self.data_DF = pd.DataFrame(self.data_dict)


        ##self.Plot_radius()
        self.Plot_TAWSS()
        self.Plot_OSI()
        self.Plot_ECAP()



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











p9 = VadenjePodataka(case)




















