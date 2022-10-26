"""
ovo je file koji služi za kopiranje wssMag > TAWSS filea u jednom folderu autmatksi
dodaje i OSI I ECAP čisto da čitanje bude moguće.
"""


import shutil




simulacija_number = 53
moments = [1.25, 1.3, 1.5]


case = "//home/josip/feap/FSG/automatizacija_38/TAWSS/Newt_50_4/simulacija"+str(simulacija_number)+"/"

koordinate_file = "//home/josip/feap/FSG/automatizacija_38/TAWSS/Newt_50_4/simulacija" + \
                  str(simulacija_number) + "/2/koordinate"



for moment in moments:

    koordinate_new = case + str(moment)+"/koordinate"
    shutil.copy(koordinate_file, koordinate_new)


    wssMag_file = case + str(moment) + "/" + "wssMag"

    TAWSS_file = case + str(moment) + "/" + "TAWSS"
    OSI_file = case + str(moment) + "/" + "OSI"
    ECAP_file = case + str(moment) + "/" + "ECAP"


    shutil.copy(wssMag_file, TAWSS_file)
    shutil.copy(wssMag_file, OSI_file)
    shutil.copy(wssMag_file, ECAP_file)

    wssMag_file = case + "/wssMag"

    TAWSS = case + "/TAWSS"
    OSI = case + "/OSI"
    ECAP = case + "/TAWSS"




from average_parameters import *





