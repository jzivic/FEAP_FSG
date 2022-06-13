import os, math, itertools
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt


# input = "//home/josip/foamOpen/cases/FSG/NOVI_axial/usporedbaTolerancija/res__ILT_lines__89-5"
# simulacija = "//home/josip/foamOpen/cases/FSG/NOVI_axial/dizanjeTAWSS/prava1"

input = "/home/josip/feap/FSG/automatizacija_27/proba_1/res__ILT_lines__172-22"

simulacija = "//home/josip/feap/FSG/automatizacija_27/proba_1/probavanjemreze"


class Mesh:
    def __init__(self, rILTFile, nRel, nZel, grading, smooth=True, negTS=-1):
        self.rILTFile = rILTFile
        self.nRel = nRel            # broj radijalnih elemenata mreže
        self.nZel = nZel            # broj aksijalnih elemenata mreže
        self.negTS = negTS          # koji negativi korak se koristi
        self.grading = grading
        self.smooth = smooth
        self.PlaneList, self.Vertices = [], []

        self.read_rILT_Vertices()
        if self.smooth == False:
            self.no_smooth_process()
        elif smooth == True:
            self.smooth_process()

        self.MakeMesh()
        self.WriteMesh()
        self.Plot()


    # čitanje ILT dokumenta gdje su spremljene koordinate čvorova
    def read_rILT_Vertices(self):
        TSLenght = 121
        wholeDocument_rILT = open(self.rILTFile, "r").readlines()
        zadnjiKorak = wholeDocument_rILT[-(TSLenght + 1):-1]

        model_lenght = (float(zadnjiKorak[-1].strip().split()[3]) - float(zadnjiKorak[0].strip().split()[3]))
        # shift = (model_lenght - 150) / 2  # shift se dodaje jer je tako u feapu stl namješteno.
        shift = 0
        # Bitno je da prva i zadnja točka budu (-5,10) i (150, 10)

        self.r_list_org, self.z_list_org = [10], [-5]
        # self.r_list_org, self.z_list_org = [], []
        for self.n in range(len(zadnjiKorak)):
            red = wholeDocument_rILT[self.negTS * (TSLenght + 1): (self.negTS + 1) - 1][self.n].strip().split()
            r, z = float(red[0]), float(red[3]) - shift

            # if z > -5 and z < 150:
            self.r_list_org.append(float(r))
            self.z_list_org.append(float(z))

        self.r_list_org.append(10)
        self.z_list_org.append(model_lenght+5)


    # ako nije odabrano smooth, samo prolazi kroz koord i pravi plohe
    def no_smooth_process(self):
        angle = math.radians(2.5)
        for n in range(len(self.z_list_org)):
            r = self.r_list_org[n]
            z = self.z_list_org[n]

            t0 = [0,0, z]
            t1 = [r*math.cos(angle), -r*math.sin(angle), z]
            t2 = [r*math.cos(angle), +r*math.sin(angle), z]
            s_t0 = "\t"*3 + "(" + (" ".join([str(i) for i in t0])) + ")"  + "\n"
            s_t1 = "\t"*3 + "(" + (" ".join([str(i) for i in t1])) + ")"  + "\n"
            s_t2 = "\t"*3 + "(" + (" ".join([str(i) for i in t2])) + ")"  + "\n"
            self.Vertices.append(s_t0)
            self.Vertices.append(s_t1)
            self.Vertices.append(s_t2)
            Ploha = [s_t0, s_t1,s_t2]
            self.PlaneList.append(Ploha)


    # uglađuje krivulju aneurizme preko fit funkcije
    def smooth_process(self):
        self.rList = []
        r_zdravi = 10

        # razdvajanje lista na 3 dijela (žila-aaa-žila)
        r_1, r_2, r_3, z_1, z_2, z_3 = [], [], [], [], [], []

        # sve unutar udubljene točke vraća na razinu zdrave žile (10 mm)
        for n in range(len(self.r_list_org)):
            if self.r_list_org[n] < r_zdravi:
                self.r_list_org[n] = r_zdravi

        # traži prvu točku gdje žila prelazi u AAA
        n_start, n_end = None, None
        for n in range(len(self.z_list_org)):
            if self.r_list_org[n]-r_zdravi > 0.05*r_zdravi:
                n_start = n
                break
        # traži zadnju
        for n in reversed(range(len(self.z_list_org))):
            if self.r_list_org[n]-r_zdravi > 0.05*r_zdravi:
                n_end = n
                break


        if n_start == None:
            self.rList = self.r_list_org

        elif n_start != None:
            for n in range(len(self.z_list_org)):
                if n < n_start:
                    z_1.append(self.z_list_org[n])
                    r_1.append(self.r_list_org[n])
                elif n >= n_start and n <= n_end:
                    z_2.append(self.z_list_org[n])
                    r_2.append(self.r_list_org[n])
                elif n > n_end:
                    z_3.append(self.z_list_org[n])
                    r_3.append(self.r_list_org[n])

            coefs = poly.polyfit(z_2, r_2, 15)  # koef polinoma
            f_fit = poly.Polynomial(coefs)  # funkcija za fitanje
            r_2_fit = f_fit(np.array(z_2))  # fitan drugi dio

            rList_fit = list(itertools.chain(r_1, r_2_fit, r_3))
            self.rList = rList_fit






        angle = math.radians(2.5)
        # stvaranje vrhova i ploha za meširanje
        for n in range(len(self.z_list_org)):
            # r = rList_fit[n]
            r = self.rList[n]
            z = self.z_list_org[n]
            t0 = [0,0, z]
            t1 = [r*math.cos(angle), -r*math.sin(angle), z]
            t2 = [r*math.cos(angle), +r*math.sin(angle), z]
            s_t0 = "\t"*3 + "(" + (" ".join([str(i) for i in t0])) + ")"  + "\n"
            s_t1 = "\t"*3 + "(" + (" ".join([str(i) for i in t1])) + ")"  + "\n"
            s_t2 = "\t"*3 + "(" + (" ".join([str(i) for i in t2])) + ")"  + "\n"
            self.Vertices.append(s_t0)
            self.Vertices.append(s_t1)
            self.Vertices.append(s_t2)
            Ploha = [s_t0, s_t1,s_t2]
            self.PlaneList.append(Ploha)


    def MakeMesh(self):
        #Faces
        ulaz = [3*(len(self.PlaneList)-1)+0, 3*(len(self.PlaneList)-1)+1, 3*(len(self.PlaneList)-1)+2, 3*(len(self.PlaneList)-1)+0]
        izlaz = [0,2,1,0]

        self.UlazString = ("\t"*3 + "(" + " ".join([str(i) for i in ulaz])+")\n")
        self.IzlazString = ("\t"*3 + "(" + " ".join([str(i) for i in izlaz])+")\n")

        self.BlockStrings = []
        hexRed_0 = "hex () ("+str(self.nRel)+" 1 " +str(self.nZel) + ") simpleGrading ("+str(self.grading)+" 1 1)"
        self.OsiStrings = []
        self.DStraneString = []
        self.LStraneString = []
        self.AneurizmeString = []

        for nPloha in range(len(self.PlaneList)-1):
            ST = 3*nPloha                            #Startna Točka
            blok = [ST+0, ST+1, ST+2, ST+0, ST+3, ST+4, ST+5, ST+3]
            s = [str(i) for i in blok]
            zapis = (" ".join(s))
            cijeliRed = "\t"+hexRed_0[0:5] + zapis + hexRed_0[5:]+"\n"
            self.BlockStrings.append(cijeliRed)

            os = [ST, ST+3, ST+3, ST]               #Faces
            desna = [ST, ST+1, ST+4, ST+3]
            lijeva = [ST, ST+3, ST+5, ST+2]
            aneurizma = [ST+1, ST+2, ST+5, ST+4]

            s_osi = [str(i) for i in os]
            cijeliRed_osi  = "\t"*3 + "("+ " ".join(s_osi)+ ")\n"
            self.OsiStrings.append(cijeliRed_osi)

            s_DStrane = [str(i) for i in desna]
            cijeliRed_DStrane  = "\t"*3 + "("+ " ".join(s_DStrane)+ ")\n"
            self.DStraneString.append(cijeliRed_DStrane)

            s_LStrane = [str(i) for i in lijeva]
            cijeliRed_LStrane  = "\t"*3 + "("+ " ".join(s_LStrane)+ ")\n"
            self.LStraneString.append(cijeliRed_LStrane)

            s_Aneurizme = [str(i) for i in aneurizma]
            cijeliRed_Aneurizme  = "\t"*3 + "("+ " ".join(s_Aneurizme)+ ")\n"
            self.AneurizmeString.append(cijeliRed_Aneurizme)


    def WriteMesh(self):
        blockMeshDoc = open("blockMeshDict_pre", "r")
        listOfLines = blockMeshDoc.readlines()

        for nRed in range(len(listOfLines)):            #ide kroz cijeli blockMesh_pre_0
            red = listOfLines[nRed].strip()

            if red == "vertices":
                for n in range(len(self.Vertices)):
                    listOfLines.insert(nRed+2+n, self.Vertices[n])
            if red=="blocks":                           #popunjavanje Blocks-a
                for n in range(len(self.BlockStrings)):
                    listOfLines.insert(nRed+2+n, self.BlockStrings[n])

            if red=="ulaz":
                listOfLines.insert(nRed + 5 , self.UlazString)
            if red=="izlaz":
                listOfLines.insert(nRed + 5, self.IzlazString)

            if red == "os":
                for n in range(len(self.OsiStrings)):
                    listOfLines.insert(nRed+5+n, self.OsiStrings[n])

            if red == "strana_d":
                for n in range(len(self.DStraneString)):
                    listOfLines.insert(nRed+5+n, self.DStraneString[n])

            if red == "strana_l":
                for n in range(len(self.LStraneString)):
                    listOfLines.insert(nRed+5+n, self.LStraneString[n])

            if red == "aneurizma":
                for n in range(len(self.AneurizmeString)):
                    listOfLines.insert(nRed+5+n, self.AneurizmeString[n])

        output = simulacija + "/system/blockMeshDict"
        p = open(output, "w")
        p.writelines(listOfLines)
        p.close()

    def Plot(self):

        fig = plt.gcf()
        plt.plot(self.z_list_org, self.r_list_org, label="org")
        if self.smooth == True:
            plt.plot(self.z_list_org, self.rList, label="smooth")
        plt.grid(color='k', linestyle=':', linewidth=0.5)

        plt.xlabel("z")
        plt.ylabel("r")
        plt.legend()
        plt.draw()
        fig.savefig('radijus.png', dpi=300)
        plt.close()

        # plt.show()

# Mesh(input, nRel=2, nZel=1, grading=1, smooth=True, negTS=-1)


Mesh(input, nRel=30, nZel=1, grading=0.2, smooth=False, negTS=-1)











# a_file = open("stari", "r")
# list_of_lines = a_file.readlines()
#
# for n in range(len(list_of_lines)):
#     red = list_of_lines[n].strip()
#
#     if red == "ona":
#         list_of_lines[n] = "ovo je izmjenjeni red\n"
#
#         list_of_lines.insert(n, "A\n")

# stari = open("novi", "w")
# stari.writelines(list_of_lines)
# stari.close()



















