import openturns as ot
from openturns.viewer import View
from math import pi, sqrt
from time import time

ot.ResourceMap.SetAsUnsignedInteger( "OptimizationAlgorithm-DefaultMaximumIterationNumber", 10000 )
ot.ResourceMap.SetAsUnsignedInteger( "OptimizationAlgorithm-DefaultMaximumCallsNumber", 1000000)

level = -4
N = 50

p = 1
def buildFormula(c, j):
    formula = ""
    for i in range(len(c)):
        if i>0:
            formula += " + "
        formula += "(x" + str(i) + "-(" + str(c[i]) + "))^" + str(2*(p + j))
    return formula

points = [[1.0, 0.0, -1.0 / sqrt(2.0)], [-1.0, 0.0, -1.0 / sqrt(2.0)], [0.0, 1.0, 1.0 / sqrt(2.0)], [0.0, -1.0, 1.0 / sqrt(2.0)]]
formula = ""
for i in range(len(points)):
    if (i>0):
        formula += "  +  "
    formula += "1.0/(" + buildFormula(points[i], i) + ")"

print(formula)
f = ot.SymbolicFunction(["x0", "x1", "x2"], ["-(" + formula + ")"])

ls = ot.LevelSet(f, ot.Less(), level)
print("build mesh")
t0 = time()
mesh1 = ot.LevelSetMesher([N]*3).build(ls, ot.Interval([-2.5]*3, [2.5]*3), False)
print("t (mesh1)=", time() - t0, "s")
mesh2 = ot.LevelSetMesher([3*N]*3).build(ls, ot.Interval([-2.5]*3, [2.5]*3), True)
print("t (mesh1+mesh2)=", time() - t0, "s")
print("mesh1=", mesh1.getVerticesNumber(), "vertices and", mesh1.getSimplicesNumber(), "simplices")
print("mesh2=", mesh2.getVerticesNumber(), "vertices and", mesh2.getSimplicesNumber(), "simplices")
print("draw mesh")
t0 = time()
graph = mesh1.draw3D(True, pi/16, 0, pi/4, False, 1.0)
mesh2.setVertices(mesh2.getVertices() + ot.Point([-4.0, 0.0, 0.0]))
ot.ResourceMap.SetAsScalar("Mesh-AmbientFactor", 0.1)
ot.ResourceMap.SetAsScalar("Mesh-DiffuseFactor", 0.6)
ot.ResourceMap.SetAsScalar("Mesh-SpecularFactor", 0.3)
ot.ResourceMap.SetAsScalar("Mesh-Shininess", 100.0)
graph.add(mesh2.draw3D(False, pi/16, 0, pi/4, True, 1.0))
graph.setTitle("3D mesh of implicit domains (with and without shading)")
graph.setXTitle(r"")
graph.setYTitle(r"")
graph.setGrid(False)
graph.setAxes(False)
print("t=", time() - t0, "s")

print("export")
t0 = time()
view = View(graph, (1200, 600))
view._ax[0].axis("equal")
view.save("../plot_3d_mesh.png")
view.close()
print("Matplotlib=", time() - t0, "s")
