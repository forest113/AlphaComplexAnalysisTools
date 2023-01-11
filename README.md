# AlphaComplexHelpers
Tools to help compare and debug different alpahcomplex outputs
Algorithms to compute Delaunay triangulations and Alpha shapes often differ in their outputs to some degree. When it comes to large input sizes as is the case with biomolecules, analyzing, debugging and comparing these output triangulations requires some tools and automation.This repository contains some tools which can help in this process.

the repository contains the following scripts:
Running the main python file provides the user with the following options
1. Sanity check: checks for self intersection between simplices in a given alpha shape
2. Visualisation: produces obj files which can be viewd on meshalb
3. comparision of two alpha shapes: reports extra and missing simplices given a test alpha complex output and a (asumed to be) correct one
4. qerrying orthoradius:querry simplice sizes by typing in indices of the atoms in the simplices.

The repository also conatins a scripts to render obj files using opengl. this is a quick way to view the meshes after generating obj files.

All the scripts asume that the alpha complex files are in the format of a text file with all the vertices listed first, followed by the simplices listed with the indices of the participating vertices

**Instrcutions to run:**

Dependencies:

python3

the scripts make use of some libarries that can easily be installed using pip
```
pip install sympy
pip install numpy
```

->clone the repository

->install libraries

->run the main script using:
```
python3 /path/to/dir/alphaComplexTools.py
```

->run the opengl render script using
'''
python3 /path/to/dir/render_mesh.py
'''
drag abd drop an obj file onto the GUI that pops up to render the mesh
