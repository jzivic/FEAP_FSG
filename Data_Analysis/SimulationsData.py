chosen_TimeSteps = [i for i in range(1,666)]        # mora od 1 od nekog broja!!


# x = 97
# chosen_TimeSteps = [i for i in range(x,x+10)]

barcelona = False





# barcelona = False
# results_directory = "//home/josip/feap/FSG/automatizacija_25/"
# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_25.pickle"
# simulation_names = [
        # "a3=30",
        # "a3=40",
        # "ac=16",
        # "ac=25",
        # "ae=1",
        # "ae=4",
        # "ab=100",
        # "ab=900",
        #
        # "tawss=020",
        # "tawss=025",
        # "tawss=030",
        # "tawss=035",
        # "tawss=040",
        # "tawss=045",
        # "tawss=050",

        # "BC",
        # "Casson",
        # "Newt_5",
        # "Newt_6",
        # "Newt_33",
        #
        #
        # "turb_Newt_3",
        # "turbulent_Newt_3",
        # "turbulent_Newt_5",
        # "turbulent_Newt_6",
        # "turbulent_Casson",
        #
        #
        #
        # "debljina_010",
        # "debljina_015",
        # "debljina_020",
        # "debljina_025",
        #
        # "i4=102",
        # "i4=108",
        # "i4=114",
        # "i4=120",
        # "i4=126",
        # "i4=132",
        #
        # "stari_case_provjera_pocetak_2",
        #
        #
        #
        # "no_ILT",

# ]




# barcelona = False
# results_directory = "//home/josip/feap/FSG/automatizacija_26/"
# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_26.pickle"
# simulation_names = [
#
#                 "stiffness_low",
#                 "stiffness_low_01",
#                 "stiffness_low_05",
#                 "stiffness_low_10",
#                 "stiffness_low_25",
#                 "stiffness_low_50",
#                 "stiffness_low_75",
#                 "stifness_normal",
#
# ]



# barcelona = False
# results_directory = "//home/josip/feap/FSG/automatizacija_29/"
# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_26.pickle"
# simulation_names = [
#
#     "a3=30",
#     "a3=40",
#     "ac=16",
#     "ac=25",
#     "ae=1",
#     "ae=4",
#     "flow_laminar_BC",
#     "flow_laminar_Casson",
#     "flow_laminar_Newt_3",
#     "flow_laminar_Newt_5",
#     "flow_laminar_Newt_6",
#     "flow_turbulent_BC",
#     "flow_turbulent_Casson",
#     "flow_turbulent_Newt_3",
#     "flow_turbulent_Newt_5",
#     "flow_turbulent_Newt_6",
#     "tawss_025",
#     "tawss_030",
#     "tawss_035",
#     "tawss_040",
#     "tawss_045",
#     "tawss_050",
#
# ]






# barcelona = False
# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_33.pickle"
#
# results_directory = "//home/josip/feap/FSG/automatizacija_33/radial/"
# simulation_names = [
#
#                "radial_a3_30",
#                "radial_a3_40",
#                "radial_tawss_35_d02",
#                "radial_tawss_40_d01",
#                "radial_tawss_40_d02",
#                "radial_tawss_45_d02",
#
# ]




# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_33.pickle"
# simulationsData_dict = {
#                 "//home/josip/feap/FSG/automatizacija_33/radial/":
#                 ["radial_a3_30",
#                 "radial_a3_40",
#                 "radial_tawss_35_d02",
#                 "radial_tawss_40_d01",
#                 "radial_tawss_40_d02",
#                 "radial_tawss_45_d02"],




# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_25_novo.pickle"
# simulationsData_dict = {
#                 "//home/josip/feap/FSG/automatizacija_25/":
#                 [
#                     "a3_30",
#                     "a3_40",
#                     "ac_16",],
#           }



pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/auto_FSG_usporedba.pickle"
simulationsData_dict = {

                "//home/josip/feap/FSG/automatizacija_25/":
                    {"version": "old",

                     "simulations":
                         ["a3_30",
                          "a3_40",
                          "Casson"]
                     },



                "//home/josip/feap/FSG/automatizacija_33/NO_biochemo_FSG/x3_2/":
                {"version": "new",

                 "simulations":
                     ["x3_2_a3_20",
                      "x3_2_a3_30",
                      "x3_2_a3_40"]
                },


                "//home/josip/feap/FSG/automatizacija_33/NO_biochemo_FSG/x3_3/":
                    {"version": "new",

                     "simulations":
                         ["x3_3_a3_20",
                          "x3_3_a3_30",
                          "x3_3_a3_40"]
                     },

          }



# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_biochemo.pickle"
# simulationsData_dict = {
                #
                # "//home/josip/feap/FSG/automatizacija_33/3D/":
                # {"version": "new",
                #
                #  "simulations":
                #    [
                #    "3D_a3_30",
                #     "3D_a3_40",
                #     "3D_tawss_35_d_02",
                #     "3D_tawss_40_d_01",
                #     "3D_tawss_40_d_02",
                #     "3D_tawss_45_d_02",
                #
                #     ]
                # },



          #       "//home/josip/feap/FSG/automatizacija_33/radial/":
          #       {"version": "new",
          #
          #        "simulations":
          #            [
          #                "radial_a3_30",      #__b označava begin, odnosno da nema restart opcije
          #                "radial_a3_40",
          #                "radial_tawss_35_d02",
          #                "radial_tawss_40_d01",
          #                "radial_tawss_40_d02",
          #                "radial_tawss_45_d02",
          #            ]
          #        },
          #
          #       "//home/josip/feap/FSG/automatizacija_25/":
          #           {"version"  :  "old",
          #
          #            "simulations":
          #               [
          #                "a3_30",
          #                "a3_40",
          #                "Casson",
          #               ]
          #            },
          #
          #
          #       "//home/josip/feap/FSG/automatizacija_33/3D/":
          #           {"version": "new",
          #
          #            "simulations":
          #                [
          #                    "standard_3D",
          #                    # "a3_40",
          #                    # "Casson",
          #                ]
          #            }
          #
          #
          #
          #
          # }


pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_25.pickle"
simulationsData_dict = {

                "//home/josip/feap/FSG/automatizacija_25/":
                    {"version": "old",

                     "simulations":
                         [
                             # "debljina_010",
                             # "debljina_015",
                             # "debljina_020",
                             # "debljina_025",

                            "i4=102",
                            "i4=108",
                            "i4=114",
                            "i4=120",
                            "i4=126",
                            "i4=132",

                          ]
                     },


                "//home/josip/feap/FSG/automatizacija_33_N_AVERAGE!!/NO_biochemo_FSG/x3_2/":
                    {"version": "new",

                     "simulations":
                         [
                            "x3_2_a3_20_novo",
                            # "x3_2_a3_20",
                          ]
                     },


          }




# pickle_name = "//home/josip/PycharmProjects/FEAP_FSG/automatizacija_avg_vs_NOavg.pickle"
# simulationsData_dict = {
#
#                 "//home/josip/feap/FSG/automatizacija_33_N_AVERAGE!!/NO_biochemo_FSG/x3_2/":
#                     {"version": "new",
#
#                      "simulations":
#                          [
#                             "x3_2_a3_20_novo",
#                             "x3_2_a3_20",
#                           ]
#                      },
#           }