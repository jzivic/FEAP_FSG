import collections
import os

# import numpy as np
# import pandas as pd
import pandas as pd

from SimulationsData import *



suffix_list = ["89-5"]



TSLenght = 121


TSLenght_res_Inner_lines = TSLenght + 1
TSLlenght_res_Outer_lines = TSLenght + 1
TSLlenght_res_ILT_lines = TSLenght + 1
TSLlenght_rN0841 = 1







class FSG_Analysis:


    def __init__(self):

        # Podaci svih simulacija i svih vremenskih koraka
        all_simulations_data_df = pd.DataFrame({"timeStep":[],
                                                "inner_contours":[],
                                                "z":[],
                                                "outer_contours":[],
                                                "ILT_contours":[],
                                                "ILT_thickness_contours":[],
                                                "vein_thickness_contours": [],
                                                },
                                            index= [])



        for simulation_folder in simulations:                               # ulazi u folder simulacije
            simulation_path = results_directory + simulation_folder
            os.chdir(simulation_path)

            # Setting simulation
            self.simulation_name = simulation_folder
            self.set_files()
            self.data_construction()



            for self.time_step in chosen_TimeSteps:
                self.setting_start_lines()
                # self.check_AAA_formation()

                try:
                    self.timeStep_extraction()
                except IndexError:
                    pass


            dopuna = [self.oneSim_data_dict["timeStep"],
                      self.oneSim_data_dict["inner_contours"],
                      self.oneSim_data_dict["z"],
                      self.oneSim_data_dict["outer_contours"],
                      self.oneSim_data_dict["ILT_contours"],

                      self.oneSim_data_dict["ILT_thickness_contours"],
                      self.oneSim_data_dict["vein_thickness_contours"]
                      ]

            all_simulations_data_df.loc[self.simulation_name] = dopuna
        all_simulations_data_df.to_pickle("//home/josip/PycharmProjects/FEAP_FSG/podaci_analize.pickle")








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


    def data_construction(self):
        self.r0 = float(self.whole_document_Inner_lines[5].strip().split()[0]) * 2
        self.oneSim_data_dict = {"timeStep":[], "inner_contours":[], "z":[], "outer_contours":[], "ILT_contours":[],
                                 "ILT_thickness_contours":[], "vein_thickness_contours":[]}






        #

    # Svaki vremenski korak se vrti

    def setting_start_lines(self):
        self.startLine_res_Inner_lines = 5 + TSLenght_res_Inner_lines * (self.time_step - 1)
        self.startLine_res_ILT_lines = self.startLine_res_Inner_lines
        self.startLine_res_Outer_lines = self.startLine_res_Inner_lines

    def check_AAA_formation(self):
        for line in self.whole_document_Inner_lines[self.startLine_res_Inner_lines:
        (self.startLine_res_Inner_lines + TSLenght_res_Inner_lines -1)]:
            R = float(line.strip().split()[0])
            if R > 1.1 * self.r0:                                               # kako ovo definirati - mijenja se?
                return True
        return False


    def timeStep_extraction(self):
        timeSteps_list, d_inner_list, z_list, d_outer_list, d_ILT_list = [], [], [], [], []
        ILT_thickness_list, vein_thickness_list = [], []
        for n_line in range(TSLenght_res_Inner_lines-1):

            d_inner = float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line].strip().split()[0])
            z = float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line].strip().split()[3])
            d_outer = float(self.whole_document_Outer_lines[self.startLine_res_Outer_lines + n_line].strip().split()[0])
            d_ILT = float(self.whole_document_ILT_lines[self.startLine_res_ILT_lines + n_line].strip().split()[0])
            ILT_thickness = d_inner - d_ILT
            vein_thickness = d_outer - d_inner

            d_inner_list.append(d_inner)
            z_list.append(z)
            d_outer_list.append(d_outer)
            d_ILT_list.append(d_ILT)
            ILT_thickness_list.append(ILT_thickness)
            vein_thickness_list.append(vein_thickness)

        self.oneSim_data_dict["timeStep"].append(self.time_step)

        self.oneSim_data_dict["inner_contours"].append(d_inner_list)
        self.oneSim_data_dict["z"].append(z_list)
        self.oneSim_data_dict["outer_contours"].append(d_outer_list)
        self.oneSim_data_dict["ILT_contours"].append(d_ILT_list)

        self.oneSim_data_dict["ILT_thickness_contours"].append(ILT_thickness_list)
        self.oneSim_data_dict["vein_thickness_contours"].append(vein_thickness_list)








FSG_Analysis()








