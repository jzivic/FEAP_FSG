chosen_TimeSteps = [i for i in range(1,666)]        # mora od 1 od nekog broja!!


x = 100
# chosen_TimeSteps = [i for i in range(x,x+1)]

barcelona = False






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

                # "//home/josip/feap/FSG/automatizacija_25/":
                #     {"version": "old",
                #
                #      "simulations":
                #          [
                #             "a3_30",
                #             "a3_40",
                #             "ab=900",
                #             "BC",
                #             "Casson",
                #
                #
                #             "Newt_5",
                #             "Newt_6",
                #             "Newt_33",
                #
                #             "tawss=030",
                #             "tawss=035",
                #             "tawss=040",
                #             "tawss=045",
                #             "tawss=050",
                #
                #                         ]
                #      },


                "//home/josip/feap/FSG/automatizacija_35/":
                    {"version": "new",

                     "simulations":
                         [
                            # "osi_le_035_3",
                            # "osi_le_030_3",
                            # "osi_le_025_3",
                            # "osi_le_020_3",

                            # "osi_gt_55",
                            # "osi_gt_050",
                            # "osi_gt_045",
                            # "osi_gt_40",

                            # "ecap_le_060",
                            # "ecap_le_055",
                            "ecap_le_050",
                                                ]
                     },


          }


