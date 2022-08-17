import matplotlib.pyplot as plt
import pandas as pd





case = "//home/josip/feap/FSG/automatizacija_38/TAWSS/casson"
sim_broj = 12

picture_save = False
already_averaged = True


font = {'family' : 'Times New Roman',
        'size'   : 20}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'


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
        # self.Plot_radius()
        # self.Plot_TAWSS()
        # self.Plot_OSI()
        # self.Plot_ECAP()

        self.Plot_TAWSS_2()


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

    def Plot_radius(self):
        plt.clf()
        plt.plot(self.data_DF["r"], self.data_DF["z"], label=self.simulation_name)
        plt.title("Radius")
        plt.ylabel("$z$ [mm]")
        plt.xlabel("$r$ [mm]")
        plt.ylim([0, 220])
        # plt.xlim([8, 14])
        plt.xlim([7, 18])

        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=0.15)
        fig.subplots_adjust(bottom=0.15)
        if picture_save == True:
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/radius.png", dpi=300)
        elif picture_save == False:
            plt.show()

    def Plot_TAWSS(self):
        plt.clf()
        plt.plot(self.data_DF["z"], self.data_DF["TAWSS"], label=self.simulation_name)
        plt.ylim(0.3, 0.9)

        plt.title("Time averaged wall shear stress")
        plt.ylabel("TAWSS [Pa]")
        plt.xlabel("$z$ [mm]")
        plt.text(-40, 0.205, "$b)$")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=0.15)
        fig.subplots_adjust(bottom=0.15)
        if picture_save == True:
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/TAWSS.png", dpi=300)
        elif picture_save == False:
            plt.show()



    def Plot_OSI(self):
        plt.clf()
        plt.plot(self.data_DF["z"], self.data_DF["OSI"], label=self.simulation_name)
        plt.title("Oscillatory shear index ")
        plt.ylabel("OSI [-]")
        plt.xlabel("$z$ [mm]")
        plt.text(-40, 0, "$c)$")

        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=0.15)
        fig.subplots_adjust(bottom=0.15)

        if picture_save == True:
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/OSI.png", dpi=300)
        elif picture_save == False:
            plt.show()


    def Plot_ECAP(self):
        plt.clf()
        plt.plot(self.data_DF["z"], self.data_DF["ECAP"], label=self.simulation_name)
        plt.title("Endothelium cell activation potential")
        # plt.ylabel("ECAP [Pa$^{-1}$]")
        plt.ylabel("ECAP [-]")
        plt.xlabel("$z$ [mm]")
        plt.text(-40, -0.135, "$d)$")

        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=0.15)
        fig.subplots_adjust(bottom=0.15)
        if picture_save == True:
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/ECAP.png", dpi=300)
        elif picture_save == False:
            plt.show()



    def Plot_TAWSS_2(self):

        fig = plt.figure(figsize=(6, 8), dpi=100)
        plt.clf()

        plt.plot(self.data_DF["TAWSS"], self.data_DF["z"], label=self.simulation_name)
        plt.axvline(x=0.4, linestyle='--', color="red", label='axvline - full height')
        plt.xlim(0.35, 0.66)
        plt.ylim(40, 210)

        plt.title("Time averaged wall shear stress")
        plt.ylabel("$z$ [mm]")
        plt.xlabel("TAWSS [Pa]")
        plt.text(0.305, -50, "$b)$")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig.subplots_adjust(left=0.15)
        fig.subplots_adjust(bottom=0.15)

        if picture_save == True:
            fig.subplots_adjust(left=0.15)
            fig.subplots_adjust(bottom=0.15)
            fig.savefig("//home/josip/feap/FSG/slike/FSG_model/TAWSS.png", dpi=300)

        elif picture_save == False:
            plt.show()








p9 = VadenjePodataka(case)




















