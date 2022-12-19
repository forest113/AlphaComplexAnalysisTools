import math

class Atom:
    
    def __init__(self, atom):
        self.x = atom[0]
        self.y = atom[1]
        self.z = atom[2]
        self.radius = atom[3]

def get_edge_orthoradius(verts, simplice):
    a1 = verts[simplice[0]]
    a2 = verts[simplice[1]]
    a = a1[0] - a2[0]
    b = a1[1] - a2[1]
    c = a1[2] - a2[2]
    d = (a1[0] * a1[0] - a2[0] * a2[0]) + (a1[1] * a1[1] - a2[1] * a2[1]) + (a1[2] * a1[2] - a2[2] * a2[2]) - (a1[3] * a1[3]) + (a2[3] * a2[3])
    d /= 2
    t = (d - a * a1[0] - b * a1[1] - c * a1[2])
    return ((t * t) / (a * a + b * b + c * c)) - (a1[3] * a1[3])

def get_tri_orthoradius(verts, simplice):
    a1 = Atom(verts[simplice[0]])
    a2 = Atom(verts[simplice[1]])
    a3 = Atom(verts[simplice[2]])
    a11 = a1.x - a2.x
    a12 = a1.y - a2.y
    a13 = a1.z - a2.z
    b1 = (a1.x * a1.x - a2.x * a2.x) + (a1.y * a1.y - a2.y * a2.y) + (a1.z * a1.z - a2.z * a2.z) - (a1.radius * a1.radius) + (a2.radius * a2.radius)
    b1 /= 2
    #Find equation of plane of intersection of atoms a2 and a3
    a21 = a2.x - a3.x
    a22 = a2.y - a3.y
    a23 = a2.z - a3.z
    b2 = (a2.x * a2.x - a3.x * a3.x) + (a2.y * a2.y - a3.y * a3.y)+ (a2.z * a2.z - a3.z * a3.z) - (a2.radius * a2.radius)+ (a3.radius * a3.radius)
    b2 /= 2
    # Find equation of plane containing centers of atoms a1, a2 and a3
    a31 = (a2.y - a1.y) * (a3.z - a1.z) - (a3.y - a1.y) * (a2.z - a1.z)
    a32 = (a2.z - a1.z) * (a3.x - a1.x) - (a3.z - a1.z) * (a2.x - a1.x)
    a33 = (a2.x - a1.x) * (a3.y - a1.y) - (a3.x - a1.x) * (a2.y - a1.y)
    b3 = a31 * a1.x + a32 * a1.y + a33 * a1.z
    # Use Cramer's rule to find intersection point of these three planes
    D = a11 * a22 * a33 + a12 * a23 * a31 + a13 * a21 * a32 - a13 * a22 * a31 - a12 * a21 * a33 - a11 * a23 * a32
    Dx = b1 * a22 * a33 + a12 * a23 * b3 + a13 * b2 * a32 - a13 * a22 * b3 - a12 * b2 * a33 - b1 * a23 * a32
    Dy = a11 * b2 * a33 + b1 * a23 * a31 + a13 * a21 * b3 - a13 * b2 * a31 - b1 * a21 * a33 - a11 * a23 * b3
    Dz = a11 * a22 * b3 + a12 * b2 * a31 + b1 * a21 * a32 - b1 * a22 * a31 - a12 * a21 * b3 - a11 * b2 * a32
    X = Dx / D
    Y = Dy / D
    Z = Dz / D
    dist = (a1.x - X) * (a1.x - X) + (a1.y - Y) * (a1.y - Y) + (a1.z - Z) * (a1.z - Z) - a1.radius * a1.radius
    return dist
    
def get_tet_orthoradius(verts, simplice):
    a1 = Atom(verts[simplice[0]])
    a2 = Atom(verts[simplice[1]])
    a3 = Atom(verts[simplice[2]])
    a4 = Atom(verts[simplice[3]])
    
    a11 = a1.x - a2.x
    a12 = a1.y - a2.y
    a13 = a1.z - a2.z
    b1 = (a1.x * a1.x - a2.x * a2.x) + (a1.y * a1.y - a2.y * a2.y) + (a1.z * a1.z - a2.z * a2.z) - (a1.radius * a1.radius) + (a2.radius * a2.radius)
    b1 /= 2
    # Find equation of plane of intersection of atoms a2 and a3
    a21 = a2.x - a3.x
    a22 = a2.y - a3.y
    a23 = a2.z - a3.z
    b2 = (a2.x * a2.x - a3.x * a3.x) + (a2.y * a2.y - a3.y * a3.y) + (a2.z * a2.z - a3.z * a3.z) - (a2.radius * a2.radius) + (a3.radius * a3.radius)
    b2 /= 2
    # Find equation of plane of intersection of atoms a3 and a4
    a31 = a3.x - a4.x
    a32 = a3.y - a4.y
    a33 = a3.z - a4.z
    b3 = (a3.x * a3.x - a4.x * a4.x) + (a3.y * a3.y - a4.y * a4.y) + (a3.z * a3.z - a4.z * a4.z) - (a3.radius * a3.radius) + (a4.radius * a4.radius)
    b3 /= 2
    # Use Cramer's rule to find ortho-sphere center
    D = a11 * a22 * a33 + a12 * a23 * a31 + a13 * a21 * a32 - a13 * a22 * a31 - a12 * a21 * a33 - a11 * a23 * a32
    Dx = b1 * a22 * a33 + a12 * a23 * b3 + a13 * b2 * a32 - a13 * a22 * b3 - a12 * b2 * a33 - b1 * a23 * a32
    Dy = a11 * b2 * a33 + b1 * a23 * a31 + a13 * a21 * b3 - a13 * b2 * a31 - b1 * a21 * a33 - a11 * a23 * b3
    Dz = a11 * a22 * b3 + a12 * b2 * a31 + b1 * a21 * a32 - b1 * a22 * a31 - a12 * a21 * b3 - a11 * b2 * a32
    if (D == 0.0): 
        return 0
    else:
        X = Dx / D
        Y = Dy / D
        Z = Dz / D
        dist = (a2.x - X) * (a2.x - X) + (a2.y - Y) * (a2.y - Y) + (a2.z - Z) * (a2.z - Z) - a2.radius * a2.radius
        return dist
