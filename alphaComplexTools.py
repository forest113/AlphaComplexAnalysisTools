from modules.ac_sanity_check import *
from modules.ac_cpu_gpu_cmp import *
from modules.create_obj_file import *
from modules.orthoradius import *

choice = 0
while(choice != 5):
    print('1: sanity check')
    print('2: obj files visualisation')
    print('3: compare outputs')
    print('4: querry orthoradius')
    print('5: exit')
    choice = int(input('enter option:'))
    alphaComplex_file1 = input("enter the path to your alphacomplex file")
    
    if(choice == 1):
        simplices = {}
        simplices['verts'] = []
        simplices['faces'] = []
        simplices['edges'] = []
        simplices['tets'] = []
        get_simplices(alphaComplex_file1, simplices)
        sanity_check(simplices['verts'],simplices)
        
    if(choice == 2):
        obj_file_path = input("where would you like to store the obj file?:")
        create_obj_file.create(alphaComplex_file1, obj_file_path)
        print('done! open with meshlab->import mesh->your obj file')
        
    if(choice == 3):
        alphaComplex_file2 = input("which alphacomplex would you like to compare against?:")
        ac_cpu_gpu_cmp.compare(alphaComplex_file1, alphaComplex_file2)
        
    if(choice == 4):
        simplices = {}
        simplices['verts'] = []
        simplices['faces'] = []
        simplices['edges'] = []
        simplices['tets'] = []
        get_simplices(alphaComplex_file1, simplices)
        quit = input('press q to quit, any key to continue')
        while(quit != 'q' or 'Q'):
            simplice_str = input('Enter indices of simplice seperated by commas')
            simplice = []
            for ind in simplice_str.split(','):
                simplice.append(int(ind))
            
            if(len(simplice)==2):
                print(get_edge_orthoradius(simplices['verts'],simplice))
            if(len(simplice)==3):
                print(get_tri_orthoradius(simplices['verts'],simplice))
            if(len(simplice)==4):
                print(get_tet_orthoradius(simplices['verts'],simplice))
                
    
    
