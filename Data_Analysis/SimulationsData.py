chosen_TimeSteps = [i for i in range(1,666)]        # mora od 1 od nekog broja!!


# x = 100
# chosen_TimeSteps = [i for i in range(x,x+1)]

barcelona = False






pickle_name_25 = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_25.pickle"
simulationsData_dict_25 = {

                "//home/josip/feap/FSG/automatizacija_25/":
                    {"version": "old",

                     "simulations":
                         [
                            "a3_30",
                            "a3_40",
                            "ab=900",
                            "BC",
                            "Casson",


                            "Newt_5",
                            "Newt_6",
                            "Newt_33",

                            "tawss=030",
                            "tawss=035",
                            "tawss=040",
                            "tawss=045",
                            "tawss=050",

                                        ]
                     },


                # "//home/josip/feap/FSG/automatizacija_35/":
                #     {"version": "new",
                #
                #      "simulations":
                #          [
                #             "osi_le_035_3",
                #             "osi_le_030_3",
                #             "osi_le_025_3",
                #             "osi_le_020_3",
                #
                #             "osi_gt_55",
                #             "osi_gt_050",
                #             "osi_gt_045",
                #             "osi_gt_40",
                #
                #             "ecap_le_060",
                #             "ecap_le_055",
                #             "ecap_le_050",
                #                                 ]
                #      },


          }

pickle_name_36 = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_36.pickle"
simulationsData_dict_36 = {
                # "//home/josip/feap/FSG/automatizacija_25/":
                #     {"version": "old",
                #
                #      "simulations":
                #          [
                #          "tawss=030",
                #          "tawss=035",
                #          "tawss=040",
                #          "tawss=045",
                #          "tawss=050",
                #           ]
                #      },


                "//home/josip/feap/FSG/automatizacija_36/TAWSS/":
                    {"version": "new",

                     "simulations":
                         [
                            "tawss_le_030",
                            "tawss_le_035",
                            "tawss_le_040",
                            "tawss_le_045",
                             "tawss_le_0475",
                             "tawss_le_0475",
                            "tawss_le_04825",
                            "tawss_le_050",
                          ]
                     },

                # "//home/josip/feap/FSG/automatizacija_36/OSI/GREATER/":
                #     {"version": "new",
                #
                #      "simulations":
                #          [
                #              # "osi_gt_0375",
                #              # "osi_gt_0400",
                #              # "osi_gt_0425",
                #              # "osi_gt_0450",
                #              # "osi_gt_04625",
                # #
                #              "osi_gt_04675",        # 3. runda
                #              "osi_gt_04725",        # 3. runda
                # #
                # #              "osi_gt_0475",
                # #              "osi_gt_0500",
                #
                #
                #              "osi_gt_046250_from_0",
                #              "osi_gt_04650_from_0",
                #              "osi_gt_04675_from_0_2",
                #
                #             "osi_gt_f70_04700_n_2"
                #
                #
                #          ]
                #      },

                "//home/josip/feap/FSG/automatizacija_36/OSI/lower/":
                    {"version": "new",

                     "simulations":
                         [

                                "osi_le_0250",
                                "osi_le_0275",
                                "osi_le_0300",
                                "osi_le_0325",
                                "osi_le_0350_2",
                         ]
                     },


                "//home/josip/feap/FSG/automatizacija_36/ECAP/GREATER/":
                    {"version": "new",

                     "simulations":
                         [
                            # "ecap_gt_145",
                            ###"ecap_gt_14625",    # ovo
                            ###"ecap_gt_14750",
                            ###"ecap_gt_14825",

                             "ecap_gt_14625_2",     # 2. runda
                             "ecap_gt_14750_2",     # 2. runda
                             "ecap_gt_14825_3",     # 2. runda

                             "ecap_gt_150",
                             "ecap_gt_150_2",       # 3. runda
                             "ecap_gt_155",
                             "ecap_gt_160",

                             "ecap_gt_150_from_0",

                         ]
                     },


                "//home/josip/feap/FSG/automatizacija_36/ECAP/lower/":
                    {"version": "new",

                     "simulations":
                         [
                             "ecap_le_065",
                             "ecap_le_070",
                             "ecap_le_075",
                             "ecap_le_080",
                         ]
                     },

          }

pickle_name_37 = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_37.pickle"
simulationsData_dict_37 = {

                "//home/josip/feap/FSG/automatizacija_36/TAWSS/":
                    {"version": "new",
                     "FSG_bool": True,

                     "simulations":
                         [
                            "tawss_le_030",
                            "tawss_le_035",
                            "tawss_le_040",
                            "tawss_le_045",
                             "tawss_le_0475",
                            "tawss_le_04825",
                            "tawss_le_050",
                          ]
                     },

                "//home/josip/feap/FSG/automatizacija_37/OSI/":
                    {"version": "new",
                     "FSG_bool": True,

                     "simulations":
                             [
                                # "osi_f70_gt_04700",
                                "osi_f0_gt_04650",
                                "osi_f0_gt_04625",
                                "osi_f0_gt_04600",
                                "osi_f0_gt_04575",
                                "osi_f0_gt_04550",

                             ]
                     },


                "//home/josip/feap/FSG/automatizacija_37/ECAP/":
                    {"version": "new",
                     "FSG_bool": True,

                     "simulations":
                             [
                                "ecap_f0_gt_150",
                                "ecap_f0_gt_151",
                                "ecap_f0_gt_152",
                                "ecap_f0_gt_153",
                                "ecap_f0_gt_154",
                                "ecap_f0_gt_155",
                                "ecap_f0_gt_156",
                                "ecap_f0_gt_157",
                                "ecap_f0_gt_158",
                                "ecap_f0_gt_159",
                                "ecap_f0_gt_160",
                             ]
                     },

                "//home/josip/feap/FSG/automatizacija_39/":
                    {"version": "new",
                     "FSG_bool": True,

                     "simulations":
                         [
                                "ECAP_154_turbulent_2",
                         ]
                     },


          }





pickle_name_38 = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_38.pickle"
simulationsData_dict_38 = {

                "//home/josip/feap/FSG/automatizacija_39/":
                    {"version": "new",
                     "FSG_bool": True,

                     "simulations":
                         [
                             "tawss_turbulent_Newt_5"
                         ]
                     },


                "//home/josip/feap/FSG/automatizacija_38/TAWSS/":
                    {"version": "new",
                     "FSG_bool": True,
                     "simulations":
                         [
                                "BC",
                                "casson",
                                "Newt_33",
                                "Newt_40_2",
                                "Newt_45",
                                "Newt_50_4",
                                "Newt_60_4",
                                "tawss=030",
                                "tawss=035",
                                "tawss=040",
                                "tawss=045",
                                "tawss=050",

                                 "a3=30",
                                 "a3=40",
                          ]
                     },

                "//home/josip/feap/FSG/automatizacija_38/noFSG/":
                    {"version": "new",
                     "FSG_bool": False,

                     "simulations":
                         [
                             "noFSG_12_3",
                             "noFSG_13_3",
                         ]
                     },



          }




pickle_name_usporedba_FSG = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_usporedba_FSG.pickle"
simulationsData_dict_usporedba_FSG = {

                "//home/josip/feap/FSG/automatizacija_38/TAWSS/":
                    {"version": "new",
                     "FSG_bool": True,

                     "simulations":
                         [
                                "casson",
                          ]
                     },

                    "//home/josip/feap/FSG/automatizacija_38/noFSG/":
                        {"version": "new",
                         "FSG_bool" : False,

                         "simulations":
                             [
                                 "noFSG_115",
                                 "noFSG_12",
                                 "noFSG_13",
                             ]
                         },
}



pickle_name_proba = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_proba.pickle"
simulationsData_dict_proba = {

                "/home/josip/feap/FSG/automatizacija_41/":
                    {"version": "new",
                     "FSG_bool": False,

                     "simulations":
                         [
                                "biochemo_3D",
                                "biochemo_1",
                          ]
                     },

                "//home/josip/feap/FSG/automatizacija_38/TAWSS/":
                    {"version": "new",
                     "FSG_bool": False,

                     "simulations":
                         [
                             "casson",
                         ]
                     },
}




pickle_name = pickle_name_proba
simulationsData_dict = simulationsData_dict_proba