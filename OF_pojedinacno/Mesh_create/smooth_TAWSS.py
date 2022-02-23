import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly


# file_TAWSS = "//home/josip/feap/FSG/automatizacija_18/foam_axial=2/simulacija22/2/TAWSS"


casson_nCor_2 = "//home/josip/feap/FSG/automatizacija_18/foam_axial=1_2/simulacija30"





class VadenjePodataka:
    def __init__(self, Case, oblik, god="n"):

        self.imeSim = Case.split("/")[-1]

        self.oblik = oblik

        korak = 1
        self.koo_file = Case + "/"+str(korak)+"/koordinate"
        self.TAWSS_file = Case + "/"+str(korak)+"/TAWSS"


        self.sviPodaciDict = {"r":[], "z":[],"tawss":[],   "x":[], "y":[]}
        self.CitanjeKoordinata()
        self.CitanjeTAWSS()
        self.sviPodaciDF = pd.DataFrame(self.sviPodaciDict)
        self.sviPodaciDF = self.sviPodaciDF.sort_values(by="z")


        self.Filtriranje()

        self.Plot()


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


    def Filtriranje(self):
        dobriPodaci = {"r":[], "z":[], "tawss":[]}

        for n in range(len(self.sviPodaciDict["x"])):
            if abs(self.sviPodaciDF["y"].iloc[n]) < 1e-3 and self.sviPodaciDF["x"].iloc[n] > 0:

                dobriPodaci["r"].append(self.sviPodaciDF["x"].iloc[n])
                dobriPodaci["z"].append(self.sviPodaciDF["z"].iloc[n])
                dobriPodaci["tawss"].append(self.sviPodaciDF["tawss"].iloc[n])
        dobri_podaci_df = pd.DataFrame(dobriPodaci)
        self.dobri_podaci_df = dobri_podaci_df.sort_values(by="z")


        tawss_helathy = self.dobri_podaci_df.iloc[10]["tawss"]

        for n_start in range(1, len(self.dobri_podaci_df["tawss"])):
            if self.dobri_podaci_df["tawss"][n_start]/tawss_helathy > 1.02:
                z_start = self.dobri_podaci_df["z"][n_start]
                tawss_start = self.dobri_podaci_df["tawss"][n_start]
                print(z_start, tawss_start)
                break

        for n_stop in range(len(self.dobri_podaci_df["tawss"])-10, 1, -1):
            if self.dobri_podaci_df["tawss"][n_stop]/tawss_helathy < 0.95:
                z_stop = self.dobri_podaci_df["z"][n_stop]
                tawss_stop = self.dobri_podaci_df["tawss"][n_stop]
                print(z_stop, tawss_stop)
                break

        # plt.scatter(z_stop, tawss_stop, c="red")
        # plt.scatter(z_start, tawss_start, c="red")



        d1 = self.dobri_podaci_df[self.dobri_podaci_df.index < n_start]
        d3 = self.dobri_podaci_df[self.dobri_podaci_df.index > n_stop]
        d2 = self.dobri_podaci_df[(self.dobri_podaci_df.index > n_start) & (self.dobri_podaci_df.index < n_stop)]


        a = pd.concat([d1, d2, d3])


        coefs = poly.polyfit(d2["z"], d2["tawss"], 20)  # koef polinoma
        f_fit = poly.Polynomial(coefs)  # funkcija za fitanje

        tawss_smooth = f_fit(np.array(d2["z"]))

        d2["tawss_smooth"] = tawss_smooth

        # print(tawss_smooth)



        plt.plot(d2["z"], d2["tawss_smooth"], label="smooth")
        plt.plot(self.dobri_podaci_df["z"], self.dobri_podaci_df["tawss"], label="org")




        # self.dobri_podaci_df["tawss_smooth"] = f_fit(np.array(dobriPodaci["r"]))  # fitan drugi dio



        # rList_fit = list(itertools.chain(r_1, r_2_fit, r_3))
        # self.rList = rList_fit



        # coefs = poly.polyfit(z_2, r_2, 15)  # koef polinoma
        # f_fit = poly.Polynomial(coefs)  # funkcija za fitanje
        # r_2_fit = f_fit(np.array(z_2))  # fitan drugi dio
        #
        # rList_fit = list(itertools.chain(r_1, r_2_fit, r_3))
        # self.rList = rList_fit




    def Plot(self):
        plt.grid(color='k', linestyle=':', linewidth=0.5)

        # plt.plot(self.dobri_podaci_df["z"], self.dobri_podaci_df["tawss"], label=self.imeSim)
        # plt.plot(self.dobri_podaci_df["z"], self.dobri_podaci_df["tawss_smooth"], label="smooth")
        # plt.ylim(0, 1)

        # plt.plot(self.dobri_podaci_df["z"], self.dobri_podaci_df["r"], label=self.imeSim)
        plt.legend()
        plt.show()



        # print(self.dobri_podaci_df)




case_casson_nCor_2 = VadenjePodataka(casson_nCor_2, oblik="axial")

