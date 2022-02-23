import math
import os
import matplotlib.pyplot as plt
import pandas as pd




s1 = "//home/josip/feap/FSG/automatizacija_18/foam_axial=1_2/simulacija16/"





class VadenjePodataka:
    def __init__(self, Case, ):

        self.imeSim = Case.split("/")[-1]

        korak = 2

        self.koo_file = Case + "/"+str(korak)+"/koordinate"
        self.TAWSS_file = Case + "/"+str(korak)+"/TAWSS"



        # self.podaci_df = {"r":[], "z":[],"tawss":[],   "x":[], "y":[]}
        self.podaci_dict = {"r":[], "z":[],"tawss":[]}



        self.citanje_koordinata()
        self.citanje_TAWSS()

        self.podaci_df = pd.DataFrame(self.podaci_dict)



        # self.plot_TAWSS()
        # self.plot_radius()





    def citanje_koordinata(self):
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
                self.podaci_dict["r"].append(r)
                self.podaci_dict["z"].append(float(red[2]))

                # self.podaci_df["x"].append(float(red[0]))
                # self.podaci_df["y"].append(float(red[1]))
                

    def citanje_TAWSS(self):
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
                self.podaci_dict["tawss"].append(float(red))


    def average_TAWSS_1(self):
        print(4)








    def plot_TAWSS(self):
        plt.plot(self.podaci_df["z"], self.podaci_df["tawss"], label=self.imeSim)
        plt.ylim(0, 1)

        plt.title("TAWSS ")
        plt.ylabel("TAWSS [kPa]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        plt.legend()



    def plot_radius(self):
        plt.plot(self.podaci_df["z"], self.podaci_df["r"], label=self.imeSim)

        plt.title("R ")
        plt.ylabel("R [mm]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        plt.legend()



        # plt.plot(self.podaci_df["z"], self.podaci_df["r"], label=self.imeSim)










case_3 = VadenjePodataka(s1)




















plt.show()
