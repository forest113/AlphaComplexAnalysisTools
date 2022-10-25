import math
from sympy import Point3D, Segment3D, Line3D, Plane

GRID_SIZE = 0.5;

#*******************************************     
#**************GRID functions***************
#*******************************************

def find_bounds(verts, r_min, r_max, r_num_grids):
    r_min = [verts[0][0], vetrs[0][1], verts[0][2]]
    r_max = [verts[0][0], vetrs[0][1], verts[0][2]]
    for i in range(1, len(verts)):
         if(verts[i][0] < r_min[0]):
             r_min[0] = verts[i][0]

         if(verts[i][1] < r_min[1]):
             r_min[1] = verts[i][1]
         
         if(verts[i][2] < r_min[2]):
             r_min[2] = verts[i][2]
             
         if(verts[i][0] > r_max[0]):
             r_max[0] = verts[i][0]
         
         if(verts[i][1] > r_max[1]):
             r_max[1] = verts[i][1]
         
         if(verts[i][2] > r_max[2]):
             r_max[2] = verts[i][2]
     
    r_num_grids[0] = math.ciel((r_max[0]-r_min[0])/GRID_SIZE)
    r_num_grids[1] = math.ciel((r_max[1]-r_min[1])/GRID_SIZE)
    r_num_grids[2] = math.ciel((r_max[2]-r_min[2])/GRID_SIZE)
     
def find_simplice_bounds(verts, simplice, grid_lower, grid_upper, num_grids, r_simplice_lower, r_simplice_upper):
    r_simplice_lower = num_grids
    r_simplice_upper = [0,0,0]
    for i in range(0, len(simplice)):
        vert = verts[simplice[i]]
        vert_bounds = []
        vert_bounds.append((vert[0] - grid_lower[0])/GRID_SIZE)
        vert_bounds.append((vert[1] - grid_lower[1])/GRID_SIZE)
        vert_bounds.append((vert[2] - grid_lower[2])/GRID_SIZE)
        
        if(vert_bounds[0] < r_simplice_lower[0]):
            r_simplice_lower[0] = vert_bounds[0]
        if(vert_bounds[1] < r_simplice_lower[1]):
            r_simplice_lower[1] = vert_bounds[1]
        if(vert_bounds[2] < r_simplice_lower[2]):
            r_simplice_lower[2] = vert_bounds[2]
            
        if(vert_bounds[0] > r_simplice_upper[0]):
            r_simplice_upper[0] = vert_bounds[0]
        if(vert_bounds[1] > r_simplice_upper[1]):
            r_simplice_upper[1] = vert_bounds[1]
        if(vert_bounds[2] > r_simplice_upper[2]):
            r_simplice_upper[2] = vert_bounds[2]
    
#*******************************************     
#************utility funsctions*************
#*******************************************

def get_tri_center(tri):
    COM = []
    COM.append((tri[0][0] + tri[1][0] + tri[2][0])/3)
    COM.append((tri[0][1] + tri[1][1] + tri[2][1])/3)
    COM.append((tri[0][2] + tri[1][2] + tri[2][2])/3)
    return COM
    
def point_in_tri(point, tri):
    COM = get_tri_center(tri)
    segment = Segment3D(Point3D(point), Point3D(COM))
    edges = []
    edges.append(Segment3D(Point3D(tri[0]), Point3D(tri[1])))
    edges.append(Segment3D(Point3D(tri[1]), Point3D(tri[2])))
    edges.append(Segment3D(Point3D(tri[2]), Point3D(tri[0])))
    num_isects = 0
    for e in edges:
        if(segment.intersection(e)):
            return False
    return True

#print(point_in_tri([0,0,0],[[-1,0,-1],[1,0,-1],[0,0,3]])) #**test passed**

def line_in_tri(edge,tri):
    line = Line3D(Point3D(edge[0]), Point3D(edge[1]))
    
    edges = []
    edges.append(Segment3D(Point3D(tri[0]), Point3D(tri[1])))
    edges.append(Segment3D(Point3D(tri[1]), Point3D(tri[2])))
    edges.append(Segment3D(Point3D(tri[2]), Point3D(tri[0])))
    num_isects = 0
    for e in edges:
        if(line.intersection(e)):
            num_isects += 1
    if(num_isects>1):
        return True
    else:
        return False
        
#print(line_in_tri([[-1,0,5],[1,0,5]], [[-1,0,-1], [1,0,-1], [0,0,3]])) #*test passed*
    

#*******************************************     
#************Intersection tests*************
#*******************************************
    
def edge_isect_edge(edge1, edge2):
    p1, p2, p3, p4 = Point3D(edge1[0]), Point3D(edge1[1]), Point3D(edge2[0]), Point3D(edge2[1])
    s1, s2 = Segment3D(p1, p2), Segment3D(p3, p4)
    isect = s1.intersection(s2)
    if(isect):
        return True
    else:
        return False
   
#print(edge_isect_edge([[0,0,0],[1,1,1]], [[-1,0, 0],[0,1,1]])) #*test passed*


def tri_isect_edge(tri, edge):
    plane = Plane(Point3D(tri[0]), Point3D(tri[1]), Point3D(tri[2]))
    seg = Segment(Point3D(edge[0]), Point3D(edge[1]))
    isect = plane.intersection(seg)
    if(not isect):
        return False
    
    if(type(isect[0]) is Point3D):
        if(point_in_tri(isect[0], tri)):
            return True
        else:
            return False
    
    elif(type(isect[0]) is Line3D or type{isect[0] is Segment3D):
        if(line_in_tri(isect[0], tri)):
            return True
        else:
            return False
            
            

def tri_isect_tri(tri1, tri2):
    plane1 = Plane(Point3D(tri1[0]), Point3D(tri1[1]), Point3D(tri1[2]))
    plane2 = Plane(Point3D(tri2[0]), Point3D(tri2[1]), Point3D(tri2[2]))
    if(plane1.is_coplanar(plane2)):
        if(line_in_tri([tri1[0],tri1[1]], tri2) or line_in_tri([tri1[1],tri1[2]],tri2) or line_in_tri([tri1[2],tri1[0]], tri2)):
            return True
        return False
    isect = plane1.intersection(plane2)
    if(line_in_tri(isect[0], tri1) and line_in_tri(isect[0], tri2)):
        return True
    return False
    
def sanity_check(verts, simplices):
    

     
             
    
