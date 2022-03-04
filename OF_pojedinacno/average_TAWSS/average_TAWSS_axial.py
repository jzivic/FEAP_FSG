import math
import os
import matplotlib.pyplot as plt
import pandas as pd
simulacija_foam = "//home/josip/feap/FSG/sranje"     # ovo je isključeno za foam siimulacije





class VadenjePodataka:
    def __init__(self, Case, foam_Z_elements, average_way):

        korak = 2
        self.imeSim = Case.split("/")[-1]
        self.foam_Z_elements = foam_Z_elements
        assert average_way in ["Lana", "Josip"], "popravi način osrednjavanja"  # "Lana" ili "Josip" mora biti
        self.average_way = average_way

        self.koo_file = Case + "/"+str(korak)+"/koordinate"
        self.TAWSS_file = Case + "/"+str(korak)+"/TAWSS"

        self.reading_koordinate()
        self.reading_TAWSS()

        self.podaci_df = pd.DataFrame(self.podaci_dict)
        self.podaci_df["tawss_avg"] = self.averaging_TAWSS(3)
        self.podaci_df["tawss_avg_Lana"] = self.averaging_TAWSS_Lana()

        self.plot_TAWSS()

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
        return avg_tawss_list


    # Uprosječuje sve fomove elemente u jednom feapovom i u te fomove zapisuje isto
    def averaging_TAWSS_Lana(self):
        tawss_avg_Lana = []
        for f_n in range(self.foam_Z_elements-1, len(self.podaci_df["tawss"])+1, self.foam_Z_elements):
            foam_in_feap_element = []
            for n in range(f_n-4, f_n+1):
                foam_in_feap_element.append(self.podaci_df["tawss"][n])
            element_average = sum(foam_in_feap_element)/len(foam_in_feap_element)
            tawss_avg_Lana.extend([element_average for i in range(self.foam_Z_elements)])
        return tawss_avg_Lana


    def plot_TAWSS(self):
        fig = plt.gcf()
        plt.plot(self.podaci_df["z"], self.podaci_df["tawss"], label="org")
        plt.plot(self.podaci_df["z"], self.podaci_df["tawss_avg"], label="avg")
        plt.ylim(0, 1)
        plt.title(self.imeSim)
        plt.ylabel("TAWSS [kPa]")
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        plt.legend()
        plt.draw()
        plt.close()
        fig.savefig('TAWSS_avg.png', dpi=300)


    def write_TAWSS(self):
        text_file = open(self.TAWSS_file, "r").readlines()
        number_lines = sum(1 for line in text_file)

        start_line = 52
        finish_line = number_lines-7

        intro_tawss = text_file[0:start_line]
        outro_tawss = text_file[finish_line::]

        if self.average_way == "Josip":
            tawss_avg = [str(i)+"\n" for i in self.podaci_df["tawss_avg"]]
        elif self.average_way == "Lana":
            tawss_avg = [str(i)+"\n" for i in self.podaci_df["tawss_avg_Lana"]]

        # new_tawss_file = open(self.TAWSS_file,  "w")
        new_tawss_file = open("ae",  "w")
        new_tawss_file.writelines(intro_tawss)
        new_tawss_file.writelines(tawss_avg)
        new_tawss_file.writelines(outro_tawss)
        new_tawss_file.close()




avg = VadenjePodataka(simulacija_foam, foam_Z_elements=5, average_way="Lana")         # 1 == bez osrednjavanja, samo taj jedan čvor se gleda




















