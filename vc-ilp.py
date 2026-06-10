import pulp as lp
import sys
import gurobipy as gp

# Gurobi licence setup
options = {
    "WLSACCESSID": "",
    "WLSSECRET": "",
    "LICENSEID": 0,
}
env = gp.Env(params=options)

weight_mode = 0
if len(sys.argv) > 1 and sys.argv[1] == "-w":
    weight_mode = 1
    print("Weighted mode\n")

n, m = map(int, input().split())

vertices = range(n)
weight = [1] * n
edges = []

for i in range(m):
    u, v = map(int, input().split())
    edges.append((u,v))

# in the weighted mode (option "-w") we read vertex weights
if weight_mode:
    for i in vertices:
        weight[i] = int(input())

# setup ILP and variables
ilp = lp.LpProblem("vertex_cover_ilp_standard", lp.LpMinimize)
x = lp.LpVariable.dicts("x", vertices, cat = 'Binary')

# constraints: for each edge, one of its endpoints must be in the vertex cover
for (u,v) in edges:
    ilp += lp.LpAffineExpression([(x[u],1), (x[v],1)]) >= 1

# objective function: weighted sum of chosen vertices
ilp += lp.lpSum(lp.LpAffineExpression([(x[v], weight[v])]) for v in vertices)

solver = lp.GUROBI(env = env, msg = False)   # uses gurobipy, not gurobi_cl
#solver = lp.PULP_CBC_CMD(msg=0) # uses the default CBC solver that comes with PuLP
ilp.solve(solver)
solver.close()

vc_size = 0
vc_val = 0

# output the size of the weight of the solution
for v in vertices:
    vc_size += lp.value(x[v])
    vc_val += weight[v] * lp.value(x[v])

print("\n" + str(vc_size) + " " + str(vc_val) + "\n")
