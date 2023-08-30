"""
Script to produce the calibration figure on the www front page.
Adapted from:
https://openturns.github.io/openturns/latest/auto_calibration/least_squares_and_gaussian_calibration/plot_calibration_flooding.html
"""

# %%
from openturns.usecases import flood_model
from matplotlib import pylab as plt
import openturns.viewer as otv
import numpy as np
import openturns as ot

ot.ResourceMap.SetAsUnsignedInteger("Normal-SmallDimension", 1)
ot.Log.Show(ot.Log.NONE)

fm = flood_model.FloodModel()
Qobs = fm.data[:, 0]
Hobs = fm.data[:, 1]
nbobs = fm.data.getSize()
fm.data

# %%


def functionFlooding(X):
    L = 5.0e3
    B = 300.0
    Q, K_s, Z_v, Z_m = X
    alpha = (Z_m - Z_v) / L
    if alpha < 0.0 or K_s <= 0.0:
        H = np.inf
    else:
        H = (Q / (K_s * B * np.sqrt(alpha))) ** (3.0 / 5.0)
    return [H]


g = ot.PythonFunction(4, 1, functionFlooding)
g = ot.MemoizeFunction(g)
g.setInputDescription(["Q ($m^3/s$)", "Ks ($m^{1/3}/s$)", "Zv (m)", "Zm (m)"])
g.setOutputDescription(["H (m)"])

KsInitial = 20.0
ZvInitial = 49.0
ZmInitial = 51.0
thetaPrior = [KsInitial, ZvInitial, ZmInitial]

calibratedIndices = [1, 2, 3]
mycf = ot.ParametricFunction(g, calibratedIndices, thetaPrior)


sigmaH = 0.5  # (m^2)
errorCovariance = ot.CovarianceMatrix(1)
errorCovariance[0, 0] = sigmaH**2
sigmaKs = 5.0
sigmaZv = 1.0
sigmaZm = 1.0
#
sigma = ot.CovarianceMatrix(3)
sigma[0, 0] = sigmaKs**2
sigma[1, 1] = sigmaZv**2
sigma[2, 2] = sigmaZm**2


algo = ot.GaussianNonLinearCalibration(
    mycf, Qobs, Hobs, thetaPrior, sigma, errorCovariance
)

# %%
algo.run()
calibrationResult = algo.getResult()

# %%
thetaMAP = calibrationResult.getParameterMAP()
distributionPosterior = calibrationResult.getParameterPosterior()


# %%
print(ot.ResourceMap.GetAsUnsignedInteger("GaussianNonLinearCalibration-BootstrapSize"))

ot.ResourceMap.SetAsUnsignedInteger("GaussianNonLinearCalibration-BootstrapSize", 0)
algo = ot.GaussianNonLinearCalibration(
    mycf, Qobs, Hobs, thetaPrior, sigma, errorCovariance
)
algo.run()
calibrationResult = algo.getResult()
grid = calibrationResult.drawParameterDistributions()

graph = grid.getGraph(0, 0)
graph.setLegends(["Prior", "Posterior"])

figure_width_in_pixels = 400
figure_height_in_pixels = 280
dpi = 90
figure_width_in_inches = figure_width_in_pixels / dpi
figure_height_in_pixels = figure_height_in_pixels / dpi


view = otv.View(
    graph,
    figure_kw={
        "figsize": (figure_width_in_inches, figure_height_in_pixels),
        "dpi": dpi,
    },
    legend_kw={"bbox_to_anchor": (1.0, 1.0), "loc": "upper left"},
)
plt.subplots_adjust(right=0.7, left=0.25, bottom=0.25)
view.save("../../_static/img/calibration.png", dpi=dpi)
