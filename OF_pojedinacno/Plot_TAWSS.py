import math
import os
import matplotlib.pyplot as plt
import pandas as pd
barcelona = False




# case = "//home/josip/feap/FSG/automatizacija_33/radial/radial_tawss_40_d02"
case = "//home/josip/feap/FSG/automatizacija_25/Casson"
sim_broj = 48





font = {'family' : 'Times New Roman',
        'size'   : 18}
plt.rc('font', **font)
plt.rcParams['mathtext.fontset'] = 'stix'


class VadenjePodataka:
    def __init__(self, Case, oblik, god="n"):

        self.oblik = oblik
        korak = 2
        if barcelona == True:
            korak = 3

        self.imeSim = Case.split("/")[-1]


        self.koo_file = Case + "/simulacija"+str(sim_broj)+"/"+str(korak)+"/koordinate"  # bez uprosječavanja

        self.OSI_file = Case + "/simulacija"+str(sim_broj)+"/"+str(korak)+"/OSI"
        self.ECAP_file = Case + "/simulacija"+str(sim_broj)+"/"+str(korak)+"/ECAP"



        self.TAWSS_file = Case + "/simulacija"+str(sim_broj)+"/proba"                   # s uprosječavanjem
        self.OSI_file = Case + "/simulacija"+str(sim_broj)+"/"+str(korak)+"/OSI"
        self.ECAP_file = Case + "/simulacija"+str(sim_broj)+"/"+str(korak)+"/ECAP"



        if barcelona == True:
            self.koo_file = Case + "/" + str(korak) + "/kordinate"

        self.sviPodaciDict = {"r":[], "z":[],"tawss":[],   "x":[], "y":[]}
        self.CitanjeKoordinata()
        self.CitanjeTAWSS()
        self.sviPodaciDF = pd.DataFrame(self.sviPodaciDict)
        self.sviPodaciDF = self.sviPodaciDF.sort_values(by="z")

        if self.oblik == "full":
            self.Osrednjavanje_sakularne_geometrije()
        elif self.oblik =="axial":
            self.Filtriranje()

        # self.Plot_TAWSS()
        self.Plot_radius()


    def CitanjeKoordinata(self):
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
                r = math.sqrt(float(red[0])**2 + float(red[1])**2)
                self.sviPodaciDict["r"].append(r)

                if self.oblik == "full":
                    self.sviPodaciDict["z"].append(float(red[2])+0.05342)
                elif self.oblik == "axial":
                    self.sviPodaciDict["z"].append(float(red[2])*1000)

                self.sviPodaciDict["x"].append(float(red[0])*1000)
                self.sviPodaciDict["y"].append(float(red[1])*1000)

    def CitanjeTAWSS(self):
        zapTawss = False
        for red in open(self.TAWSS_file).readlines():
            red = red.strip()
            if red =="(":
                zapTawss = True
                continue
            if red ==")":
                zapTawss = False
                continue
            if zapTawss == True:
                self.sviPodaciDict["tawss"].append(float(red))

                # if self.god == "n":
                #     self.sviPodaciDict["tawss"].append(float(red))
                # elif self.god == "s":
                #     self.sviPodaciDict["tawss"].append(float(red)*1.998)



    def CitanjeOSI(self):
        zapTawss = False
        for red in open(self.OSI_file).readlines():
            red = red.strip()
            if red =="(":
                zapTawss = True
                continue
            if red ==")":
                zapTawss = False
                continue
            if zapTawss == True:
                self.sviPodaciDict["osi"].append(float(red))











    def Osrednjavanje_sakularne_geometrije(self):
        nPodrucja = 100
        dobriPodaci = {"r":[] , "z":[], "tawss":[]}
        tocaka_u_pojasu = len(self.sviPodaciDF)//nPodrucja       # broj točaka u svakom pojasu
        pozicija, pod_R, pod_Z, pod_TAWSS = 0, [], [], []


        for n in range(len(self.sviPodaciDict["z"])):
            if n-pozicija*tocaka_u_pojasu < tocaka_u_pojasu:
                pod_R.append(self.sviPodaciDF["r"].iloc[n])
                pod_Z.append(self.sviPodaciDF["z"].iloc[n])
                pod_TAWSS.append(self.sviPodaciDF["tawss"].iloc[n])

            elif n-pozicija*tocaka_u_pojasu == tocaka_u_pojasu:
                dobriPodaci["r"].append(sum(pod_R) / len(pod_R))
                dobriPodaci["z"].append(sum(pod_Z) / len(pod_Z))
                dobriPodaci["tawss"].append(sum(pod_TAWSS) / len(pod_TAWSS))

                pozicija +=1
                pod_R, pod_Z, pod_TAWSS = [], [], []

        self.dobPodDF = pd.DataFrame(dobriPodaci)

        print(self.dobPodDF)

    def Filtriranje(self):
        dobriPodaci = {"r":[], "z":[], "tawss":[]}

        for n in range(len(self.sviPodaciDict["x"])):
            if abs(self.sviPodaciDF["y"].iloc[n]) < 1e-3 and self.sviPodaciDF["x"].iloc[n] > 0:

                dobriPodaci["r"].append(self.sviPodaciDF["x"].iloc[n])
                dobriPodaci["z"].append(self.sviPodaciDF["z"].iloc[n])
                dobriPodaci["tawss"].append(self.sviPodaciDF["tawss"].iloc[n])
        dobPodDF = pd.DataFrame(dobriPodaci)
        self.dobPodDF = dobPodDF.sort_values(by="z")


    def Plot_TAWSS(self):
        plt.plot(self.dobPodDF["z"], self.dobPodDF["tawss"], label=self.imeSim)
        plt.ylim(0.3, 0.9)

        plt.title("TAWSS when R=16 mm")
        plt.ylabel("TAWSS [Pa]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        fig = plt.gcf()
        fig.subplots_adjust(left=0.15)
        fig.subplots_adjust(bottom=0.15)
        # plt.legend()

        fig.savefig("//home/josip/feap/FSG/slike/FSG_model/TAWSS.png", dpi=300)



    def Plot_radius(self):
        plt.plot(self.dobPodDF["z"], self.dobPodDF["r"], label=self.imeSim)

        plt.title("R ")
        plt.ylabel("R [mm]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        plt.legend()
        # plt.plot(self.dobPodDF["z"], self.dobPodDF["r"], label=self.imeSim)









p9 = VadenjePodataka(case, oblik="axial")




















plt.show()
