# vertex-cover
Experiments with integer programs for Vertex Cover

# Desciption
This repo includes implementations of two ILP-based algorithms solving Vertex Cover with weighted vertices. 
One (vc-ilp.py) models the problem as an ILP in the standard way and then calls Gurobi.
The second one (vc-kernel.py) first constructs a 2-approximate vertex cover (w.r.t. to the number of vertices) and uses a smarter ILP that is also processed by Gurobi.

# Input data
The directory "input" contains several graphs in the following format.
The first line contains integers n, m: the numbers of vertices and edges.
Each of the following m lines has two numbers describing one edge.
The vertices are indexed from 0 to n-1.
The following n lines contains the vertex weights (positive integer).

These files are named with the following convention: file graph40-e5.in describes a random graph on roughly 10^5 vertices with a planted vertex cover of size 40.
The larger input files are located on my website: https://www.mimuw.edu.pl/~mw277619/stuff/ilp/

# Usage
You need Python packages pulp and gurobipy. You also need Gurobi licence key that should be pasted in the field "options".
If executed with the parameter "-w" the algorithm will read the vertex weights (the last n lines, as described above).
Otherwise, it will stop reading input after the description of edges, and each vertex will be assigned weight 1.0.
