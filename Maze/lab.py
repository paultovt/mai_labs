import numpy as np
import turtle

class Maze:
    def __init__(self, maze, point):
        self.step_set = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        self.maze = maze
        self.length, self.width = maze.shape
        self.init_maze()
        self.maze = self.find_next_step(self.maze, point)

    def init_maze(self):
        length, width = self.maze.shape
        maze_0 = np.zeros(shape=(length, width))
        maze_0[::2, ::2] = 1
        maze = np.where(self.maze < 0, self.maze, maze_0)
        self.maze = maze

    def find_next_step(self, maze, point):
        step_set = np.random.permutation(self.step_set)
        for next_step in step_set:
            next_point = point + next_step * 2
            x, y = next_point
            if 0 <= x < self.length and 0 <= y < self.width:
                if maze[x, y] == 1: 
                    maze[x, y] = 2
                    maze[(point + next_step)[0], (point + next_step)[1]] = 2
                    maze = self.find_next_step(maze, next_point)
        return maze

size = 35

if __name__ == '__main__':
    maze = np.zeros((size, size))
    start_point=np.array([0, 0])
    maze=Maze(maze, start_point)
    maze.maze -= 3
    while True:
        start = np.random.randint(size)
        #start = 0
        if maze.maze[start][0] == -1:
            maze.maze[start][0] = 0
            break
    while True:
        end = np.random.randint(size)
        #end = size - 1
        if maze.maze[end][size-1] == -1:
            maze.maze[end][size-1] = -2
            break

    c = 0
    done = False
    while True:
        if done:
            break
        x, y = np.where(maze.maze == c)
        c += 1
        for t_x, t_y in zip(x, y):
            if done:
                break
            for r_x in [t_x - 1, t_x, t_x + 1]:
                if done:
                    break
                for r_y in [t_y - 1, t_y, t_y + 1]:
                    if (r_y == t_y and r_x == t_x) or (r_y == t_y - 1 and r_x == t_x - 1) or (r_y == t_y + 1 and r_x == t_x - 1) or (r_y == t_y - 1 and r_x == t_x + 1) or (r_y == t_y + 1 and r_x == t_x + 1) or r_y < 0 or r_y >= size or r_x < 0 or r_x >= size:
                        continue
                    if maze.maze[r_x][r_y] == -2:
                        maze.maze[r_x][r_y] = c
                        done = True
                        break
                    if maze.maze[r_x][r_y] == -1:
                        maze.maze[r_x][r_y] = c

    way_x, way_y = [], []
    t_y, t_x = size - 1, end
    for i in range(c, -1, -1):
        for r_x in [t_x - 1, t_x, t_x + 1]:
            for r_y in [t_y - 1, t_y, t_y + 1]:
                if (r_y == t_y and r_x == t_x) or (r_y == t_y - 1 and r_x == t_x - 1) or (r_y == t_y + 1 and r_x == t_x - 1) or (r_y == t_y - 1 and r_x == t_x + 1) or (r_y == t_y + 1 and r_x == t_x + 1) or r_y < 0 or r_y >= size or r_x < 0 or r_x >= size:
                    continue
                if maze.maze[r_x][r_y] == i - 1:
                    way_x.append(r_x)
                    way_y.append(r_y)
                    t_x, t_y = r_x, r_y

    way_x.reverse()
    way_y.reverse()

    screen = turtle.Screen()
    screen.title("Maze")
    screen.bgcolor("black")
    screen.setup((size + 2) * 20, (size + 2) * 20)
    screen.tracer(0)
    pen = turtle.Turtle()
    pen.shape("square")
    pen.color("white")
    pen.speed(0)
    pen.up()
    for y in range(size):
        for x in range(size):
            if maze.maze[y][x] > -3:
                pen.goto(size * 20 / 2 * -1 + x * 20, size * 20 / 2 - y * 20)
                pen.stamp()

    screen.tracer(1)
    pen.shape("square")
    pen.shapesize(5/6,5/6)
    pen.color("red")
    pen.goto(size * 20 / 2 - 20, size * 20 / 2 - end * 20)
    pen.stamp()
    pen.color("green")
    pen.goto(size * 20 / 2 * -1, size * 20 / 2 - start * 20)
    pen.stamp()
    pen.shape("circle")
    pen.shapesize(2/3,2/3)
    pen.color("blue")
    pen.pensize(7)
    pen.speed(7)
    pen.down()
    for x, y in zip(way_x, way_y):
        pen.goto(size * 20 / 2 * -1 + y * 20, size * 20 / 2 - x * 20)
    pen.goto(size * 20 / 2 - 20, size * 20 / 2 - end * 20)
    turtle.done()

