from __future__ import print_function
import openturns as ot
from openturns.viewer import View

# create a collection of distribution
coll = [ot.Beta(1.5, 3.2, 0.0, 1.0),  ot.Beta(2.0, 4.3, 0.5, 1.2)]

# create the distribution
distribution = ot.MaximumEntropyOrderStatisticsDistribution(coll)

def pdf(X):
    return [distribution.computePDF(X)]

graph = ot.PythonFunction(2, 1, pdf).draw(distribution.getRange().getLowerBound(), distribution.getRange().getUpperBound(), [256]*2)
graph.setLegendPosition("bottomright")
graph.setXTitle(r"$x_1$")
graph.setYTitle(r"$x_2$")
graph.setTitle(r"Maximum entropy order statistics distribution iso-PDF")
view = View(graph, (800, 600))
view._ax[0].axis("equal")
view.save("../plot_maximum_entropy_order_statistics_distribution.png")
view.close()
