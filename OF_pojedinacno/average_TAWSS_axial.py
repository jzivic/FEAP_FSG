import math
import os
import matplotlib.pyplot as plt
import pandas as pd




s1 = "//home/josip/feap/FSG/automatizacija_18/foam_axial=1_2/simulacija25"





class VadenjePodataka:
    def __init__(self, Case, avg_neighbors):

        korak = 2
        self.imeSim = Case.split("/")[-2]

        self.avg_neighbors = avg_neighbors   # koliko susjeda sudjeluje u prosjeku (3= čvor + susjed sa svake strane)

        self.koo_file = Case + "/"+str(korak)+"/koordinate"
        self.TAWSS_file = Case + "/"+str(korak)+"/TAWSS"

        self.citanje_koordinata()
        self.citanje_TAWSS()
        self.podaci_df = pd.DataFrame(self.podaci_dict)
        # self.averaging_TAWSS()


        self.plot_TAWSS()
        self.averaging_TAWSS_additional(3)
        self.averaging_TAWSS_additional(5)


        # self.plot_radius()





    def citanje_koordinata(self):
        self.podaci_dict = {"r":[], "z":[],"tawss":[]}

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



    # def averaging_TAWSS(self):  # ovo će se korisitit kada bude potvrđeno broj susjeda
    #     assert self.avg_neighbors % 2 == 1, "broj susjeda za osrednjavanje mora biti neparan"
    #     avg_tawss_list = list(self.podaci_df["tawss"])
    #
    #     skip = 0
    #     start_index = int((self.avg_neighbors-1)/2)     # početni index da se izbjegnu rubovi
    #
    #     for n in range(skip+start_index, (len(self.podaci_df["tawss"])-start_index-skip), 1):
    #         neighbours = [self.podaci_df["tawss"][(n-start_index)  + i] for i in range(self.avg_neighbors)]
    #         tawss_avg = sum(neighbours)/len(neighbours)
    #         avg_tawss_list[n] = tawss_avg
    #     self.podaci_df["tawss_avg"] = avg_tawss_list









    def averaging_TAWSS_additional(self, n_neighb):
        assert n_neighb % 2 == 1, "broj susjeda za osrednjavanje mora biti neparan"
        avg_tawss_list = list(self.podaci_df["tawss"])

        skip = 0
        start_index = int((n_neighb-1)/2)     # početni index da se izbjegnu rubovi

        for n in range(skip+start_index, (len(self.podaci_df["tawss"])-start_index-skip), 1):
            neighbours = [self.podaci_df["tawss"][(n-start_index)  + i] for i in range(n_neighb)]
            tawss_avg = sum(neighbours)/len(neighbours)
            avg_tawss_list[n] = tawss_avg

        plt.plot(self.podaci_df["z"], avg_tawss_list, label=n_neighb)





    def plot_TAWSS(self):
        # plt.plot(self.podaci_df["z"], self.podaci_df["tawss_avg"], label=self.avg_neighbors)
        plt.plot(self.podaci_df["z"], self.podaci_df["tawss"], label="org")
        plt.ylim(0, 1)

        plt.title(self.imeSim)
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










case_3 = VadenjePodataka(s1, 3)         # 1 == bez osrednjavanja, samo taj jedan čvor se gleda




















plt.show()
