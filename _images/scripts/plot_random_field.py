import openturns as ot
from openturns.viewer import View
from time import time

N = 30
interval = ot.Interval([0.0, 0.0], [3.5, 5.0])

def flow(X):
    Y0 = X[0]
    Y1 = X[1]
    dY0 = 0.5 * Y0 * (2.0 - Y1)
    dY1 = 0.5 * Y1 * (Y0 - 1.0)
    return [dY0, dY1]

phi_func = ot.PythonFunction(2, 2, flow)

# Create the mesh
discretization = [N]*2
mesh = ot.IntervalMesher(discretization).build(interval)

# Covariance model
covariance = ot.TensorizedCovarianceModel([ot.SquaredExponential([0.2]*2, [0.3])]*2)
trend = ot.TrendTransform(phi_func, mesh)
process = ot.GaussianProcess(trend, covariance, mesh)
field = process.getRealization()
f = ot.P1LagrangeEvaluation(field)
ot.ResourceMap.SetAsUnsignedInteger("Field-LevelNumber", 64)
ot.ResourceMap.SetAsScalar("Field-ArrowRatio", 0.01)
ot.ResourceMap.SetAsScalar("Field-ArrowScaling", 0.03)
graph = field.draw()
print("f=", f.getInputDimension(), "->", f.getOutputDimension())
phi = ot.ValueFunction(f, mesh)
solver = ot.RungeKutta(phi)
initialState = [0.5, 1.0]
timeGrid = ot.RegularGrid(0.0, 0.1, 10000)
result = solver.solve(initialState, timeGrid)
print(result)
curve = ot.Curve(result)
curve.setColor("red")
curve.setLineWidth(2)
graph.add(curve)
graph.setTitle("Perturbed Lotka-Voltera system")
graph.setXTitle(r"$x$")
graph.setYTitle(r"$y$")
view = View(graph, (800, 600))
view.save("../plot_random_field.png")
view.close()
