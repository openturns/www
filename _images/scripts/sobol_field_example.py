from openturns import *
from time import time

print(PlatformInfo.GetRevision())
# First, create a mesh
interval = Interval([-6.0]*2, [6.0]*2)
f = SymbolicFunction(["x0", "x1"], ["1.0 - (1.2 + cos(_pi * x0))^2 - (1.2 + cos(_pi * x1))^2"])
level = 0.0
domain = LevelSet(f, level)
domain.setLowerBound(interval.getLowerBound())
domain.setUpperBound(interval.getUpperBound())
discretization = [31, 31]
# To have a more symmetric mesh
ResourceMap.SetAsBool("IntervalMesher-UseDiamond", True)
mesh = LevelSetMesher(discretization).build(domain, interval)

mesh.exportToVTKFile("domain.vtk")

# Second, a model with functional output
class FUNC(OpenTURNSPythonFunction):
    def __init__(self, mesh, KLBasis, eigenValues):
        super(FUNC, self).__init__(len(eigenValues), mesh.getVerticesNumber())
        self.mesh_ = mesh
        self.KLValues_ = KLBasis
        self.eigenValues_ = eigenValues
        self.nc_ = 0

    def _exec(self, X):
        self.nc_ += 1
        print("nc=", self.nc_, "X=", X)
        values = Point(self.getOutputDimension())
        for i in range(len(X)):
            values += self.KLValues_[i] * (self.eigenValues_[i] * X[i])
        return values

# Covariance model
covariance = SquaredExponential([0.1]*2)

basis = OrthogonalProductPolynomialFactory([HermiteFactory()]*2)
basisSize = 256
experiment = LowDiscrepancyExperiment(SobolSequence(), basis.getMeasure(), 10000)
threshold = 0.0
mustScale = True
print("Build KL quadrature")
Log.Show(Log.INFO)
ResourceMap.SetAsScalar("KarhunenLoeveQuadratureAlgorithm-RegularizationFactor", 1.0e-12)
ResourceMap.SetAsScalar("KarhunenLoeveP1Algorithm-RegularizationFactor", 1.0e-12)
algo = KarhunenLoeveQuadratureAlgorithm(domain, covariance, experiment, basis, basisSize, mustScale, threshold)

algo = KarhunenLoeveP1Algorithm(mesh, covariance, threshold)
algo.run()
result = algo.getResult()
Log.Show(Log.NONE)

F = FUNC(mesh, result.getModesAsProcessSample(), result.getEigenValues())
model = Function(F)

dim = model.getInputDimension()
print("dim=", dim)
# Sobol indices using PCE
# Input distribution
distribution = ComposedDistribution([Normal()]*dim)
# Here we use a tensor-product enumerate function (100.0 ~ inf)
# because we use a Gauss product integration method (low dimension here)
enumerateFunction = EnumerateFunction(dim)
basis = OrthogonalProductPolynomialFactory([HermiteFactory()]*dim, enumerateFunction)

marginalDegree = 3

totalSize = enumerateFunction.getStrataCumulatedCardinal(marginalDegree)
print("basis total size=", totalSize)
print("input total size=", totalSize)
adaptive = FixedStrategy(basis, totalSize)

# Exact projection using Gauss Legendre integration
weightedExperiment = GaussProductExperiment(distribution, [marginalDegree+1]*dim)
inSample, weights = weightedExperiment.generateWithWeights()
print(inSample)
print(distribution.getDimension())
print(weights)
print("inSample size=", inSample.getSize(), "dimension=", inSample.getDimension())
outSample = model(inSample)
projection = IntegrationStrategy(weightedExperiment)

# PCE
algo = FunctionalChaosAlgorithm(inSample, outSample, distribution, adaptive, projection)
t0 = time()
Log.Show(Log.INFO)
algo.run()
print("t=", time() - t0, "s")

# Post-processing
vector = FunctionalChaosRandomVector(algo.getResult())

# Field of Sobol indices
for i in range(dim):
    print("i=", i)
    sobol = Point([vector.getSobolIndex(i, j) for j in range(mesh.getVerticesNumber())])
    field = Field(mesh, [[x] for x in sobol])
    field.exportToVTKFile("Sobol_" + str(i) + "_I_field.vtk")
    graph = field.draw()
    graph.setTitle("Sobol " + str(i))
    graph.draw("Sobol_" + str(i) + "_I_field.png", 600, 610)
