from __future__ import print_function
import openturns as ot
from openturns.viewer import View

# Generate some data
size = 250
sample = ot.LogNormal(0.0, 0.4).getSample(size)

# Estimate the distribution
parametric_estimate = ot.LogNormalFactory().build(sample)
nonparametric_estimate = ot.KernelSmoothing().build(sample)

# Draw a non parametric estimate and the parametric estimate
graph = parametric_estimate.drawPDF(0.0, 4.0)
graph.add(nonparametric_estimate.drawPDF(0.0, 4.0))
graph.add(ot.Cloud(sample, ot.Sample(size, 1)))
graph.setLegendPosition("topright")
graph.setXTitle(r"$x$")
graph.setYTitle(r"$p_X$")
graph.setTitle(r"Parametric vs nonparametric estimation")
graph.setColors(["red", "blue", "green"])
graph.setLegends(["parametric", "nonparametric", "data"])
view = View(graph, (800, 600))
view.save("../plot_distribution_fitting.png")
view.close()
