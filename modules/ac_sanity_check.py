import math
import numpy as np
from sympy import Point3D, Segment3D, Line3D, Plane
from sympy.vector import CoordSys3D
GRID_SIZE = 0.1;

#*******************************************     
#**************GRID functions***************
#*******************************************

def find_bounds(verts, r_min, r_max, r_num_grids):
    r_min.append(verts[0][0])
    r_min.append(verts[0][1])
    r_min.append(verts[0][2])
    r_max.append(verts[0][0]) 
    r_max.append(verts[0][1])
    r_max.append(verts[0][2])	
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
     
    r_num_grids.append(math.ceil((r_max[0]-r_min[0])/GRID_SIZE))
    r_num_grids.append(math.ceil((r_max[1]-r_min[1])/GRID_SIZE))
    r_num_grids.append(math.ceil((r_max[2]-r_min[2])/GRID_SIZE))
     
def find_simplice_bounds(verts, simplice, grid_lower, grid_upper, num_grids, r_simplice_lower, r_simplice_upper):
    r_simplice_lower.append(num_grids[0])
    r_simplice_lower.append(num_grids[1])
    r_simplice_lower.append(num_grids[1])
    r_simplice_upper.append(0)
    r_simplice_upper.append(0)
    r_simplice_upper.append(0)
    for i in range(0, len(simplice)):
        vert = verts[simplice[i]]
        vert_bounds = []
        vert_bounds.append(math.floor((vert[0] - grid_lower[0])/GRID_SIZE))
        vert_bounds.append(math.floor((vert[1] - grid_lower[1])/GRID_SIZE))
        vert_bounds.append(math.floor((vert[2] - grid_lower[2])/GRID_SIZE))
        
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
           
def lies_between(a,b,c):
    if(a >= b and a<= c):
        return True
    return False
            
def bounds_isect(bounds1, bounds2):
    if(lies_between(bounds1[0][0], bounds2[0][0], bounds2[1][0]) and lies_between(bounds1[0][1], bounds2[0][1], bounds2[1][1]) and lies_between(bounds1[0][2], bounds2[0][2], bounds2[1][2])):
        return True
    if(lies_between(bounds1[1][0], bounds2[0][0], bounds2[1][0]) and lies_between(bounds1[1][1], bounds2[0][1], bounds2[1][1]) and lies_between(bounds1[1][2], bounds2[0][2], bounds2[1][2])):
        return True
    return False
    
def check_simplice_bounds_isect(simplice1, simplice2, verts, grid_lower, grid_upper, num_grids):
    s1_lower = []
    s1_upper = []
    s2_lower = []
    s2_upper = []
    find_simplice_bounds(verts, simplice1, grid_lower, grid_upper, num_grids, s1_lower, s1_upper)
    find_simplice_bounds(verts, simplice2, grid_lower, grid_upper, num_grids, s2_lower, s2_upper)
    return bounds_isect([s1_lower,s1_upper],[s2_lower,s2_upper])
    
#*******************************************     
#************geometry funsctions*************
#*******************************************

def get_tri_center(tri):
    COM = []
    COM.append((tri[0][0] + tri[1][0] + tri[2][0])/3)
    COM.append((tri[0][1] + tri[1][1] + tri[2][1])/3)
    COM.append((tri[0][2] + tri[1][2] + tri[2][2])/3)
    return COM
    
def point_in_tri(point, tri):
    N = CoordSys3D('N')
    p = Point3D(point)
    norm = Plane(Point3D(tri[0]), Point3D(tri[1]), Point3D(tri[2])).normal_vector
    if(not Point3D.are_coplanar(p, Point3D(tri[0]), Point3D(tri[1]), Point3D(tri[2]))):
        return False
    sign = 0
    for i in range(0,3):
        vert1 = tri[i]
        vert2 = tri[(i+1)%3]
        v1 = [(p[0]-vert1[0]),(p[1]-vert1[1]), (p[2]-vert1[2])]
        v2 = [(vert2[0]-p[0]), (vert2[1]-p[1]),(vert2[2]-p[2])]
        cross = np.cross(v1,v2)
        dot = np.dot(norm,cross)
        if(sign == 0):
            sign = math.copysign(1,dot)
        else:       
            if(sign != math.copysign(1,dot)):
                return False
    return True

#print(point_in_tri([0,0,0],[[-1,2,-1],[1,2,-1],[0,2,3]])) #**test passed**

def line_in_tri(edge,tri):
    p1, p2 = Point3D(edge[0]), Point3D(edge[1])
    line = Line3D(p1,p2)
    
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
        if(isect[0] == p1 or isect[0] == p2):
            return False
        print(p1,p2,p3,p4, isect)
        return True
    else:
        return False
   
#print(edge_isect_edge([[0,0,0],[1,1,1]], [[-1,0, 0],[0,1,1]])) #*test passed*


def tri_isect_edge(tri, edge):
    plane = Plane(Point3D(tri[0]), Point3D(tri[1]), Point3D(tri[2]))
    p1,p2 = Point3D(edge[0]), Point3D(edge[1])
    seg = Segment3D(p1,p2)
    isect = plane.intersection(seg)
    if(not isect):
        return False
    
    if(type(isect[0]) is Point3D):
        if(point_in_tri(isect[0], tri) and isect[0] != p1 and isect[0] != p2):
            #print('point in tri', isect, plane,tri)
            return True
        else:
            return False
    
    elif(type(isect[0]) is Line3D or type(isect[0]) is Segment3D):
        print(isect[0])
        if(line_in_tri(isect[0].points, tri)):
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
    grid_min = []
    grid_max = []
    num_grids = []
    find_bounds(verts, grid_min, grid_max, num_grids)
    e_buckets = []
    t_buckets = []
    for a in range(0, num_grids[0]):
        e_buckets.append([])
        t_buckets.append([])
        for b in range(0, num_grids[1]):
            e_buckets[a].append([])
            t_buckets[a].append([])
            for c in range(0, num_grids[2]):
                e_buckets[a][b].append([])
                t_buckets[a][b].append([])
    
    
    edges = simplices['edges']
    tris = simplices['faces']
    tets = simplices['tets']
    
    for tet in tets:
        tris.append([tet[0], tet[1], tet[2]])
        tris.append([tet[1], tet[2], tet[3]])
        tris.append([tet[2], tet[3], tet[0]])
        tris.append([tet[3], tet[0], tet[1]])   
    
    for e in edges:
        e_upper = []
        e_lower = []
        find_simplice_bounds(verts, e, grid_min, grid_max, num_grids, e_lower, e_upper) 
        for i in range(e_lower[0], e_upper[0]):
            for j in range(e_lower[1], e_upper[1]):
                for k in range(e_lower[2], e_upper[2]):
                    e_buckets[i][j][k].append(e)
                   
    for t in tris:
        t_upper = []
        t_lower = []
        find_simplice_bounds(verts, t, grid_min, grid_max, num_grids, t_lower, t_upper) 
        for i in range(t_lower[0], t_upper[0]):
            for j in range(t_lower[1], t_upper[1]):
                for k in range(t_lower[2], t_upper[2]):
                    t_buckets[i][j][k].append(t)
                    
    test_pass = True
    
    edge_edge = []
    edge_tri = []
    tri_tri = []
    
    """#edge - edge
    for i in range(0,len(edges)):
        for j in range(i+1, len(edges)):
            print('edge edge',i,j)
            if(not check_simplice_bounds_isect(edges[i], edges[j], verts, grid_min, grid_max, num_grids)):
                print('skip')
                continue
                
            if(edge_isect_edge([verts[edges[i][0]][0:3],verts[edges[i][1]][0:3]], [verts[edges[j][0]][0:3],verts[edges[j][1]][0:3]])):
                edge_edge.append([edges[i],edges[j]])
                test_pass = False
                print('isecttt')"""
                
    #edge - tri
    print(e_buckets)
    print(t_buckets)
    for a in range(0, num_grids[0]):
        for b in range(0, num_grids[1]):
            for c in range(0, num_grids[2]):
                bucket_edges = e_buckets[a][b][c]
                bucket_tris = t_buckets[a][b][c]
                #print('bucket',a,b,c)
                for i in range(0,len(bucket_edges)):
                    for j in range(0, len(bucket_tris)):
                        common_vert_flag = False
                        for vert in bucket_tris[j]:
                            if(bucket_edges[i][0] == vert or bucket_edges[i][1] == vert):
                                common_vert_flag = True
                                break
                        if(common_vert_flag):
                            continue
                        print(bucket_tris[j], bucket_edges[i], len(verts))
                        if(tri_isect_edge([verts[bucket_tris[j][0]][0:3],verts[bucket_tris[j][1]][0:3],verts[bucket_tris[j][2]][0:3]], [verts[bucket_edges[i][0]][0:3],verts[bucket_edges[i][1]][0:3]])):
                            edge_tri.append([bucket_edges[i],bucket_tris[j]])
                            test_pass = False
                            print('*****isect******')
                            print([verts[bucket_tris[j][0]][0:3],verts[bucket_tris[j][1]][0:3],verts[bucket_tris[j][2]][0:3]], [verts[bucket_edges[i][0]][0:3],verts[bucket_edges[i][1]][0:3]])
                
    """#tri - tri
    for i in range(0,len(tris)):
        
        for j in range(i+1, len(tris)):
            if(not check_simplice_bounds_isect(tris[i], tris[j], verts, grid_min, grid_max, num_grids)):
                continue
            if(tri_isect_tri([verts[tris[i][0]][0:3],verts[tris[i][1]][0:3],verts[tris[i][2]][0:3]], [verts[tris[j][0]][0:3],verts[tris[j][1]][0:3],verts[tris[j][2]][0:3]])):
                tri_tri.append([tris[i],tris[j]])
                test_pass = False
                print('*****isect******')"""
                
    print('test pass:', test_pass)
    #print('edge-edge intersections:',edge_edge)
    print('edge-tri:',edge_tri)
    #print('tri-tri:',tri_tri)

     
             
    
