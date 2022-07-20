import math
import os
import matplotlib.pyplot as plt
import pandas as pd





case = "//home/josip/feap/FSG/automatizacija_25/Casson"
sim_broj = 50





font = {'family' : 'Times New Roman',
        'size'   : 18}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'


class VadenjePodataka:
    def __init__(self, Case, god="n"):
        foam_time = 2
        self.simulation_name = Case.split("/")[-1]

        self.koo_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/koordinate"  # bez uprosječavanja
        self.OSI_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/OSI"
        self.ECAP_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/ECAP"

        self.TAWSS_file = Case + "/simulacija"+str(sim_broj)+"/proba"                   # s uprosječavanjem
        # self.TAWSS_file = Case + "/simulacija"+str(sim_broj)+"/"+str(foam_time)+"/TAWSS"



        self.data_dict = {"r":[], "z":[], "TAWSS":[], "OSI":[],"ECAP":[] }
        self.Koordinate_reading()
        self.TAWSS_reading()
        self.OSI_reading()
        self.ECAP_reading()

        self.data_DF = pd.DataFrame(self.data_dict)
        self.Plot_TAWSS()
        # self.Plot_OSI()
        # self.Plot_ECAP()


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



    def Plot_TAWSS(self):
        plt.plot(self.data_DF["z"], self.data_DF["TAWSS"], label=self.simulation_name)
        plt.ylim(0.3, 0.9)

        plt.title("TAWSS when R=16 mm")
        plt.ylabel("TAWSS [Pa]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=0.15)
        fig.subplots_adjust(bottom=0.15)
        plt.show()
        # fig.savefig("//home/josip/feap/FSG/slike/FSG_model/TAWSS.png", dpi=300)



    def Plot_OSI(self):
        plt.plot(self.data_DF["z"], self.data_DF["OSI"], label=self.simulation_name)
        plt.title("OSI ")
        plt.ylabel("OSI [-]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=0.15)
        fig.subplots_adjust(bottom=0.15)
        plt.show()
        # fig.savefig("//home/josip/feap/FSG/slike/FSG_model/TAWSS.png", dpi=300)

    def Plot_ECAP(self):
        plt.plot(self.data_DF["z"], self.data_DF["ECAP"], label=self.simulation_name)
        plt.title("ECAP")
        plt.ylabel("ECAP [Pa]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=0.15)
        fig.subplots_adjust(bottom=0.15)
        plt.show()
        # fig.savefig("//home/josip/feap/FSG/slike/FSG_model/TAWSS.png", dpi=300)




    def Plot_radius(self):
        plt.plot(self.dobPodDF["z"], self.dobPodDF["r"], label=self.simulation_name)

        plt.title("R ")
        plt.ylabel("R [mm]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        plt.legend()
        # plt.plot(self.dobPodDF["z"], self.dobPodDF["r"], label=self.simulation_name)









p9 = VadenjePodataka(case)




















plt.show()