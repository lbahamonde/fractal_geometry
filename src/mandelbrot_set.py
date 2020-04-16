"""Calculates the set of complex points defined as the Mandelbrot set

    References
    ----------
    https://scipy-lectures.org/intro/numpy/auto_examples/plot_mandelbrot.html
"""
import numpy as np
from numpy import newaxis
from matplotlib import pyplot as plt


class MandelbrotSet(object): # inherit from abc to make it a collection?
    def __init__(self, maxRecurrence, boundnessThreshold):
        self.maxRecurrence = maxRecurrence
        self.boundnessThreshold = boundnessThreshold

    def iterateTilMax(self, c):
        z = c
        for _ in range(self.maxRecurrence):
            z = z**2 + c
        return z

    def areContained(self, c):
        return abs(self.iterateTilMax(c)) < self.boundnessThreshold # why abs value? cause complex numbers aren't larger or smaller

    def intersection(self, c):
        return c[self.areContained(c)] # intersect all the points to return only the ones within the Mandelbrot set

class Point2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle(object):
    def __init__(self, bottomLeftVertexCoords, topRightVertexCoords):
        self.bottomLeftVertex = Point2D(*bottomLeftVertexCoords)
        self.topRightVertex = Point2D(*topRightVertexCoords)

    @property
    def left(self):
        return self.bottomLeftVertex.x

    @property
    def right(self):
        return self.topRightVertex.x

    @property
    def bottom(self):
        return self.bottomLeftVertex.y

    @property
    def top(self):
        return self.topRightVertex.y

    @property
    def extent(self):
        return self.left, self.right, self.bottom, self.top

class RectangularGrid(object):
    def __init__(self, rectangle):
        self.rectangle = rectangle

    def seed(self, numSeedsLength, numSeedsHeight):
        self.numSeedsLength = numSeedsLength
        self.numSeedsHeight = numSeedsHeight

    def mesh(self):
        self.lengthSeeds = np.linspace(self.rectangle.left, self.rectangle.right, self.numSeedsLength)

        self.heightSeeds = np.linspace(self.rectangle.bottom, self.rectangle.top, self.numSeedsHeight)

    def asComplexPts(self):
        return self.lengthSeeds[:, newaxis] + 1j * self.heightSeeds[newaxis, :]

class MandelbrotImage(object):
    def __init__(self, grid, mset):
        self.grid = grid
        self.mset = mset
        self.fig, self.ax = plt.subplots()

    def intersectGridWithMandelbrotSet(self):
        return self.mset.areContained(self.grid.asComplexPts())

    def plot(self):
        self.ax.imshow(self.intersectGridWithMandelbrotSet().T,
                       cmap = 'gray',
                       extent=self.grid.rectangle.extent) # what is the T for?

    def turnOffTicks(self):
        self.ax.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False)
        self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

    def show(self):
        self.turnOffTicks()
        self.fig.tight_layout()
        plt.show()


def main(bottomLeftVertexCoords, topRightVertexCoords, numSeedsLength, numSeedsHeight, maxRecurrence=50, boundnessThreshold=2.0):
    # a grid of c-values
    boundingBox = Rectangle(bottomLeftVertexCoords, topRightVertexCoords)
    grid = RectangularGrid(boundingBox)
    grid.seed(numSeedsLength, numSeedsHeight)
    grid.mesh()

    # Mandelbrot iteration
    mset = MandelbrotSet(maxRecurrence, boundnessThreshold)

    # plot Mandelbrot image
    mimg = MandelbrotImage(grid, mset)
    mimg.plot()
    mimg.show()

if __name__ == "__main__":
    main(bottomLeftVertexCoords=(-2, -1.5), topRightVertexCoords=(1, 1.5), numSeedsLength=12001, numSeedsHeight=10001)