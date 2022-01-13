import os, numpy, pandas

res_y0 = "//home/josip/feap/FSG/automatizacija_13/prava_Newt_5/res__Y0_field__89-5"

op = open(res_y0, "r")  # open txt file
cijeli_tekst = op.readlines()  # whole txt read in self.wholeDocument_eIW
nl_res_y = sum(1 for line in open(res_y0))  # number of lines in export Inner Wall


TSLlenght_res_Y0__field = 846
start_line = 140

timeStep = 2


nutarnja_linija = []

# for i in range(TSLlenght_res_Y0__field):
#     red = cijeli_tekst[i]
#     print(red)


print(cijeli_tekst[260].strip().split())



#     for n_line in range(TSLenght_res_Inner_lines - 1):
    #         r_inner = float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line].strip().split()[0])
