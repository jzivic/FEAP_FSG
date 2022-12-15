# Class for NODE file objects


class ReadNodeFile():
    # On initialization read files and save data
    def __init__(self, file_path_rin, file_path_rout):
        # Initialize class attributes
        self.file_path_rin = file_path_rin
        self.file_path_rout = file_path_rout
        self.timestep = []
        self.time = []
        self.radius_rin = []
        self.radius_rout = []
        self.growth_rate_rin = []
        self.growth_rate_rout = []
        self.wall_thickness = []
        self.file_steps = 0

        # Read file for inner node
        try:
            with open(self.file_path_rin, "r") as file_rin:
                lines = file_rin.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_rin)
            print(msg)

        # Save data for inner node
        for line in range(5, len(lines)):
            data = lines[line].split()
            self.timestep.append(int(data[0]))
            self.time.append(float(data[1]))
            self.radius_rin.append(float(data[2]))
            self.growth_rate_rin.append(float(data[3]))
        self.file_steps = len(lines) - 5

        # Read file for outer node
        read_out = False
        try:
            with open(self.file_path_rout, "r") as file_rout:
                lines = file_rout.readlines()
            read_out = True
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_rout)
            print(msg)
            print("Values for outer node set to zero.")

        # Save data for outer node and calculate wall thickness
        if read_out:
            i = 0
            for line in range(5, len(lines)):
                data = lines[line].split()
                rout = float(data[2])
                self.radius_rout.append(rout)
                self.growth_rate_rout.append(float(data[3]))
                self.wall_thickness.append(rout - self.radius_rin[i])
                i += 1
        else:
            for line in range(5, len(lines)):
                self.radius_rout.append(0.0)
                self.growth_rate_rout.append(0.0)
                self.wall_thickness.append(0.0)



    # Print data for given line
    def print_line(self, l):
        print("Results file: ",self.file_path_rin)
        print("    timestep        time         rin        rout       thick      grrtin     grrtout")
        print("    --------------------------------------------------------------------------------")
        print("{0:12d}{1:12.1f}{2:12.4f}{3:12.4f}{4:12.4f}{5:12.6f}{6:12.6f}".format(self.timestep[l],
                        self.time[l], self.radius_rin[l], self.radius_rout[l], self.wall_thickness[l],
                        self.growth_rate_rin[l], self.growth_rate_rout[l]),"\n")

# ======================================================================================================================

# Class for NODE file objects - extended version of NODE file


class ReadNodeFile2():
    # On initialization read files and save data
    def __init__(self, file_path_rin, file_path_rout):
        # Initialize class attributes
        self.file_path_rin = file_path_rin
        self.file_path_rout = file_path_rout
        self.timestep = []
        self.time = []
        self.radius_rin = []
        self.radius_rout = []
        self.growth_rate_rin = []
        self.growth_rate_rout = []
        self.S11in = []
        self.S22in = []
        self.S33in = []
        self.S11out = []
        self.S22out = []
        self.S33out = []
        self.wall_thickness = []
        self.file_steps = 0

        # Read file for inner node
        try:
            with open(self.file_path_rin, "r") as file_rin:
                lines = file_rin.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_rin)
            print(msg)

        # Save data for inner node
        for line in range(5, len(lines)):
            data = lines[line].split()
            self.timestep.append(int(data[0]))
            self.time.append(float(data[1]))
            self.radius_rin.append(float(data[2]))
            self.growth_rate_rin.append(float(data[3]))
            self.S11in.append(float(data[4]))
            self.S22in.append(float(data[5]))
            self.S33in.append(float(data[6]))
        self.file_steps = len(lines) - 5

        # Read file for outer node
        read_out = False
        try:
            with open(self.file_path_rout, "r") as file_rout:
                lines = file_rout.readlines()
            read_out = True
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_rout)
            print(msg)
            print("Values for outer node set to zero.")

        # Save data for outer node and calculate wall thickness
        if read_out:
            i = 0
            for line in range(5, len(lines)):
                data = lines[line].split()
                rout = float(data[2])
                self.radius_rout.append(rout)
                self.growth_rate_rout.append(float(data[3]))
                self.S11out.append(float(data[4]))
                self.S22out.append(float(data[5]))
                self.S33out.append(float(data[6]))
                self.wall_thickness.append(rout - self.radius_rin[i])
                i += 1
        else:
            for line in range(5, len(lines)):
                self.radius_rout.append(0.0)
                self.growth_rate_rout.append(0.0)
                self.wall_thickness.append(0.0)
                self.S11out.append(0.0)
                self.S22out.append(0.0)
                self.S33out.append(0.0)


    # Print data for given line
    def print_line(self, l):
        print("Results file: ",self.file_path_rin)
        print("    timestep        time         rin        rout       thick      grrtin     grrtout"
              "         S11in         S22in         S33in        S11out        S22out        S33out")
        print("    --------------------------------------------------------------------------------"
              "------------------------------------------------------------------------------------")
        print("{0:12d}{1:12.1f}{2:12.4f}{3:12.4f}{4:12.4f}{5:12.6f}{6:12.6f}{7:14.4e}{8:14.4e}{9:14.4e}"
              "{10:14.4e}{11:14.4e}{12:14.4e}".format(self.timestep[l],self.time[l], self.radius_rin[l],
                self.radius_rout[l], self.wall_thickness[l],self.growth_rate_rin[l], self.growth_rate_rout[l],
                self.S11in[l],self.S22in[l],self.S33in[l],self.S11out[l],self.S22out[l],self.S33out[l]),"\n")


# ======================================================================================================================


class ReadOldNodeFile():
    # On initialization read files and save data
    def __init__(self, file_path_rin, file_path_rout):
        # Initialize class attributes
        self.file_path_rin = file_path_rin
        self.file_path_rout = file_path_rout
        self.timestep = []
        self.time = []
        self.radius_rin = []
        self.radius_rout = []
        self.growth_rate_rin = []
        self.growth_rate_rout = []
        self.wall_thickness = []
        self.file_steps = 0

        # Read file for inner node
        try:
            with open(self.file_path_rin, "r") as file_rin:
                lines = file_rin.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_rin)
            print(msg)

        # Save data for inner node
        for line in range(5, len(lines)):
            data = lines[line].split()
            self.timestep.append(int(data[0]))
            self.time.append(float(data[1]))
            self.radius_rin.append(float(data[2]))
            self.growth_rate_rin.append(float(data[3]))
        self.file_steps = len(lines) - 5

        # Read file for outer node
        read_out = False
        try:
            with open(self.file_path_rout, "r") as file_rout:
                lines = file_rout.readlines()
            read_out = True
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_rout)
            print(msg)
            print("Values for outer node set to zero.")

        # Save data for outer node and calculate wall thickness
        if read_out:
            i = 0
            for line in range(5, len(lines)):
                data = lines[line].split()
                rout = float(data[2])
                self.radius_rout.append(rout)
                self.growth_rate_rout.append(float(data[3]))
                self.wall_thickness.append(rout - self.radius_rin[i])
                i += 1
        else:
            for line in range(5, len(lines)):
                self.radius_rout.append(0.0)
                self.growth_rate_rout.append(0.0)
                self.wall_thickness.append(0.0)


    # Print data for given line
    def print_line(self, l):
        print("Results file: ",self.file_path_rin)
        print("    timestep        time         rin        rout       thick      grrtin     grrtout"
              "         S11in         S22in         S33in        S11out        S22out        S33out")
        print("    --------------------------------------------------------------------------------"
              "------------------------------------------------------------------------------------")
        print("{0:12d}{1:12.1f}{2:12.4f}{3:12.4f}{4:12.4f}{5:12.6f}{6:12.6f}".format(self.timestep[l],self.time[l],
                self.radius_rin[l],self.radius_rout[l], self.wall_thickness[l],self.growth_rate_rin[l],
                self.growth_rate_rout[l],"\n"))

# ======================================================================================================================

# Class for MIDDLE_line file objects


class ReadMiddleFile():
    # On initialization read files and save data
    def __init__(self, file_path):
        # Initialize class attributes
        self.file_path = file_path
        self.node = []
        self.x = []
        self.ux = []
        self.S11 = []
        self.S22 = []
        self.S33 = []

        # Read file for inner node
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path)
            print(msg)

        # Save data from middle file
        list_node = []
        list_x = []
        list_ux = []
        list_S11 = []
        list_S22 = []
        list_S33 = []
        for line in range(7, len(lines)):
            data = lines[line].split()
            if not data:
                pass
            elif data[0] == '--------------------------------------------------------------------------':
                self.node.append([])
                self.x.append([])
                self.ux.append([])
                self.S11.append([])
                self.S22.append([])
                self.S33.append([])
                for i in range(len(list_node)):
                    self.node[-1].append(list_node[i])
                    self.x[-1].append(list_x[i])
                    self.ux[-1].append(list_ux[i])
                    self.S11[-1].append(list_S11[i])
                    self.S22[-1].append(list_S22[i])
                    self.S33[-1].append(list_S33[i])
                list_node.clear()
                list_x.clear()
                list_ux.clear()
                list_S11.clear()
                list_S22.clear()
                list_S33.clear()
            else:
                list_node.append(int(data[0]))
                list_x.append(float(data[1]))
                list_ux.append(float(data[2]))
                list_S11.append(float(data[3]))
                list_S22.append(float(data[4]))
                list_S33.append(float(data[5]))


    # Print data for given timestep
    def print_timestep(self, l):
        print("Results file: ",self.file_path)
        print(f"Timestep = {l}")
        print("        NODE           x          ux         S11         S22         S33 ")
        print("                    [mm]        [mm]       [MPa]       [MPa]       [MPa] ")
        print("      --------------------------------------------------------------------")
        n = len(self.node[l])
        for i in range(n):
            print("{0:12d}{1:12.2f}{2:12.4f}{3:12.4f}{4:12.4f}{5:12.4f}".format(self.node[l][i],
                self.x[l][i], self.ux[l][i], self.S11[l][i], self.S22[l][i], self.S33[l][i]))


# ======================================================================================================================

# Class for contour files objects (INNER, OUTER, ILT lines)


class ReadContourFiles():
    # On initialization read files and save data
    def __init__(self, file_path_inn, file_path_out, file_path_ilt):
        # Initialize class attributes
        self.file_path_inn = file_path_inn
        self.file_path_out = file_path_out
        self.file_path_ilt = file_path_ilt
        self.R_line1_inn = []
        self.R_line2_inn = []
        self.R_line3_inn = []
        self.R_line1_out = []
        self.R_line2_out = []
        self.R_line3_out = []
        self.R_line1_ilt = []
        self.R_line2_ilt = []
        self.R_line3_ilt = []
        self.z_line1_inn = []
        self.z_line2_inn = []
        self.z_line3_inn = []
        self.z_line1_out = []
        self.z_line2_out = []
        self.z_line3_out = []
        self.z_line1_ilt = []
        self.z_line2_ilt = []
        self.z_line3_ilt = []

        # Read INNER_lines file
        try:
            with open(self.file_path_inn, "r") as file:
                lines_inn = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_inn)
            print(msg)

        # Read OUTER_lines file
        try:
            with open(self.file_path_out, "r") as file:
                lines_out = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_out)
            print(msg)

        # Read ILT_lines file
        try:
            with open(self.file_path_ilt, "r") as file:
                lines_ilt = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_ilt)
            print(msg)

        # Save data from INNER_lines file
        list_R_line1 = []
        list_R_line2 = []
        list_R_line3 = []
        list_z_line1 = []
        list_z_line2 = []
        list_z_line3 = []
        for line in range(5, len(lines_inn)):
            data = lines_inn[line].split()
            if not data:
                self.R_line1_inn.append([])
                self.R_line2_inn.append([])
                self.R_line3_inn.append([])
                self.z_line1_inn.append([])
                self.z_line2_inn.append([])
                self.z_line3_inn.append([])
                for i in range(len(list_R_line1)):
                    self.R_line1_inn[-1].append(list_R_line1[i])
                    self.R_line2_inn[-1].append(list_R_line2[i])
                    self.R_line3_inn[-1].append(list_R_line3[i])
                    self.z_line1_inn[-1].append(list_z_line1[i])
                    self.z_line2_inn[-1].append(list_z_line2[i])
                    self.z_line3_inn[-1].append(list_z_line3[i])
                list_R_line1.clear()
                list_R_line2.clear()
                list_R_line3.clear()
                list_z_line1.clear()
                list_z_line2.clear()
                list_z_line3.clear()
            else:
                list_R_line1.append(float(data[0]))
                list_R_line2.append(float(data[1]))
                list_R_line3.append(float(data[2]))
                list_z_line1.append(float(data[3]))
                list_z_line2.append(float(data[4]))
                list_z_line3.append(float(data[5]))

        # Save data from OUTER_lines file
        list_R_line1.clear()
        list_R_line2.clear()
        list_R_line3.clear()
        list_z_line1.clear()
        list_z_line2.clear()
        list_z_line3.clear()
        for line in range(5, len(lines_out)):
            data = lines_out[line].split()
            if not data:
                self.R_line1_out.append([])
                self.R_line2_out.append([])
                self.R_line3_out.append([])
                self.z_line1_out.append([])
                self.z_line2_out.append([])
                self.z_line3_out.append([])
                for i in range(len(list_R_line1)):
                    self.R_line1_out[-1].append(list_R_line1[i])
                    self.R_line2_out[-1].append(list_R_line2[i])
                    self.R_line3_out[-1].append(list_R_line3[i])
                    self.z_line1_out[-1].append(list_z_line1[i])
                    self.z_line2_out[-1].append(list_z_line2[i])
                    self.z_line3_out[-1].append(list_z_line3[i])
                list_R_line1.clear()
                list_R_line2.clear()
                list_R_line3.clear()
                list_z_line1.clear()
                list_z_line2.clear()
                list_z_line3.clear()
            else:
                list_R_line1.append(float(data[0]))
                list_R_line2.append(float(data[1]))
                list_R_line3.append(float(data[2]))
                list_z_line1.append(float(data[3]))
                list_z_line2.append(float(data[4]))
                list_z_line3.append(float(data[5]))

        # Save data from ILT_lines file
        list_R_line1.clear()
        list_R_line2.clear()
        list_R_line3.clear()
        list_z_line1.clear()
        list_z_line2.clear()
        list_z_line3.clear()
        for line in range(5, len(lines_ilt)):
            data = lines_ilt[line].split()
            if not data:
                self.R_line1_ilt.append([])
                self.R_line2_ilt.append([])
                self.R_line3_ilt.append([])
                self.z_line1_ilt.append([])
                self.z_line2_ilt.append([])
                self.z_line3_ilt.append([])
                for i in range(len(list_R_line1)):
                    self.R_line1_ilt[-1].append(list_R_line1[i])
                    self.R_line2_ilt[-1].append(list_R_line2[i])
                    self.R_line3_ilt[-1].append(list_R_line3[i])
                    self.z_line1_ilt[-1].append(list_z_line1[i])
                    self.z_line2_ilt[-1].append(list_z_line2[i])
                    self.z_line3_ilt[-1].append(list_z_line3[i])
                list_R_line1.clear()
                list_R_line2.clear()
                list_R_line3.clear()
                list_z_line1.clear()
                list_z_line2.clear()
                list_z_line3.clear()
            else:
                list_R_line1.append(float(data[0]))
                list_R_line2.append(float(data[1]))
                list_R_line3.append(float(data[2]))
                list_z_line1.append(float(data[3]))
                list_z_line2.append(float(data[4]))
                list_z_line3.append(float(data[5]))


    # Print data for given timestep
    def print_timestep(self, l):
        print("Results file inn: ", self.file_path_inn)
        print("Results file out: ", self.file_path_out)
        print("Results file ilt: ", self.file_path_ilt)
        print(f"Timestep = {l}")
        print("       R_ilt       R_inn       R_out       z_ilt       z_inn       z_out ")
        print("        [mm]        [mm]        [mm]        [mm]        [mm]        [mm] ")
        print("      --------------------------------------------------------------------")
        for i in range(len(self.R_line1_inn[l])):
            print("{0:12.4f}{1:12.4f}{2:12.4f}{3:12.4f}{4:12.4f}{5:12.4f}".format(self.R_line1_ilt[l][i],
                self.R_line1_inn[l][i], self.R_line1_out[l][i], self.z_line1_ilt[l][i],
                self.z_line1_inn[l][i], self.z_line1_out[l][i]))


# ======================================================================================================================

# Class for STRESS_line file objects


class ReadStressFile():
    # On initialization read files and save data
    def __init__(self, file_path):
        # Initialize class attributes
        self.file_path = file_path
        self.node = []
        self.x = []
        self.ux = []
        self.S11 = []
        self.S22 = []
        self.S33 = []

        # Read file for inner node
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path)
            print(msg)

        # Save data from middle file
        list_node = []
        list_x = []
        list_ux = []
        list_S11 = []
        list_S22 = []
        list_S33 = []
        for line in range(5, len(lines)):
            data = lines[line].split()
            if not data:
                self.node.append([])
                self.x.append([])
                self.ux.append([])
                self.S11.append([])
                self.S22.append([])
                self.S33.append([])
                for i in range(len(list_node)):
                    self.node[-1].append(list_node[i])
                    self.x[-1].append(list_x[i])
                    self.ux[-1].append(list_ux[i])
                    self.S11[-1].append(list_S11[i])
                    self.S22[-1].append(list_S22[i])
                    self.S33[-1].append(list_S33[i])
                list_node.clear()
                list_x.clear()
                list_ux.clear()
                list_S11.clear()
                list_S22.clear()
                list_S33.clear()
            else:
                list_node.append(int(data[0]))
                list_x.append(float(data[4]))
                list_ux.append(float(data[5]))
                list_S11.append(float(data[1]))
                list_S22.append(float(data[2]))
                list_S33.append(float(data[3]))


    # Print data for given timestep
    def print_timestep(self, l):
        print("Results file: ",self.file_path)
        print(f"Timestep = {l}")
        print("        NODE           x          ux         S11         S22         S33 ")
        print("                    [mm]        [mm]       [MPa]       [MPa]       [MPa] ")
        print("      --------------------------------------------------------------------")
        n = len(self.node[l])
        for i in range(n):
            print("{0:12d}{1:12.2f}{2:12.4f}{3:12.4f}{4:12.4f}{5:12.4f}".format(self.node[l][i],
                self.x[l][i], self.ux[l][i], self.S11[l][i], self.S22[l][i], self.S33[l][i]))


# ======================================================================================================================

# Class for INNER contour files objects


class CalculateFusiformAAALengthFromInnerContour():
    # On initialization read files and save data
    def __init__(self, file_path_inn,neck_relative_radius):
        # Initialize class attributes
        self.file_path_inn = file_path_inn
        self.neck_relative_radius = neck_relative_radius
        self.R_line1_inn = []
        self.z_line1_inn = []
        self.AAA_length = []

        # Read INNER_lines file
        try:
            with open(self.file_path_inn, "r") as file:
                lines_inn = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_inn)
            print(msg)

        # Save data from INNER_lines file
        list_R_line1 = []
        list_z_line1 = []
        for line in range(5, len(lines_inn)):
            data = lines_inn[line].split()
            if not data:
                self.R_line1_inn.append([])
                self.z_line1_inn.append([])
                for i in range(len(list_R_line1)):
                    self.R_line1_inn[-1].append(list_R_line1[i])
                    self.z_line1_inn[-1].append(list_z_line1[i])
                list_R_line1.clear()
                list_z_line1.clear()
            else:
                list_R_line1.append(float(data[0]))
                list_z_line1.append(float(data[3]))

        # Determine position of AAA necks and calculate distance between them
        for timestep in range(0,len(self.R_line1_inn)):
            bottom_neck_z = 0
            top_neck_z = 0
            list_R = self.R_line1_inn[timestep]
            list_z = self.z_line1_inn[timestep]
            normal_R = list_R[0]
            neck_R = neck_relative_radius * normal_R
            length_zero = True
            for point in range(len(list_R)):
                if list_R[point] >= neck_R:
                    length_zero = False
                    break
            if length_zero:
                length = 0.0
            else:
                bottom_neck_z1 = 0.0
                bottom_neck_z2 = 0.0
                bottom_neck_r1 = 0.0
                bottom_neck_r2 = 0.0
                top_neck_z1 = 0.0
                top_neck_z2 = 0.0
                top_neck_r1 = 0.0
                top_neck_r2 = 0.0
                for point in range(len(list_R)):
                    if list_R[point] >= neck_R:
                        bottom_neck_z1 = list_z[point-1]
                        bottom_neck_z2 = list_z[point]
                        bottom_neck_r1 = list_R[point-1]
                        bottom_neck_r2 = list_R[point]
                        break
                for point in range(len(list_R)-1,0,-1):
                    if list_R[point] >= neck_R:
                        top_neck_z1 = list_z[point]
                        top_neck_z2 = list_z[point-1]
                        top_neck_r1 = list_R[point]
                        top_neck_r2 = list_R[point-1]
                        break

                top_neck_z = top_neck_z1 + (neck_R - top_neck_r1) / (top_neck_r2 - top_neck_r1) * (
                            top_neck_z2 - top_neck_z1)
                bottom_neck_z = bottom_neck_z1 + (neck_R - bottom_neck_r1) / (bottom_neck_r2 - bottom_neck_r1) * (
                            bottom_neck_z2 - bottom_neck_z1)
                length = top_neck_z - bottom_neck_z

            self.AAA_length.append(length)


    # Print data for given timestep
    def print_timestep(self, l):
        print("Results file inn: ", self.file_path_inn)
        print(f"Timestep = {l}")
        print("       AAA_length ")
        print("             [mm] ")
        print("      -------------------")
        print("{0:12.4f}".format(self.AAA_length[l]))


# ======================================================================================================================


class CalculateFusiformAAALengthFromInnerContour3():
    # On initialization read files and save data
    def __init__(self, file_path_inn,neck_relative_radius):
        # Initialize class attributes
        self.file_path_inn = file_path_inn
        self.neck_relative_radius = neck_relative_radius
        self.R_line1_inn = []
        self.z_line1_inn = []
        self.AAA_length = []

        # Read INNER_lines file
        try:
            with open(self.file_path_inn, "r") as file:
                lines_inn = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path_inn)
            print(msg)

        # Save data from INNER_lines file
        list_R_line1 = []
        list_z_line1 = []
        for line in range(5, len(lines_inn)):
            data = lines_inn[line].split()
            if not data:
                self.R_line1_inn.append([])
                self.z_line1_inn.append([])
                for i in range(len(list_R_line1)):
                    self.R_line1_inn[-1].append(list_R_line1[i])
                    self.z_line1_inn[-1].append(list_z_line1[i])
                list_R_line1.clear()
                list_z_line1.clear()
            else:
                list_R_line1.append(float(data[2]))
                list_z_line1.append(float(data[5]))

        # Determine position of AAA necks and calculate distance between them
        for timestep in range(0,len(self.R_line1_inn)):
            bottom_neck_z = 0
            top_neck_z = 0
            list_R = self.R_line1_inn[timestep]
            list_z = self.z_line1_inn[timestep]
            normal_R = list_R[0]
            neck_R = neck_relative_radius * normal_R
            length_zero = True
            for point in range(len(list_R)):
                if list_R[point] >= neck_R:
                    length_zero = False
                    break
            if length_zero:
                length = 0.0
            else:
                bottom_neck_z1 = 0.0
                bottom_neck_z2 = 0.0
                bottom_neck_r1 = 0.0
                bottom_neck_r2 = 0.0
                top_neck_z1 = 0.0
                top_neck_z2 = 0.0
                top_neck_r1 = 0.0
                top_neck_r2 = 0.0
                for point in range(len(list_R)):
                    if list_R[point] >= neck_R:
                        bottom_neck_z1 = list_z[point-1]
                        bottom_neck_z2 = list_z[point]
                        bottom_neck_r1 = list_R[point-1]
                        bottom_neck_r2 = list_R[point]
                        break
                for point in range(len(list_R)-1,0,-1):
                    if list_R[point] >= neck_R:
                        top_neck_z1 = list_z[point]
                        top_neck_z2 = list_z[point-1]
                        top_neck_r1 = list_R[point]
                        top_neck_r2 = list_R[point-1]
                        break

                top_neck_z = top_neck_z1 + (neck_R - top_neck_r1) / (top_neck_r2 - top_neck_r1) * (
                            top_neck_z2 - top_neck_z1)
                bottom_neck_z = bottom_neck_z1 + (neck_R - bottom_neck_r1) / (bottom_neck_r2 - bottom_neck_r1) * (
                            bottom_neck_z2 - bottom_neck_z1)
                length = top_neck_z - bottom_neck_z

            self.AAA_length.append(length)


    # Print data for given timestep
    def print_timestep(self, l):
        print("Results file inn: ", self.file_path_inn)
        print(f"Timestep = {l}")
        print("       AAA_length ")
        print("             [mm] ")
        print("      -------------------")
        print("{0:12.4f}".format(self.AAA_length[l]))


# ======================================================================================================================


class ReadGIDGraphFile1:
    # On initialization read files and save data
    def __init__(self, file_path):
        # Initialize class attributes
        self.file_path = file_path
        self.time = []
        self.mass = []

        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path)
            print(msg)

        for line in lines:
            data = line.split()
            self.time.append(int(float(data[0])))
            self.mass.append(float(data[1]))


# ======================================================================================================================


class ReadResY0File:
    # On initialization read files and save data
    def __init__(self, file_path):
        # Initialize class attributes
        self.file_path = file_path
        self.timestep = []
        self.node = []
        self.radius = []
        self.zcoor = []
        self.S11 = []
        self.S22 = []
        self.S33 = []
        self.M_elas = []
        self.M_MMP = []

        # Read file
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path)
            print(msg)

        # Save data
        list_node = []
        list_r = []
        list_z = []
        list_S11 = []
        list_S22 = []
        list_S33 = []
        list_M_elas = []
        list_M_MMP = []
        first_timestep = True
        for line in range(137, len(lines)):
            data = lines[line].split()
            if not data:
                pass
            elif data[0] == 'Timestep:':
                self.timestep.append(int(data[1]))
                if first_timestep:
                    first_timestep = False
                    pass
                else:
                    self.node.append([])
                    self.radius.append([])
                    self.zcoor.append([])
                    self.S11.append([])
                    self.S22.append([])
                    self.S33.append([])
                    self.M_elas.append([])
                    self.M_MMP.append([])
                    for i in range(len(list_node)):
                        self.node[-1].append(list_node[i])
                        self.radius[-1].append(list_r[i])
                        self.zcoor[-1].append(list_z[i])
                        self.S11[-1].append(list_S11[i])
                        self.S22[-1].append(list_S22[i])
                        self.S33[-1].append(list_S33[i])
                        self.M_elas[-1].append(list_M_elas[i])
                        self.M_MMP[-1].append(list_M_MMP[i])
                    list_node.clear()
                    list_r.clear()
                    list_z.clear()
                    list_S11.clear()
                    list_S22.clear()
                    list_S33.clear()
                    list_M_elas.clear()
                    list_M_MMP.clear()
            else:
                list_node.append(int(data[0]))
                list_r.append(float(data[1]))
                list_z.append(float(data[2]))
                list_S11.append(float(data[3]))
                list_S22.append(float(data[4]))
                list_S33.append(float(data[5]))

                try:
                    list_M_elas.append(float(data[6]))
                except ValueError:
                    list_M_elas.append(0)

                try:
                    list_M_MMP.append(float(data[7]))
                except ValueError:
                    list_M_MMP.append(0)



        self.node.append([])
        self.radius.append([])
        self.zcoor.append([])
        self.S11.append([])
        self.S22.append([])
        self.S33.append([])
        self.M_elas.append([])
        self.M_MMP.append([])
        for i in range(len(list_node)):
            self.node[-1].append(list_node[i])
            self.radius[-1].append(list_r[i])
            self.zcoor[-1].append(list_z[i])
            self.S11[-1].append(list_S11[i])
            self.S22[-1].append(list_S22[i])
            self.S33[-1].append(list_S33[i])
            self.M_elas[-1].append(list_M_elas[i])
            self.M_MMP[-1].append(list_M_MMP[i])
        list_node.clear()
        list_r.clear()
        list_z.clear()
        list_S11.clear()
        list_S22.clear()
        list_S33.clear()
        list_M_elas.clear()
        list_M_MMP.clear()

# ======================================================================================================================


class ReadResY0ILTFile:
    # On initialization read files and save data
    def __init__(self, file_path):
        # Initialize class attributes
        self.file_path = file_path
        self.timestep = []
        self.node = []
        self.radius = []
        self.zcoor = []
        self.S11 = []
        self.S22 = []
        self.S33 = []
        self.M_elas = []
        self.M_MMP = []

        # Read file
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path)
            print(msg)

        # Save data
        list_node = []
        list_r = []
        list_z = []
        list_S11 = []
        list_S22 = []
        list_S33 = []
        list_M_elas = []
        list_M_MMP = []
        first_timestep = True
        for line in range(6, len(lines)):
            data = lines[line].split()
            if not data:
                pass
            elif data[0] == 'Timestep:':
                self.timestep.append(int(data[1]))
                if first_timestep:
                    first_timestep = False
                    pass
                else:
                    self.node.append([])
                    self.radius.append([])
                    self.zcoor.append([])
                    self.S11.append([])
                    self.S22.append([])
                    self.S33.append([])
                    self.M_elas.append([])
                    self.M_MMP.append([])
                    for i in range(len(list_node)):
                        self.node[-1].append(list_node[i])
                        self.radius[-1].append(list_r[i])
                        self.zcoor[-1].append(list_z[i])
                        self.S11[-1].append(list_S11[i])
                        self.S22[-1].append(list_S22[i])
                        self.S33[-1].append(list_S33[i])
                        self.M_elas[-1].append(list_M_elas[i])
                        self.M_MMP[-1].append(list_M_MMP[i])
                    list_node.clear()
                    list_r.clear()
                    list_z.clear()
                    list_S11.clear()
                    list_S22.clear()
                    list_S33.clear()
                    list_M_elas.clear()
                    list_M_MMP.clear()
            else:
                list_node.append(int(data[0]))
                list_r.append(float(data[1]))
                list_z.append(float(data[2]))
                list_S11.append(float(data[3]))
                list_S22.append(float(data[4]))
                list_S33.append(float(data[5]))

                try:
                    list_M_elas.append(float(data[6]))
                except ValueError:
                    list_M_elas.append(0)

                try:
                    list_M_MMP.append(float(data[7]))
                except ValueError:
                    list_M_MMP.append(0)



        self.node.append([])
        self.radius.append([])
        self.zcoor.append([])
        self.S11.append([])
        self.S22.append([])
        self.S33.append([])
        self.M_elas.append([])
        self.M_MMP.append([])
        for i in range(len(list_node)):
            self.node[-1].append(list_node[i])
            self.radius[-1].append(list_r[i])
            self.zcoor[-1].append(list_z[i])
            self.S11[-1].append(list_S11[i])
            self.S22[-1].append(list_S22[i])
            self.S33[-1].append(list_S33[i])
            self.M_elas[-1].append(list_M_elas[i])
            self.M_MMP[-1].append(list_M_MMP[i])
        list_node.clear()
        list_r.clear()
        list_z.clear()
        list_S11.clear()
        list_S22.clear()
        list_S33.clear()
        list_M_elas.clear()
        list_M_MMP.clear()


# ======================================================================================================================


class ReadRonodFile:
    # On initialization read files and save data
    def __init__(self, file_path):
        # Initialize class attributes
        self.file_path = file_path
        self.timestep = []
        self.node = []
        self.radius = []
        self.zcoor = []
        self.theta = []
        self.V_seg = []
        self.M_e_seg0 = []
        self.M_e_segs = []
        self.M_EDP_tot = []
        self.A_VV = []
        self.M_elas = []
        self.M_MMP = []
        self.M_elas = []
        self.M_MMP = []
        self.M_coll = []
        self.M_SMC = []

        # Read file
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            msg = "Can't find file {0}".format(self.file_path)
            print(msg)

        # Save data
        list_node = []
        list_radius = []
        list_zcoor = []
        list_theta = []
        list_V_seg = []
        list_M_e_seg0 = []
        list_M_e_segs = []
        list_M_EDP_tot = []
        list_A_VV = []
        list_M_elas = []
        list_M_MMP = []
        list_M_coll = []
        list_M_SMC = []

        first_timestep = True
        for line in range(137, len(lines)):
            data = lines[line].split()
            if not data:
                pass
            elif data[0] == 'Timestep:':
                self.timestep.append(int(data[1]))
                if first_timestep:
                    first_timestep = False
                    pass
                else:
                    self.node.append([])
                    self.radius.append([])
                    self.zcoor.append([])
                    self.theta.append([])
                    self.V_seg.append([])
                    self.M_e_seg0.append([])
                    self.M_e_segs.append([])
                    self.M_EDP_tot.append([])
                    self.A_VV.append([])
                    self.M_elas.append([])
                    self.M_MMP.append([])
                    self.M_coll.append([])
                    self.M_SMC.append([])
                    for i in range(len(list_node)):
                        self.node[-1].append(list_node[i])
                        self.radius[-1].append(list_radius[i])
                        self.zcoor[-1].append(list_zcoor[i])
                        self.theta[-1].append(list_theta[i])
                        self.V_seg[-1].append(list_V_seg[i])
                        self.M_e_seg0[-1].append(list_M_e_seg0[i])
                        self.M_e_segs[-1].append(list_M_e_segs[i])
                        self.M_EDP_tot[-1].append(list_M_EDP_tot[i])
                        self.A_VV[-1].append(list_A_VV[i])
                        self.M_elas[-1].append(list_M_elas[i])
                        self.M_MMP[-1].append(list_M_MMP[i])
                        self.M_coll[-1].append(list_M_coll[i])
                        self.M_SMC[-1].append(list_M_SMC[i])
                    list_node.clear()
                    list_radius.clear()
                    list_zcoor.clear()
                    list_theta.clear()
                    list_V_seg.clear()
                    list_M_e_seg0.clear()
                    list_M_e_segs.clear()
                    list_M_EDP_tot.clear()
                    list_A_VV.clear()
                    list_M_elas.clear()
                    list_M_MMP.clear()
                    list_M_coll.clear()
                    list_M_SMC.clear()
            else:
                list_node.append(int(data[0]))
                list_radius.append(float(data[3]))
                list_zcoor.append(float(data[1]))
                list_theta.append(float(data[2]))
                list_V_seg.append(float(data[4]))
                list_M_e_seg0.append(float(data[5]))
                list_M_e_segs.append(float(data[6]))
                list_M_EDP_tot.append(float(data[7]))
                list_A_VV.append(float(data[8]))
                list_M_elas.append(float(data[9]))
                list_M_MMP.append(float(data[10]))
                list_M_coll.append(float(data[11]))
                list_M_SMC.append(float(data[12]))
        self.node.append([])
        self.radius.append([])
        self.zcoor.append([])
        self.theta.append([])
        self.V_seg.append([])
        self.M_e_seg0.append([])
        self.M_e_segs.append([])
        self.M_EDP_tot.append([])
        self.A_VV.append([])
        self.M_elas.append([])
        self.M_MMP.append([])
        self.M_coll.append([])
        self.M_SMC.append([])
        for i in range(len(list_node)):
            self.node[-1].append(list_node[i])
            self.radius[-1].append(list_radius[i])
            self.zcoor[-1].append(list_zcoor[i])
            self.theta[-1].append(list_theta[i])
            self.V_seg[-1].append(list_V_seg[i])
            self.M_e_seg0[-1].append(list_M_e_seg0[i])
            self.M_e_segs[-1].append(list_M_e_segs[i])
            self.M_EDP_tot[-1].append(list_M_EDP_tot[i])
            self.A_VV[-1].append(list_A_VV[i])
            self.M_elas[-1].append(list_M_elas[i])
            self.M_MMP[-1].append(list_M_MMP[i])
            self.M_coll[-1].append(list_M_coll[i])
            self.M_SMC[-1].append(list_M_SMC[i])
        list_node.clear()
        list_radius.clear()
        list_zcoor.clear()
        list_theta.clear()
        list_V_seg.clear()
        list_M_e_seg0.clear()
        list_M_e_segs.clear()
        list_M_EDP_tot.clear()
        list_A_VV.clear()
        list_M_elas.clear()
        list_M_MMP.clear()
        list_M_coll.clear()
        list_M_SMC.clear()
