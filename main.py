import os, numpy, pandas

res_y0 = "//home/josip/feap/FSG/automatizacija_13/prava_Newt_5/res__Y0_field__89-5"

op = open(res_y0, "r")  # open txt file
cijeli_tekst = op.readlines()  # whole txt read in self.wholeDocument_eIW
nl_res_y = sum(1 for line in open(res_y0))  # number of lines in export Inner Wall


TSLlenght_res_Y0__field = 850
start_line = 137

timeStep =




for i in range(137, nl_res_y, 850):
    red = cijeli_tekst[i]
    print(red)







    #     for n_line in range(TSLenght_res_Inner_lines - 1):
    #         r_inner = float(self.whole_document_Inner_lines[self.startLine_res_Inner_lines + n_line].strip().split()[0])
