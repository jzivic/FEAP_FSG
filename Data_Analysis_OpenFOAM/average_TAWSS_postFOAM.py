"""
Ako nije ništa osrednjeno u foam-u, ovo treba samo jednom provrtiti i TAWSS, OSI i ECAP 
će se osrednjiti. Nakon toga ide samo plotanje grafova
"""


import matplotlib.pyplot as plt
import pandas as pd


simulacija_foam = "//home/josip/feap/FSG/automatizacija_25/Casson/simulacija50"



FF_system = False

class AveragingParameters:
    
    def __init__(self, Case ):
        foam_time = 2
        self.simulation_name = Case.split("/")[-1]


        self.koo_file = Case + "/"+str(foam_time)+"/koordinate"
        self.TAWSS_file = Case + "/"+str(foam_time)+"/TAWSS"
        self.OSI_file = Case + "/"+str(foam_time)+"/OSI"
        self.ECAP_file = Case + "/"+str(foam_time)+"/ECAP"

        self.data_dict = {"r":[], "z":[], "TAWSS":[], "OSI":[],"ECAP":[] }

        self.Koordinate_reading()
        self.TAWSS_reading()
        self.OSI_reading()
        self.ECAP_reading()

        self.data_dict["TAWSS_avg"] = self.parameter_averaging("TAWSS")
        self.data_dict["OSI_avg"] = self.parameter_averaging("OSI")
        self.data_dict["ECAP_avg"] = self.parameter_averaging("ECAP")

        self.data_DF = pd.DataFrame(self.data_dict)
        self.write_parameter("TAWSS")
        self.write_parameter("ECAP")
        self.write_parameter("OSI")

        self.plot_parameter("TAWSS")
        self.plot_parameter("OSI")
        self.plot_parameter("ECAP")




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


    def parameter_averaging(self, parameter_name):
        n_neighb = 3
        if n_neighb % 2 == 0:
            n_neighb +=1
        average_list = list(self.data_dict[parameter_name])
        start_index = int((n_neighb-1)/2)     # početni index da se izbjegnu rubovi
        for n in range(start_index, (len(self.data_dict[parameter_name])-start_index), 1):
            neighbours = [self.data_dict[parameter_name][(n-start_index) + i] for i in range(n_neighb)]
            parameter_avg = sum(neighbours)/len(neighbours)
            average_list[n] = parameter_avg
        return average_list


    def write_parameter(self, parameter_name):

        if parameter_name == "TAWSS":
            text_file = open(self.TAWSS_file, "r").readlines()
        elif parameter_name == "OSI":
            text_file = open(self.OSI_file, "r").readlines()
        elif parameter_name == "ECAP":
            text_file = open(self.ECAP_file, "r").readlines()

        number_lines = sum(1 for line in text_file)
        start_line = 52
        finish_line = number_lines-7
        intro_file = text_file[0:start_line]
        outro_file = text_file[finish_line::]
        parameter_avg = [str(i)+"\n" for i in self.data_DF[parameter_name+"_avg"]]

        if FF_system == True:
            if parameter_name == "TAWSS":
                new_text_file = open(self.TAWSS_file, "w")
            elif parameter_name == "OSI":
                new_text_file = open(self.OSI_file, "w")
            elif parameter_name == "ECAP":
                new_text_file = open(self.ECAP_file, "w")


        elif FF_system == False:
            if parameter_name == "TAWSS":
                new_text_file = open(self.TAWSS_file+"_avg",  "w")
            elif parameter_name == "OSI":
                new_text_file = open(self.OSI_file+"_avg",  "w")
            elif parameter_name == "ECAP":
                new_text_file = open(self.ECAP_file+"_avg",  "w")


        new_text_file.writelines(intro_file)
        new_text_file.writelines(parameter_avg)
        new_text_file.writelines(outro_file)
        new_text_file.close()




    def plot_parameter(self, parameter_name):

        fig = plt.gcf()
        plt.plot(self.data_DF["z"], self.data_DF[parameter_name], label="org")
        plt.plot(self.data_DF["z"], self.data_DF[parameter_name+"_avg"], label="avg")

        plt.title(parameter_name)
        plt.ylabel(parameter_name)
        plt.xlabel("z [mm]")
        plt.grid(which='both', linestyle='--', linewidth='0.5')
        plt.legend()

        if FF_system == True:
            plt.draw()
            plt.close()
            fig.savefig(simulacija_foam+"/"+parameter_name+'_avging.png', dpi=300)

        elif FF_system == False:
            plt.show()




avg = AveragingParameters(simulacija_foam)


















