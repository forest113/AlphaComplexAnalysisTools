import sys
MAX_DIFF_RANGE = 100
#Extract data from given file into lists and sort them
def get_simplices(output_file, data):
    temp = output_file.readline().split(" ")
    num_verts = int(temp[0])
    num_edges = int(temp[1])
    num_faces = int(temp[2])
    num_tets = int(temp[3].split('\n')[0])

    for i in range(0, num_verts):
        temp = output_file.readline().split(' ')
        coords = []
        for s in temp:
            if(s != ''):
                coords.append(float(s))
        data['verts'].append(coords)
    
    for i in range(0, num_edges):
        temp = output_file.readline().split(' ')
        edge = []
        for s in temp:
            if(s != ''):
                edge.append(int(s))
        edge = sorted(edge)
        data['edges'].append(edge)
        
    for i in range(0, num_faces):
        temp = output_file.readline().split(' ')
        face = []
        for s in temp:
            if(s != ''):
                face.append(int(s))
        face = sorted(face)
        data['faces'].append(face)
      
    for i in range(0, num_tets):
        temp = output_file.readline().split(' ')
        tet = []
        for s in temp:
            if(s != ''):
                tet.append(int(s))
        tet = sorted(tet)
        data['tets'].append(tet)
        
#recompute indices of simplices  to match indices in list'new_verts'
def recompute_indices(simplices):
    for ele in simplices:
        for i in range(len(ele)):
            ele[i] = ele[i]+1
        ele = sorted(ele)
    return simplices
    
def set_diff(A, B, k):
    diff = []
    for i in range(len(A)):
        found = False
        range_low = 0
        range_high = len(B)
        if(i-k > 0):
            range_low = i-k
        if(i+k < len(B)):
            range_high = i+k
        
        for j in range(range_low, range_high):
                if(A[i] == B[j]): 
                    found = True
        if(found == False):
            diff.append(A[i])
    return diff
        
AC_op_file = open(sys.argv[1], 'r')
pAC_op_file = open(sys.argv[2], 'r')
extra_file = open("cmp/extra.obj","w")
missing_file = open("cmp/missing.obj","w")
	

#alpha complex output
AC_op = {}
AC_op['verts'] = []
AC_op['faces'] = []
AC_op['edges'] = []
AC_op['tets'] = []

#ParallelAC output
pAC_op = {}
pAC_op['verts'] = []
pAC_op['faces'] = []
pAC_op['edges'] = []
pAC_op['tets'] = []


#Get Alpha complex output
get_simplices(AC_op_file, AC_op)
#Get ParallelAC output
get_simplices(pAC_op_file, pAC_op)

for i in range(len(AC_op['verts'])-1):
    for j in range(0,4):
        if(AC_op['verts'][i+1][j] - pAC_op['verts'][i][j] < 0.0001):
           pAC_op['verts'][i][j] = AC_op['verts'][i+1][j]

v1 = set(tuple(i) for i in AC_op['verts'])
v2 = set(tuple(i) for i in pAC_op['verts'])
verts_union = AC_op['verts']
for vert in verts_union:
    line = "v "+ str(vert[0]) + (" ") + str(vert[1]) + (" ") + str(vert[2]) + (" ") + str(vert[3]) + "\n"
    extra_file.write(line)
    missing_file.write(line)

print('computed verts union')
#Recompute indices so that all indices correspond to union of verts
AC_op['edges'] = sorted(AC_op['edges'])
AC_op['faces'] = sorted(AC_op['faces'])
AC_op['tets'] = sorted(AC_op['tets'])

print('recomputing indices for pac edges')
pAC_op['new_edges'] = sorted(recompute_indices(pAC_op['edges']))
print('recomputing indices for pac tris')
pAC_op['new_faces'] = sorted(recompute_indices(pAC_op['faces']))
print('recomputing indices for pac tets')
pAC_op['new_tets'] = sorted(recompute_indices(pAC_op['tets']))
#Convert lists into tuples so that verts are hashable
extra_edges = set_diff(pAC_op['new_edges'], AC_op['edges'],MAX_DIFF_RANGE)
missing_edges = set_diff(AC_op['edges'],pAC_op['new_edges'],MAX_DIFF_RANGE)

extra_tris = set_diff(pAC_op['new_faces'],AC_op['faces'],MAX_DIFF_RANGE)
missing_tris = set_diff(AC_op['faces'],pAC_op['new_faces'],MAX_DIFF_RANGE)

extra_tets = set_diff(pAC_op['new_tets'],AC_op['tets'],MAX_DIFF_RANGE)
missing_tets = set_diff(AC_op['tets'],pAC_op['new_tets'],MAX_DIFF_RANGE)
   
print("extra edges:")
for ele in extra_edges:
   line_out = "l " + str(int(ele[0])+1) + " " + str(int(ele[1])+1) + '\n'
   extra_file.write(line_out)
   print(ele)
   
print("missing edges:")
for ele in missing_edges:
   line_out = "l " + str(int(ele[0])+1) + " " + str(int(ele[1])+1) + '\n'
   missing_file.write(line_out)
   print(ele)
   

print("extra tris:")
for ele in extra_tris:
   line_out = "f " + str(int(ele[0])+1) + " " + str(int(ele[1])+1) + " " + str(int(ele[2])+1) + '\n'
   extra_file.write(line_out)
   print(ele)
   
print("missing tris:")
for ele in missing_tris:
   line_out = "f " + str(int(ele[0])+1) + " " + str(int(ele[1])+1) + " " + str(int(ele[2])+1) + '\n'
   missing_file.write(line_out)
   print(ele)

print("extra tets:")
for tet in extra_tets:
   line_out = "f " + str(int(tet[0])+1) + " " + str(int(tet[1])+1) + " " + str(int(tet[2])+1) + '\n'
   extra_file.write(line_out)
   line_out = "f " + str(int(tet[1])+1) + " " + str(int(tet[2])+1) + " " + str(int(tet[3])+1) + '\n'
   extra_file.write(line_out)
   line_out = "f " + str(int(tet[2])+1) + " " + str(int(tet[3])+1) + " " + str(int(tet[0])+1) + '\n'
   extra_file.write(line_out)
   line_out = "f " + str(int(tet[3])+1) + " " + str(int(tet[0])+1) + " " + str(int(tet[1])+1) + '\n'
   extra_file.write(line_out)
   print(tet)
   
print("missing tets:")
for tet in missing_tets:
   line_out = "f " + str(int(tet[0])+1) + " " + str(int(tet[1])+1) + " " + str(int(tet[2])+1) + '\n'
   missing_file.write(line_out)
   line_out = "f " + str(int(tet[1])+1) + " " + str(int(tet[2])+1) + " " + str(int(tet[3])+1) + '\n'
   missing_file.write(line_out)
   line_out = "f " + str(int(tet[2])+1) + " " + str(int(tet[3])+1) + " " + str(int(tet[0])+1) + '\n'
   missing_file.write(line_out)
   line_out = "f " + str(int(tet[3])+1) + " " + str(int(tet[0])+1) + " " + str(int(tet[1])+1) + '\n'
   missing_file.write(line_out)
   print(tet)



