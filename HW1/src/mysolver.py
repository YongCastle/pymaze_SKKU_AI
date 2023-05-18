import math
from queue import PriorityQueue
import time
import random
import logging
from src.maze import Maze

logging.basicConfig(level=logging.DEBUG)


class Solver(object):
    """Base class for solution methods.
    Every new solution method should override the solve method.

    Attributes:
        maze (list): The maze which is being solved.
        neighbor_method:
        quiet_mode: When enabled, information is not outputted to the console

    """

    def __init__(self, quiet_mode):
        logging.debug("Class Solver ctor called")

        self.name = ""
        self.quiet_mode = quiet_mode

    def solve(self):
        logging.debug('Class: Solver solve called')
        raise NotImplementedError

    def get_name(self):
        logging.debug('Class Solver get_name called')
        raise self.name

    def get_path(self):
        logging.debug('Class Solver get_path called')
        return self.path

class UniformCostSearch():
    
    """brute-force는 무작위로 이웃 셀을 주는 method이고, fancy는 목표와 가까운 이웃 셀을 주는 method이다."""
    def __init__(self):
        logging.debug('Class uniform_cost_search ctor called')

        self.name = "Uniform Cost Search Algoritm"
        

    def uniform_cost_search(self, maze):

        logging.debug("Class uniform_cost_search solve called")


        priority_queue = PriorityQueue()                                    # 우선순위 큐로 구현 (O(logn)의 시간복잡도를 가짐. (cf. list는 O(n)))
        priority_queue.put((0, maze.entry_coor))                            # 시작 위치의 cell을 큐에 입력, 시작위치는 g=0
        path = list()                                                       # To track path of solution cell coordinates

        print("\nSolving the maze with Uniform-Cost search...")
        time_start = time.perf_counter()

        while True:                                                         # Loop until return statement is encountered
            while priority_queue:                                           # While still cells left to search on current level
                stack, (k_curr, l_curr) = priority_queue.get()              # Search one cell on the current level
                maze.grid[k_curr][l_curr].visited = True                    # Mark current cell as visited
                path.append(((k_curr, l_curr), False))                      # Append current cell to total search path

                if (k_curr, l_curr) == maze.exit_coor:                      # Exit if current cell is exit cell
                    if True:
                        print("Number of moves performed: {}".format(len(path)))
                        time_cost = time.perf_counter() - time_start
                        print("Execution time for algorithm: {:.4f}".format(time_cost))
                    return len(path),path,time_cost                         # Return cost,path,time

                neighbour_coors = maze.find_neighbours(k_curr, l_curr)  # Find neighbour indicies
                neighbour_coors = maze.validate_neighbours_solve(neighbour_coors, k_curr,
                                                                  l_curr, maze.exit_coor[0],
                                                                  maze.exit_coor[1], "brute-force")

                if neighbour_coors is not None:
                    for coor in neighbour_coors:
                        priority_queue.put((stack+1,coor))                  # 이웃 셀을 우선순위 큐에 추가한다. (시작위치까지의 거리가 증가하므로 stack +1)

        logging.debug("Class uniform_cost_search leaving solve")

class AStarSearch(Solver):
    
    def __init__(self):
        logging.debug('Class A Star Search ctor called')

        self.name = "A* Search Algoritm"

    def heuristic(self, coor, exit_coor) :
        """
        목표 위치의 시작 위치와 비용. 휴리스틱 기능을 위해 유클리드 거리를 사용하십시오.
        Return = dist_to_target : (k_n, l_n) 과 END cell 까지의 거리
        """
        (k_n, l_n) = coor                                                         
        (k_end, l_end) = exit_coor
        dist_to_target = math.sqrt((k_n - k_end) ** 2 + (l_n - l_end) ** 2)             #유클리드 거리 계산을 위해 Math 함수의 sqrt를 사용한다.
        return dist_to_target                                                           #coor에서 출구까지의 유클리드 거리를 반환한다.

    def a_star_search(self, maze):

        logging.debug("Class a_star_search solve called")

        priority_queue = PriorityQueue()                                                # 우선순위 큐로 구현 (O(logn)의 시간복잡도를 가짐. (cf. list는 O(n)))
        g = 0                                                                           
        h = self.heuristic(maze.entry_coor, maze.exit_coor)                             # h는 휴리스틱 함수로 '현재 위치에서 출구까지의 유클리드 거리이다.'
        priority_queue.put((g + h, g, maze.entry_coor))                                 # 큐의 구조 (g + h, g, (현재위치))                
        path = list()                                                                   # To track path of solution cell coordinates
        print("\nSolving the maze with A_star_search...")
        time_start = time.perf_counter()                                                # Error발생으로 인해 time.perf_counter을 사용하였다.
        while True:                                                                     # Loop until return statement is encountered
            while priority_queue:                                                       # While still cells left to search on current level
                
                g , (k_curr, l_curr) = priority_queue.get()[1:]                         
                maze.grid[k_curr][l_curr].visited = True                                # Mark current cell as visited
                path.append(((k_curr, l_curr), False))                                  # Append current cell to total search path

                if (k_curr, l_curr) == maze.exit_coor:                                  # Exit if current cell is exit cell
                    if True:
                        print("Number of moves performed: {}".format(len(path)))
                        time_cost = time.perf_counter() - time_start
                        print("Execution time for algorithm: {:.4f}".format(time_cost))
                    return len(path),path,time_cost                                     # Return COST, PATH, TIME

                neighbour_coors = maze.find_neighbours(k_curr, l_curr)                  # Find neighbour indicies
                neighbour_coors = maze.validate_neighbours_solve(neighbour_coors, k_curr,
                                                                  l_curr, maze.exit_coor[0],
                                                                  maze.exit_coor[1], "brute-force")

                if neighbour_coors is not None:
                    for coor in neighbour_coors:
                        h = self.heuristic(coor, maze.exit_coor)                        # 다음 셀의 휴리스틱 함수를 계산한다.
                        priority_queue.put((g + 1 + h, g+1, coor))                      # 이웃 셀을 우선순위 큐에 추가한다. 구조는 (f,g,현재위치)이다.                

        logging.debug("Class uniform_cost_search leaving solve")
