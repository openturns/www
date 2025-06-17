import openturns as ot
import openturns.viewer as otv
from time import time

print(ot.PlatformInfo.GetRevision())
# First, create a mesh
interval = ot.Interval([-6.0]*2, [6.0]*2)
f = ot.SymbolicFunction(["x0", "x1"], ["1.0 - (1.2 + cos(pi_ * x0))^2 - (1.2 + cos(pi_ * x1))^2"])
level = 0.0
domain = ot.LevelSet(f, ot.Less(), level)
domain.setLowerBound(interval.getLowerBound())
domain.setUpperBound(interval.getUpperBound())
discretization = [31, 31]
# To have a more symmetric mesh
ot.ResourceMap.SetAsBool("IntervalMesher-UseDiamond", True)
mesh = ot.LevelSetMesher(discretization).build(domain, interval)

mesh.exportToVTKFile("domain.vtk")

# Second, a model with functional output
class FUNC(ot.OpenTURNSPythonFunction):
    def __init__(self, mesh, KLBasis, eigenValues):
        super(FUNC, self).__init__(len(eigenValues), mesh.getVerticesNumber())
        self.mesh_ = mesh
        self.KLValues_ = KLBasis
        self.eigenValues_ = eigenValues
        self.nc_ = 0

    def _exec(self, X):
        Xp = ot.Point(X)
        self.nc_ += 1
        print("nc=", self.nc_, "X=", Xp)
        values = ot.Point(self.getOutputDimension())
        for i in range(len(X)):
            values += self.KLValues_[i].asPoint() * (self.eigenValues_[i] * Xp[i])
        return values

# Covariance model
covariance = ot.SquaredExponential([0.1]*2)

basis = ot.OrthogonalProductPolynomialFactory([ot.HermiteFactory()]*2)
basisSize = 256
experiment = ot.LowDiscrepancyExperiment(ot.SobolSequence(), basis.getMeasure(), 10000)
threshold = 0.0
mustScale = True
print("Build KL quadrature")
ot.Log.Show(ot.Log.INFO)
ot.ResourceMap.SetAsScalar("KarhunenLoeveQuadratureAlgorithm-RegularizationFactor", 1.0e-12)
ot.ResourceMap.SetAsScalar("KarhunenLoeveP1Algorithm-RegularizationFactor", 1.0e-12)
#algo = ot.KarhunenLoeveQuadratureAlgorithm(domain, interval, covariance, experiment, basis, mustScale, threshold)

algo = ot.KarhunenLoeveP1Algorithm(mesh, covariance, threshold)
algo.setNbModes(5)
algo.run()
result = algo.getResult()
ot.Log.Show(ot.Log.NONE)

F = FUNC(mesh, result.getModesAsProcessSample(), result.getEigenvalues())
model = ot.Function(F)

dim = model.getInputDimension()
print("dim=", dim)
# Sobol indices using PCE
# Input distribution
distribution = ot.JointDistribution([ot.Normal()]*dim)
# Here we use a tensor-product enumerate function (100.0 ~ inf)
# because we use a Gauss product integration method (low dimension here)
enumerateFunction = ot.LinearEnumerateFunction(dim)
basis = ot.OrthogonalProductPolynomialFactory([ot.HermiteFactory()]*dim, enumerateFunction)

marginalDegree = 3

totalSize = enumerateFunction.getStrataCumulatedCardinal(marginalDegree)
print("basis total size=", totalSize)
print("input total size=", totalSize)
adaptive = ot.FixedStrategy(basis, totalSize)

# Exact projection using Gauss Legendre integration
weightedExperiment = ot.GaussProductExperiment(distribution, [marginalDegree+1]*dim)
inSample, weights = weightedExperiment.generateWithWeights()
print(inSample)
print(distribution.getDimension())
print(weights)
print("inSample size=", inSample.getSize(), "dimension=", inSample.getDimension())
outSample = model(inSample)
projection = ot.IntegrationStrategy(weightedExperiment)

# PCE
algo = ot.FunctionalChaosAlgorithm(inSample, outSample, distribution, adaptive, projection)
t0 = time()
ot.Log.Show(ot.Log.INFO)
algo.run()
print("t=", time() - t0, "s")

# Post-processing
sensitivity = ot.FunctionalChaosSobolIndices(algo.getResult())

# Field of Sobol indices
for i in range(dim):
    print("i=", i)
    sobol = ot.Point([sensitivity.getSobolIndex(i, j) for j in range(mesh.getVerticesNumber())])
    field = ot.Field(mesh, [[x] for x in sobol])
    field.exportToVTKFile("Sobol_" + str(i) + "_I_field.vtk")
    graph = field.draw()
    graph.setTitle("Sobol " + str(i))
    view = otv.View(graph)
    view.save("Sobol_" + str(i) + "_I_field.png")
