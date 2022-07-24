import math

from SimulationsData import *


import os
import numpy as  np
import pandas as pd


TSLenght = 121
TSLenght_res_Inner_lines = TSLenght + 1
TSLlenght_res_Outer_lines = TSLenght + 1
TSLlenght_res_ILT_lines = TSLenght + 1
TSLlenght_rN0841 = 1
TSLlenght_res_Y0__field = 850
Y0_corrention = 132                 # pomak Y0 file za broj redova nakon restarta

suffixes = ["89-5", "172-22"]





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
                                                "D_inner_max": [],
                                                "S22_max": [],
                                                "S22_Z_max_abs": [],

                                                "Z_S22_is_max": [],

                                                "ILT_thickness_max": [],
                                                "vein_thickness_max": [],
                                                "ILT_surface": [],
                                                "Volume_ILT": [],

                                                },
                                            index= [])

        for subdirectory in simulationsData_dict.keys():                               # ulazi u folder simulacije
            self.Y0_version = simulationsData_dict[subdirectory]["version"]
            simulations_in_directory = simulationsData_dict[subdirectory]["simulations"]

            for simulation_name in simulations_in_directory:
                simulation_path = subdirectory + simulation_name
                os.chdir(simulation_path)

                # Setting simulation
                self.simulation_name = simulation_name

                self.set_files()
                self.data_construction()


                for self.time_step in chosen_TimeSteps:

                    if self.time_step > self.max_TS:                 # prekida vađenje podataka za TS == maxTS
                        break

                    self.setting_start_lines()
                    if self.check_AAA_formation() == True:
                        self.timeStep_extraction()              # ovdje je bio try!!!

                    elif self.check_AAA_formation() == False:
                        dopuna = [None for i in all_simulations_data_df]

                dopuna = [self.oneSim_data_dict["timeStep"],

                          self.oneSim_data_dict["inner_contours"],
                          self.oneSim_data_dict["outer_contours"],
                          self.oneSim_data_dict["ILT_contours"],
                          self.oneSim_data_dict["Z_contours"],

                          self.oneSim_data_dict["ILT_thickness_contours"],
                          self.oneSim_data_dict["vein_thickness_contours"],
                          self.oneSim_data_dict["S22_contours"],

                          self.oneSim_data_dict["H"],
                          self.oneSim_data_dict["D_inner_max"],
                          self.oneSim_data_dict["S22_max"],
                          self.oneSim_data_dict["S22_Z_max_abs"],
                          self.oneSim_data_dict["Z_S22_is_max"],
                          self.oneSim_data_dict["ILT_thickness_max"],
                          self.oneSim_data_dict["vein_thickness_max"],
                          self.oneSim_data_dict["ILT_surface"],
                          self.oneSim_data_dict["Volume_ILT"]
                          ]

                all_simulations_data_df.loc[self.simulation_name] = dopuna
            all_simulations_data_df.to_pickle(pickle_name)


#     # Samo jednom se postavlja
    def set_files(self):
        self.restart_sign = False
        # self.restart_sign = True

        for suffix in suffixes:
            try:
                opening_res_NODE_0841 = open("res__NODE_0841_"+suffix, "r")  # open txt file
                self.whole_document_res_NODE_0841 = opening_res_NODE_0841.readlines()  # whole txt read in self.wholeDocument_eIW
                self.nl_res_NODE = sum(1 for line in open("res__NODE_0841_"+suffix))  # number of lines in export Inner Wall

                self.max_TS = self.nl_res_NODE - 5

                opening_res_Inner_lines = open("res__INNER_lines__"+suffix, "r")  # open txt file
                self.whole_document_Inner_lines = opening_res_Inner_lines.readlines()  # whole txt read in self.wholeDocument_eIW
                self.nl_res_Inner_lines = sum(1 for line in open("res__INNER_lines__"+suffix))  # number of lines in export Inner Wall

                opening_res_Outer_lines = open("res__OUTER_lines__"+suffix, "r")  # open txt file
                self.whole_document_Outer_lines = opening_res_Outer_lines.readlines()  # whole txt read in self.wholeDocument_eIW
                self.nl_res_Outer_lines = sum(1 for line in open("res__OUTER_lines__"+suffix))  # number of lines in export Inner Wall


                opening_res_ILT_lines = open("res__ILT_lines__"+suffix, "r")  # open txt file
                self.whole_document_ILT_lines = opening_res_ILT_lines.readlines()  # whole txt read in self.wholeDocument_eIW
                self.nl_res_ILT_lines = sum(1 for line in open("res__ILT_lines__"+suffix))  # number of lines in export Inner Wall

                if barcelona == False:
                    opening_res_Y0_field = open("res__Y0_field__"+suffix, "r")  # open txt file
                    self.whole_document_res_Y0_field = opening_res_Y0_field.readlines()  # whole txt read in self.wholeDocument_eIW
                    self.nl_res_Y0_field = sum(1 for line in open("res__Y0_field__"+suffix))  # number of lines in export Inner Wall

            except FileNotFoundError:
                continue



    def data_construction(self):
        self.r0 = float(self.whole_document_Inner_lines[5].strip().split()[0])
        self.oneSim_data_dict = {"timeStep":[], "inner_contours":[], "outer_contours":[], "ILT_contours":[],
                                 "Z_contours":[], "ILT_thickness_contours":[], "vein_thickness_contours":[],
                                 "S22_contours": [],
                                 "H":[], "D_inner_max":[],"S22_max":[], "Z_S22_is_max":[], "S22_Z_max_abs":[],
                                 "ILT_thickness_max":[], "vein_thickness_max":[],
                                 "ILT_surface":[], "Volume_ILT":[]
                                 }




##########################################################################################################################
    # Svaki vremenski korak se vrti
##########################################################################################################################



    def setting_start_lines(self):
        self.startLine_res_Inner_lines = 5 + TSLenght_res_Inner_lines * (self.time_step - 1)
        self.startLine_res_ILT_lines = self.startLine_res_Inner_lines
        self.startLine_res_Outer_lines = self.startLine_res_Inner_lines

        # ovo će biti startni red koraka: uvijek je prazna linija:
        self.startLine_res_Y0_field = 139 + TSLlenght_res_Y0__field * (self.time_step-1)        #OVO
        first_node_row = self.whole_document_res_Y0_field[self.startLine_res_Y0_field].strip().split()

        if first_node_row[0] == "o--->":    # dodatak ako postoji restart opcija jer zapiše zaglavlje za restart TS
            self.restart_sign = True

        if self.restart_sign == True:
            self.startLine_res_Y0_field += Y0_corrention

    def check_AAA_formation(self):
        for line in self.whole_document_Inner_lines[self.startLine_res_Inner_lines:
                (self.startLine_res_Inner_lines + TSLenght_res_Inner_lines -1)]:
            R = float(line.strip().split()[0])
            if R > 0.99 * self.r0:                                               # kako ovo definirati - mijenja se?
                return True
        return False


    def timeStep_extraction(self):
        timeSteps_list, r_inner_list, z_list, r_outer_list, r_ILT_list = [], [], [], [], []
        ILT_thickness_list, vein_thickness_list, h_list, S22_list, ILT_surface, Volume_ILT = [], [], [], [], 0, 0

        for n_line in range(TSLenght_res_Inner_lines-1):
            r_inner = float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line].strip().split()[0])
            r_outer = float(self.whole_document_Outer_lines[self.startLine_res_Outer_lines + n_line].strip().split()[0])
            r_ILT = float(self.whole_document_ILT_lines[self.startLine_res_ILT_lines + n_line].strip().split()[0])
            ILT_thickness = r_inner - r_ILT
            vein_thickness = r_outer - r_inner
            z = float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line].strip().split()[3])


            if barcelona == False:
                if self.Y0_version == "old":
                    S22_list_by_thickness = []      # lista naprezanja po layerima na istom Z

                    for node in range(7):
                        n_row = self.startLine_res_Y0_field + n_line + (node*TSLenght)
                        row = self.whole_document_res_Y0_field[n_row].strip().split()
                        S22 = float(row[4])*1000
                        S22_list_by_thickness.append(S22)

                elif self.Y0_version == "new":
                    S22_list_by_thickness = []
                    for node in range(7):
                        n_row = self.startLine_res_Y0_field + 7*n_line + node
                        row = self.whole_document_res_Y0_field[n_row].strip().split()
                        # print(n_row)
                        S22 = float(row[4])*1000
                        S22_list_by_thickness.append(S22)


            elif barcelona == True:
                S22 = 0

            if n_line > 0:
                delta_z = float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line].strip().split()[3]) - \
                          float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line-1].strip().split()[3])
                ilt_surface = delta_z * (r_inner-r_ILT)/2
                ILT_surface += ilt_surface

                r_ILT_delta = r_inner - r_ILT
                r_center = r_ILT + (r_ILT_delta) / 2
                V_ILT = r_ILT_delta * r_center * 2 * math.pi    #Volumen ILT-a
                Volume_ILT += V_ILT

            r_inner_list.append(r_inner)
            r_outer_list.append(r_outer)
            r_ILT_list.append(r_ILT)
            ILT_thickness_list.append(ILT_thickness)
            vein_thickness_list.append(vein_thickness)
            z_list.append(z)
            S22_list.append(S22_list_by_thickness)



            if r_inner > 1.05 * self.r0:
                h_list.append(z)
                H = h_list[-1] - h_list[0]

        D_inner_max = max(r_inner_list)*2


        # S22_Z_max_abs = max(S22_list, key=max)
        # ind_S22_Z_max_abs = S22_list.index(S22_Z_max_abs)


        S22_list = np.array(S22_list)
        S22_inner_nodes_list = S22_list[:,0]        # max index se uvijek vadi iz 1. čvora!!
        S22_max_inner = max(S22_inner_nodes_list)
        S22_max_by_thickness = [max(S22_list[:,i]) for i in range(7)]   # sprema se max vrijednost za svaki layer

        z_ind_list = np.where(S22_inner_nodes_list == S22_max_inner)[0]
        Z_ind = int(sum(z_ind_list)/len(z_ind_list))
        Z_S22_is_max = {"height": z_list[Z_ind], "index": Z_ind}


        S22_Z_max_abs = max(max(S22_list, key=max))    # layer gdje se nalazi jendo max naprezanje za cijeli korak

        list_ind_abs = []
        for n in range(len(S22_list)):
            if S22_Z_max_abs in S22_list[n]:
                list_ind_abs.append(n)
        ind_S22_Z_max_abs = int(sum(list_ind_abs) / ( len(list_ind_abs)))
        S22_Z_max_abs = {"S22":S22_Z_max_abs,  "height": z_list[ind_S22_Z_max_abs]}




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

        try:
            self.oneSim_data_dict["H"].append(H)
        except UnboundLocalError:
            self.oneSim_data_dict["H"].append(0)

        self.oneSim_data_dict["D_inner_max"].append(D_inner_max)
        self.oneSim_data_dict["S22_max"].append(S22_max_by_thickness)
        self.oneSim_data_dict["Z_S22_is_max"].append(Z_S22_is_max)

        self.oneSim_data_dict["S22_Z_max_abs"].append(S22_Z_max_abs)

        self.oneSim_data_dict["ILT_thickness_max"].append(ILT_thickness_max)
        self.oneSim_data_dict["vein_thickness_max"].append(vein_thickness_max)
        self.oneSim_data_dict["ILT_surface"].append(ILT_surface)
        self.oneSim_data_dict["Volume_ILT"].append(Volume_ILT)




FSG_Analysis()











# aj = [red     for red in S22_list if S22_Z_max_abs in red]
# proba = np.where(S22_Z_max_abs in i for i in S22_list)              #NEK OSTANE ZA PY UČENJE