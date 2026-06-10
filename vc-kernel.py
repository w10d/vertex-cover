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
adj = [set() for v in vertices]

for i in range(m):
    u, v = map(int, input().split())
    edges.append((u,v))
    adj[u].add(v)
    adj[v].add(u)

# in the weighted mode (option "-w") we read vertex weights
if weight_mode:
    for i in vertices:
        weight[i] = int(input())

# 2-approximation for minimum-size vertex cover: take vertices in an inclusion-maximal matching
apx = []
taken = [0] * n
for u,v in edges:
    if taken[u] == 0 and taken[v] == 0:
        apx.append(u)
        apx.append(v)
        taken[u] = taken[v] = 1

# setup ILP
ilp = lp.LpProblem("vertex_cover_ilp_kernel", lp.LpMinimize)

# setup variables. the ones in the 2-approximate vertex cover are binary, the others are continuous in [0,1]
x = [None] * n
for v in vertices:
    name = "x" + str(v)
    if taken[v]:
        x[v] = lp.LpVariable(name, cat = 'Binary')
    else:
        x[v] = lp.LpVariable(name, lowBound = 0, upBound = 1, cat = 'Continuous')

# constraints: for each vertex v in the 2-approximate vertex cover we either take v are all its neighbors
for v in apx:
    degree = len(adj[v])
    big_one = lp.LpAffineExpression([(x[v], degree)])
    small_ones = lp.lpSum(x[u] for u in adj[v])
    ilp += lp.lpSum([big_one, small_ones]) >= degree

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
