from SimulationsData import *


import os
import pandas as pd


TSLenght = 121
TSLenght_res_Inner_lines = TSLenght + 1
TSLlenght_res_Outer_lines = TSLenght + 1
TSLlenght_res_ILT_lines = TSLenght + 1
TSLlenght_rN0841 = 1
TSLlenght_res_Y0__field = 850
# suffix_list = ["89-5"]


class FSG_Analysis:

    def __init__(self):

        # Podaci svih simulacija i svih vremenskih koraka
        all_simulations_data_df = pd.DataFrame({"timeStep":[],
                                                "inner_contours":[],
                                                "outer_contours": [],
                                                "ILT_contours": [],
                                                "Z_contours":[],
                                                "ILT_thickness_contours":[],
                                                "vein_thickness_contours": [],
                                                "S22_contours": [],

                                                "H": [],
                                                "D_max": [],
                                                "S22_max": [],
                                                "ILT_thickness_max": [],
                                                "vein_thickness_max": [],
                                                },
                                            index= [])


        for simulation_folder in simulation_names:                               # ulazi u folder simulacije
            simulation_path = results_directory + simulation_folder
            os.chdir(simulation_path)
            # Setting simulation
            self.simulation_name = simulation_folder
            self.set_files()
            self.data_construction()

            for self.time_step in chosen_TimeSteps:
                self.setting_start_lines()

                if self.check_AAA_formation() == True:
                    try:
                        self.timeStep_extraction()
                    except IndexError:
                        pass

                elif self.check_AAA_formation() == False:
                    dopuna = [None for i in range(len(all_simulations_data_df))]

            dopuna = [self.oneSim_data_dict["timeStep"],

                      self.oneSim_data_dict["inner_contours"],
                      self.oneSim_data_dict["outer_contours"],
                      self.oneSim_data_dict["ILT_contours"],
                      self.oneSim_data_dict["Z_contours"],

                      self.oneSim_data_dict["ILT_thickness_contours"],
                      self.oneSim_data_dict["vein_thickness_contours"],
                      self.oneSim_data_dict["S22_contours"],

                      self.oneSim_data_dict["H"],
                      self.oneSim_data_dict["D_max"],
                      self.oneSim_data_dict["S22_max"],
                      self.oneSim_data_dict["ILT_thickness_max"],
                      self.oneSim_data_dict["vein_thickness_max"]
                      ]


            all_simulations_data_df.loc[self.simulation_name] = dopuna
        all_simulations_data_df.to_pickle(pickle_name)


    # Samo jednom se postavlja

    def set_files(self):
        opening_res_NODE_0841 = open("res__NODE_0841_89-5", "r")  # open txt file
        self.whole_document_res_NODE_0841 = opening_res_NODE_0841.readlines()  # whole txt read in self.wholeDocument_eIW
        self.nl_res_NODE = sum(1 for line in open("res__NODE_0841_89-5"))  # number of lines in export Inner Wall

        self.max_TS = self.nl_res_NODE - 5

        opening_res_Inner_lines = open("res__INNER_lines__89-5", "r")  # open txt file
        self.whole_document_Inner_lines = opening_res_Inner_lines.readlines()  # whole txt read in self.wholeDocument_eIW
        self.nl_res_Inner_lines = sum(1 for line in open("res__INNER_lines__89-5"))  # number of lines in export Inner Wall

        opening_res_Outer_lines = open("res__OUTER_lines__89-5", "r")  # open txt file
        self.whole_document_Outer_lines = opening_res_Outer_lines.readlines()  # whole txt read in self.wholeDocument_eIW
        self.nl_res_Outer_lines = sum(1 for line in open("res__OUTER_lines__89-5"))  # number of lines in export Inner Wall


        opening_res_ILT_lines = open("res__ILT_lines__89-5", "r")  # open txt file
        self.whole_document_ILT_lines = opening_res_ILT_lines.readlines()  # whole txt read in self.wholeDocument_eIW
        self.nl_res_ILT_lines = sum(1 for line in open("res__ILT_lines__89-5"))  # number of lines in export Inner Wall

        opening_res_Y0_field = open("res__Y0_field__89-5", "r")  # open txt file
        self.whole_document_res_Y0_field = opening_res_Y0_field.readlines()  # whole txt read in self.wholeDocument_eIW
        self.nl_res_Y0_field = sum(1 for line in open("res__Y0_field__89-5"))  # number of lines in export Inner Wall



    def data_construction(self):
        self.r0 = float(self.whole_document_Inner_lines[5].strip().split()[0])
        self.oneSim_data_dict = {"timeStep":[], "inner_contours":[], "outer_contours":[], "ILT_contours":[],
                                 "Z_contours":[], "ILT_thickness_contours":[], "vein_thickness_contours":[],
                                 "S22_contours": [],
                                 "H":[], "D_max":[],"S22_max":[], "ILT_thickness_max":[], "vein_thickness_max":[]
                                 }



    # Svaki vremenski korak se vrti

    def setting_start_lines(self):
        self.startLine_res_Inner_lines = 5 + TSLenght_res_Inner_lines * (self.time_step - 1)
        self.startLine_res_ILT_lines = self.startLine_res_Inner_lines
        self.startLine_res_Outer_lines = self.startLine_res_Inner_lines

        # mogućnost odabira 1-7 radijalnog elementa, 1: skroz unutarnji, 7: vanjski
        radial_layer = 1
        assert radial_layer in [1,2,3,4,5,6,7],  "Nedopušteni layer elementa"
        self.startLine_res_Y0_field = 139 + TSLlenght_res_Y0__field * self.time_step + ((radial_layer-1)*TSLenght)



    def check_AAA_formation(self):
        for line in self.whole_document_Inner_lines[self.startLine_res_Inner_lines:
                (self.startLine_res_Inner_lines + TSLenght_res_Inner_lines -1)]:

            R = float(line.strip().split()[0])
            if R > 1.0 * self.r0:                                               # kako ovo definirati - mijenja se?
                return True
        return False


    def timeStep_extraction(self):
        timeSteps_list, r_inner_list, z_list, r_outer_list, r_ILT_list = [], [], [], [], []
        ILT_thickness_list, vein_thickness_list, h_list, S22_list = [], [], [], [],

        for n_line in range(TSLenght_res_Inner_lines-1):

            r_inner = float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line].strip().split()[0])
            r_outer = float(self.whole_document_Outer_lines[self.startLine_res_Outer_lines + n_line].strip().split()[0])
            r_ILT = float(self.whole_document_ILT_lines[self.startLine_res_ILT_lines + n_line].strip().split()[0])
            ILT_thickness = r_inner - r_ILT
            vein_thickness = r_outer - r_inner
            z = float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line].strip().split()[3])
            S22 = float(self.whole_document_res_Y0_field[self.startLine_res_Y0_field+n_line].strip().split()[4])*1000 #kPa

            r_inner_list.append(r_inner)
            r_outer_list.append(r_outer)
            r_ILT_list.append(r_ILT)
            ILT_thickness_list.append(ILT_thickness)
            vein_thickness_list.append(vein_thickness)
            z_list.append(z)
            S22_list.append(S22)
            # S22_list.append(0)

            if r_inner > 1.05 * self.r0:
                h_list.append(z)

        H = h_list[-1] - h_list[0]
        D_max = max(r_inner_list)*2
        S22_max = max(S22_list)
        ILT_thickness_max = max(ILT_thickness_list)
        vein_thickness_max = max(vein_thickness_list)



        self.oneSim_data_dict["timeStep"].append(self.time_step)

        self.oneSim_data_dict["inner_contours"].append(r_inner_list)
        self.oneSim_data_dict["outer_contours"].append(r_outer_list)
        self.oneSim_data_dict["ILT_contours"].append(r_ILT_list)
        self.oneSim_data_dict["Z_contours"].append(z_list)

        self.oneSim_data_dict["ILT_thickness_contours"].append(ILT_thickness_list)
        self.oneSim_data_dict["vein_thickness_contours"].append(vein_thickness_list)
        self.oneSim_data_dict["S22_contours"].append(S22_list)

        self.oneSim_data_dict["H"].append(H)
        self.oneSim_data_dict["D_max"].append(D_max)
        self.oneSim_data_dict["S22_max"].append(S22_max)

        self.oneSim_data_dict["ILT_thickness_max"].append(ILT_thickness_max)
        self.oneSim_data_dict["vein_thickness_max"].append(vein_thickness_max)




FSG_Analysis()






