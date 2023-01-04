import sys
def create(fin_path, fout_path):
    fout = open(fout_path+".obj", "w")
    fin = open(fin_path,"r")
    num_verts = 0
    num_edges = 0
    num_tris = 0
    num_tets = 0

    line = fin.readline()
    num_verts = line.split(" ")[0]
    num_edges = line.split(" ")[1]
    num_tris = line.split(" ")[2]
    num_tets = line.split(" ")[3]

    for i in range(0,int(num_verts)):
       temp = fin.readline().split(" ")
       vert = []
       for x in temp:
          if(x != ''):
             vert.append(x)

       line_out = "v "+ vert[0] + (" ") + vert[1] + (" ") + vert[2] + (" ") + vert[3]
       fout.write(line_out)
   
    for i in range(0,int(num_edges)):
       temp = fin.readline().split(" ")
       edge = []
       for x in temp:
          if(x != ''):
             edge.append(x)
       print(edge)
       line_out = "l " + str(int(edge[0])) + " " + str(int(edge[1])) + '\n'
       fout.write(line_out)
   
    print(num_tris)
    for i in range(0, int(num_tris)):
       temp = fin.readline().split(" ")
       tri = []
       for x in temp:
          if(x != ''):
             tri.append(x)
       print(tri)
       line_out = "f " + str(int(tri[0])) + " " + str(int(tri[1])) + " " + str(int(tri[2])) + '\n'
       fout.write(line_out)
   
    for i in range(0, int(num_tets)):
       temp = fin.readline().split(" ")
       tet = []
       for x in temp:
          if(x != ''):
             tet.append(x)
       print(tet)
       line_out = "f " + str(int(tet[0])) + " " + str(int(tet[1])) + " " + str(int(tet[2])) + '\n'
       fout.write(line_out)
       line_out = "f " + str(int(tet[1])) + " " + str(int(tet[2])) + " " + str(int(tet[3])) + '\n'
       fout.write(line_out)
       line_out = "f " + str(int(tet[2])) + " " + str(int(tet[3])) + " " + str(int(tet[0])) + '\n'
       fout.write(line_out)
       line_out = "f " + str(int(tet[3])) + " " + str(int(tet[0])) + " " + str(int(tet[1])) + '\n'
       fout.write(line_out)
   


