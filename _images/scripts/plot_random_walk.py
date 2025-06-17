import openturns as ot
from openturns.viewer import View
from time import time

size = 20000
randomWalk = ot.RandomWalk([0.0]*2, ot.Normal(2), ot.RegularGrid(0, 1, size))

graph = randomWalk.getRealization().draw()
graph.setColors(["red"])

graph.setTitle("2D random walk")
graph.setXTitle(r"$x$")
graph.setYTitle(r"$y$")
view = View(graph, (800, 600))
view._ax[0].axis("equal")
view.save("../plot_random_walk.png")
view.close()
