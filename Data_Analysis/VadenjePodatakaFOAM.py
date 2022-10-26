import matplotlib.pyplot as plt
import pandas as pd


class VadenjePodataka_FOAM:
    def __init__(self, Case, simulation_number):
        foam_time = 2

        self.koo_file = Case + "/simulacija"+str(simulation_number)+"/"+str(foam_time)+"/koordinate"
        self.TAWSS_file = Case + "/simulacija"+str(simulation_number)+"/"+str(foam_time)+"/TAWSS"
        self.OSI_file = Case + "/simulacija"+str(simulation_number)+"/"+str(foam_time)+"/OSI"
        self.ECAP_file = Case + "/simulacija"+str(simulation_number)+"/"+str(foam_time)+"/ECAP"

        self.data_dict = {"r":[], "z":[], "TAWSS":[], "OSI":[],"ECAP":[] }
        self.Koordinate_reading()
        self.TAWSS_reading()
        self.OSI_reading()
        self.ECAP_reading()
        self.data_DF = pd.DataFrame(self.data_dict)

        self.return_Z_foam()
        self.return_TAWSS()
        self.return_OSI()
        self.return_ECAP()




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


    def return_TAWSS(self):
        return self.data_dict["TAWSS"]

    def return_OSI(self):
        return self.data_dict["OSI"]

    def return_ECAP(self):
        return self.data_dict["ECAP"]

    def return_Z_foam(self):
        return self.data_dict["z"]





# p9 = VadenjePodataka_FOAM(case)

