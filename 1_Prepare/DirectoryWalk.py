import os

# import numpy as np
# import pandas as pd


from SimulationsData import *



suffix_list = ["89-5"]



TSLenght = 121


TSLenght_res_Inner_lines = TSLenght + 1
TSLegnht_res_Outer_lines = TSLenght + 1
TSLegnht_res_ILT_lines = TSLenght + 1
TSLegnht_rN0841 = 1







class FSG_Analysis:


    def __init__(self):

        for simulation_folder in simulations:                               # ulazi u folder simulacije
            simulation_path = results_directory + simulation_folder
            os.chdir(simulation_path)



            # Setting simulation
            self.simulation_name = simulation_folder
            self.set_files()
            self.d0 = float(self.whole_document_Inner_lines[5].strip().split()[0]) * 2



            for self.time_step in chosen_TimeSteps:
                self.startLine_res_Inner_lines = 5 + TSLenght_res_Inner_lines * (self.time_step - 1)
                self.startLine_res_ILT_lines = self.startLine_res_Inner_lines
                self.startLine_res_Outer_lines = self.startLine_res_Inner_lines


                self.check_AAA_formation()









    def set_files(self):
        opening_res_NODE_0841 = open("res__NODE_0841_89-5", "r")  # open txt file
        self.whole_document_res_NODE_0841 = opening_res_NODE_0841.readlines()  # whole txt read in self.wholeDocument_eIW
        self.nl_res_NODE = sum(1 for line in open("res__NODE_0841_89-5"))  # number of lines in export Inner Wall

        self.max_TS = self.nl_res_NODE - 5

        opening_res_Inner_lines = open("res__INNER_lines__89-5", "r")  # open txt file
        self.whole_document_Inner_lines = opening_res_Inner_lines.readlines()  # whole txt read in self.wholeDocument_eIW
        self.nl_res_Inner_lines = sum(1 for line in open("res__INNER_lines__89-5"))  # number of lines in export Inner Wall


        opening_res_ILT_lines = open("res__ILT_lines__89-5", "r")  # open txt file
        self.whole_document_ILT_lines = opening_res_ILT_lines.readlines()  # whole txt read in self.wholeDocument_eIW
        self.nl_res_ILT_lines = sum(1 for line in open("res__ILT_lines__89-5"))  # number of lines in export Inner Wall



    def check_AAA_formation(self):
        for line in self.whole_document_Inner_lines[self.startLine_res_Inner_lines:
                    (self.startLine_res_Inner_lines + TSLenght_res_Inner_lines -1)]:

            D = float(line.strip().split()[0]) * 2


            # if D > 1.5 * self.d0:     # kako ovo definirati - mijenja se?
            #     print(D, self.d0)





FSG_Analysis()








