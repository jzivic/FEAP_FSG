import math
import os
import matplotlib.pyplot as plt
import pandas as pd




# casson_nCor_2 = "//home/josip/foamOpen/cases/FSG/NOVI_axial/usporedba_Modela/Casson/casson_2"

# s1 = "//home/josip/feap/FSG/konferencijaKarsaj/rezultati/sve_simulacije/ab=900/simulacija68"
# s2 = "//home/josip/feap/FSG/automatizacija_18/foam_axial=1_2/simulacija56_mrdanje"
# s3 = "//home/josip/feap/FSG/automatizacija_18/foam_axial=1_2/simulacija56_Newt"
# s4 = "//home/josip/foamOpen/cases/problemi/simulacija61"


s5 = "//home/josip/foamOpen/cases/turbulencija/laminar_Newt"
s6 = "//home/josip/foamOpen/cases/turbulencija/turb_moje_dugacka_Newton"



# s7 = "//home/josip/foamOpen/cases/turbulencija/laminar_Casson"
# s8 = "//home/josip/foamOpen/cases/turbulencija/turb_moje_dugacka_Casson"






barcelona = False


class VadenjePodataka:
    def __init__(self, Case, oblik, god="n"):

        # self.imeSim = Case.split("/")[-2]+ " - " + Case.split("/")[-1]
        self.imeSim = Case.split("/")[-1]
        # self.imeSim = Case.split("/")[-2]

        self.oblik = oblik
        korak = 3
        if barcelona == True:
            korak = 3
        self.koo_file = Case + "/"+str(korak)+"/koordinate"
        self.TAWSS_file = Case + "/"+str(korak)+"/TAWSS"

        if barcelona == True:
            self.koo_file = Case + "/" + str(korak) + "/kordinate"

        self.sviPodaciDict = {"r":[], "z":[],"tawss":[],   "x":[], "y":[]}
        self.CitanjeKoordinata()
        self.CitanjeTAWSS()
        self.sviPodaciDF = pd.DataFrame(self.sviPodaciDict)
        self.sviPodaciDF = self.sviPodaciDF.sort_values(by="z")

        if self.oblik == "full":
            self.Osrednjavanje()
        elif self.oblik =="axial":
            self.Filtriranje()

        self.Plot_TAWSS()
        # self.Plot_radius()


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
                    self.sviPodaciDict["z"].append(float(red[2]))

                self.sviPodaciDict["x"].append(float(red[0]))
                self.sviPodaciDict["y"].append(float(red[1]))

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


    def Osrednjavanje(self):
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
        # plt.ylim(0, 1)

        plt.title("TAWSS ")
        plt.ylabel("TAWSS [Pa]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        plt.legend()



    def Plot_radius(self):
        plt.plot(self.dobPodDF["z"], self.dobPodDF["r"], label=self.imeSim)

        plt.title("R ")
        plt.ylabel("R [mm]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        plt.legend()
        # plt.plot(self.dobPodDF["z"], self.dobPodDF["r"], label=self.imeSim)







p7 = VadenjePodataka(s5, oblik="axial")
p8 = VadenjePodataka(s6, oblik="axial")




















plt.show()
