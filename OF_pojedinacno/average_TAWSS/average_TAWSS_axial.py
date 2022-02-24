import math
import os
import matplotlib.pyplot as plt
import pandas as pd





simulacija_foam = "/home/josip/feap/FSG/automatizacija_19/simulacija20_5"






class VadenjePodataka:
    def __init__(self, Case, avg_neighbors, foam_Z_elements):

        korak = 2
        self.imeSim = Case.split("/")[-1]
        self.foam_Z_elements = foam_Z_elements
        self.avg_neighbors = avg_neighbors   # koliko susjeda sudjeluje u prosjeku (3= čvor + susjed sa svake strane)

        self.koo_file = Case + "/"+str(korak)+"/koordinate"
        self.TAWSS_file = Case + "/"+str(korak)+"/TAWSS"

        self.reading_koordinate()
        self.reading_TAWSS()
        self.podaci_df = pd.DataFrame(self.podaci_dict)


        self.plot_TAWSS()
        self.podaci_df["tawss_avg"] = self.averaging_TAWSS(3)
        plt.show()


        self.write_TAWSS()




    def reading_koordinate(self):
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


    def reading_TAWSS(self):
        read_TAWSS = False
        for red in open(self.TAWSS_file).readlines():
            red = red.strip()
            if red =="(":
                read_TAWSS = True
                continue
            if red ==")":
                read_TAWSS = False
                continue
            if read_TAWSS == True:
                self.podaci_dict["tawss"].append(float(red))


    def averaging_TAWSS(self, n_neighb):
        n_neighb *= self.foam_Z_elements
        if n_neighb % 2 == 0:
            n_neighb +=1
        avg_tawss_list = list(self.podaci_df["tawss"])
        start_index = int((n_neighb-1)/2)     # početni index da se izbjegnu rubovi
        for n in range(start_index, (len(self.podaci_df["tawss"])-start_index), 1):
            neighbours = [self.podaci_df["tawss"][(n-start_index) + i] for i in range(n_neighb)]
            tawss_avg = sum(neighbours)/len(neighbours)
            avg_tawss_list[n] = tawss_avg
        plt.plot(self.podaci_df["z"], avg_tawss_list, label="avg")
        return avg_tawss_list



    def plot_TAWSS(self):
        plt.plot(self.podaci_df["z"], self.podaci_df["tawss"], label="org")
        plt.ylim(0, 1)
        plt.title(self.imeSim)
        plt.ylabel("TAWSS [kPa]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        plt.legend()



    def write_TAWSS(self):

        text_file = open(self.TAWSS_file, "r").readlines()
        number_lines = sum(1 for line in text_file)


        start_line = 52
        finish_line = number_lines-7

        intro_tawss = text_file[0:start_line]
        outro_tawss = text_file[finish_line::]
        tawss_avg = [str(i)+"\n" for i in self.podaci_df["tawss_avg"]]

        novi = open("pero",  "w")
        novi.writelines(intro_tawss)
        novi.writelines(tawss_avg)
        novi.writelines(outro_tawss)
        novi.close()










case_3 = VadenjePodataka(simulacija_foam, 3, foam_Z_elements=5)         # 1 == bez osrednjavanja, samo taj jedan čvor se gleda




















# plt.show()
