from turtle import Screen, Turtle, bgcolor, title # draw
from turtle import ontimer, getcanvas, done # record

class DarkThemedScreen(object):
    def __init__(self):
        self.screen = Screen()
        self.darkScreen()

    def darkScreen(self):
        bgcolor('black')
        title('Fractal tree of turtle leaves')

    def redTurtlePen(self):
        cursor = Turtle()
        cursor.fillcolor("red")
        cursor.pencolor("red")

        cursor.shapesize(0.6, 0.6, 0.6) # stretch length, stretch width, outlinewidth
        cursor.shape('turtle')
        cursor.pensize(3)
        return cursor

    def exitOnClick(self):
        self.screen.exitonclick()


class FractalTreePath:
    def __init__(self, cursor):
        self.cursor = cursor
        self.branchingAngleInDeg = 20
        self.minimumBranchLength = 2
        self.branchLengthReduction = 15

    def goToOrigin(self):
        self.cursor.left(90)
        self.cursor.up() # no line will be drawn when it moves
        self.cursor.backward(100)
        self.cursor.down() # a line will be drawn when its moves

    def hasChildBranches(self, branchLength):
        return branchLength > self.minimumBranchLength

    def stampLeaf(self):
        self.cursor.stamp()

    def branchOutRight(self, branchLength):
        self.cursor.right(self.branchingAngleInDeg)
        self.walk(branchLength-self.branchLengthReduction)

    def branchOutLeft(self, branchLength):
        self.cursor.left(2*self.branchingAngleInDeg)
        self.walk(branchLength-self.branchLengthReduction)

    def backToParentNode(self, branchLength):
        self.cursor.right(self.branchingAngleInDeg)
        self.cursor.backward(branchLength)

    def walk(self, branchLength):
        if self.hasChildBranches(branchLength):
            self.cursor.forward(branchLength)
            self.branchOutRight(branchLength)
            self.branchOutLeft(branchLength)
            self.backToParentNode(branchLength)
        else:
            self.stampLeaf()


def draw():
    screen = DarkThemedScreen()
    cursor = screen.redTurtlePen()
    cursor.speed(10)

    path = FractalTreePath(cursor)
    path.goToOrigin()
    path.walk(branchLength=100)

    screen.exitOnClick()

running = True
FRAMES_PER_SECOND = 10

def stop():
    global running

    running = False

def save(counter=[1]):
    getcanvas().postscript(file = "tree-walk-{0:03d}.eps".format(counter[0]))
    counter[0] += 1
    if running:
        ontimer(save, int(1000 / FRAMES_PER_SECOND))

def main():
    save()  # start the recording
    ontimer(draw, 500)  # start the program (1/2 second leader)
    done()

if __name__ == '__main__':
    main()