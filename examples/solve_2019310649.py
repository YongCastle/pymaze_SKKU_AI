from __future__ import absolute_import
#ADD (Path Error로 인해 추가)
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.maze_manager import MazeManager
from src.maze import Maze


if __name__ == "__main__":

     # 각 시행의 Cost를 저장한다.
    uniform_sol_costs=list()                                
    a_star_sol_costs=list()                               

     # 각 시행의 소모시간을 저장한다.
    uniform_sol_times=list()
    a_star_sol_times=list()

    # 각 시행의 Solution 경로를 저장한다.
    uniform_sol_paths=list()
    a_star_sol_paths=list()

    for i in range(10):

        # Create the manager
        manager = MazeManager()

        # Add a 10x10 maze to the manager
        maze1 = manager.add_maze(20, 20)
    
        """---------------------Uniform_Cost_Search Soltion---------------------"""
        manager.solve_maze(maze1.id, "UniformCostSearch")

        uniform_sol_costs.append(maze1.solution_cost1)
        uniform_sol_times.append(maze1.solution_time1)
        uniform_sol_paths.append(maze1.solution_path)

        # Display the maze
        #manager.show_maze(maze1.id)

        # solution 애니메이션 visualize
        #manager.show_solution_animation(maze1.id)

        # 결과 show
        #manager.show_solution(maze1.id)

        """---------------------A_Star_Search Soltion---------------------"""
        # 각 셀들을 방문했다는 표식을 전부 False로 바꾸는 코드, Maze1을 다시 쓰기 때문에 추가하였다.
        for i in range(maze1.num_rows):
            for j in range(maze1.num_cols):
                maze1.grid[i][j].visited=False

        maze1.solution_path=None

        manager.solve_maze(maze1.id, "AStarSearch")

        a_star_sol_costs.append(maze1.solution_cost2)
        a_star_sol_times.append(maze1.solution_time2)
        a_star_sol_paths.append(maze1.solution_path)
        

        # solution 애니메이션 visualize
        #manager.show_solution_animation(maze1.id)

        # 결과 show
        #manager.show_solution(maze1.id)


    sum_uniform_sol_cost = 0
    sum_a_star_sol_cost = 0
    sum_uniform_sol_time = 0.0
    sum_a_star_sol_time = 0.0


    print("|---------------------------------------------------------------|")
    print("|-----------------------Solution Cost Tabel---------------------|")
    print("|---++----------------------------++----------------------------|")
    print("|IDX||-------------COST---------- ||-------------TIME---------- |")
    print("|---++--------------+-------------++--------------+-------------|")
    print("|IDX|| Uniform_Cost | A_STAR_COST || Uniform_TIME | A_STAR_TIME |")
    print("|---++--------------+-------------++--------------+-------------|")
    for i in range(len(uniform_sol_costs)) :
        print('|{:>3d}|| {:>12d} | {:>11d} || {:>12.4f} | {:>11.4f} |'.format(i+1,uniform_sol_costs[i], a_star_sol_costs[i],uniform_sol_times[i], a_star_sol_times[i]))
        sum_uniform_sol_cost += uniform_sol_costs[i]
        sum_a_star_sol_cost  += a_star_sol_costs[i]
        sum_uniform_sol_time += uniform_sol_times[i]
        sum_a_star_sol_time  += a_star_sol_times[i]
    print("|---++--------------+-------------++--------------+-------------|")
    avg_uniform_sol_cost = sum_uniform_sol_cost / len(uniform_sol_costs)
    avg_a_star_sol_cost = sum_a_star_sol_cost/ len(uniform_sol_costs)
    avg_uniform_sol_time = sum_uniform_sol_time/ len(uniform_sol_costs)
    avg_a_star_sol_time = sum_a_star_sol_time/ len(uniform_sol_costs)
    print('|AVG|| {:>12.2f} | {:>11.2f} || {:>12.4f} | {:>11.4f} |'.format(avg_uniform_sol_cost, avg_a_star_sol_cost,avg_uniform_sol_time, avg_a_star_sol_time))
    print("|---++--------------+-------------++--------------+-------------|")
    print("|---------------------------------------------------------------|")
