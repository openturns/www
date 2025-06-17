import openturns as ot
from openturns.viewer import View
from time import time

size = 250

copula1 = ot.ClaytonCopula(3.0)
tau = copula1.getKendallTau()[0, 1]
print("tau=", tau)
copula2 = ot.GumbelCopula(1.0 / (1.0 - tau))
sample = copula1.getSample(size)

graph = ot.VisualTest.DrawKendallPlot(sample, copula1)
graph.add(ot.VisualTest.DrawKendallPlot(sample, copula2).getDrawable(1))
graph.setColors(["red", "green", "blue"])
graph.setLegends(["", "sample vs " + str(copula1), "sample vs " + str(copula2)])
graph.setLegendPosition("bottomright")
graph.setTitle("Copula assessment using Kendall plot")
graph.setXTitle(r"$x$")
graph.setYTitle(r"$y$")
view = View(graph, (800, 600))
view._ax[0].axis("equal")
view.save("../plot_kendall_plot.png")
view.close()
