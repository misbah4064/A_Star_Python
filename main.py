__author__ = 'misbah'
class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self,from_node, to_node):
        return 1

import Board

rows = Board.rows
cols = Board.cols
Width = Board.Width
start = Board.player
goal = Board.end

#start, goal = (0, 0), (3, 2)

diagram1 = SquareGrid(cols,rows)
diagram1.walls = Board.Walls# [(1, 2), (1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
import heapq
import threading

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    openLoop = PriorityQueue()
    openLoop.put(start,0)
    closedLoop = []
    came_from = {}
    cost_so_far = {}
    cost_so_far[start] = 0
    came_from[start] = None

    while not openLoop.empty():
        current = openLoop.get()
        #print ("current = ", current)

        if current == goal:
            print ("goal reached")
            break
        for next in graph.neighbors(current):
            tentative_cost = cost_so_far[current] + graph.cost(current,next)
            if next not in cost_so_far or tentative_cost < cost_so_far[next]:
                cost_so_far[next] = tentative_cost
                priority = tentative_cost = heuristic(goal, next)
                openLoop.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


came_from, cost_so_far = a_star_search(diagram1, start, goal)
total_path = reconstruct_path(came_from, start, goal)
#print (total_path)

def run():
    global total_path
    Board.render_path(total_path)

t = threading.Thread(target=run)
t.daemon = True
t.start()
Board.start_game()
