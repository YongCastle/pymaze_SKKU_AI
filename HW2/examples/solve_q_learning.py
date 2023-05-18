from __future__ import absolute_import
import os
import sys
import shutil

from matplotlib import colors, pyplot as plt
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.maze import Maze
from src.maze_manager import MazeManager
from src.debug_viz import DebugViz

#============+====================================================================#
# Task 1 & 2 | Create Function about Q-Learning : q_learning & q_learning_path    #
#============+====================================================================#
from src.q_learning_manager import QLearningManager
print("============================")
print("     Task 1,2 Complete")
print("============================")

shutil.rmtree('./temp')
shutil.rmtree('./output')

#========+===================================================================#
# Task 3 | Train 3 randomly generated 20x20 mazes with Visualization         #
#========+===================================================================#
maze_row, maze_col = 20, 20
manager = MazeManager()
maze_list = []
solver_list = []

for i in range(3):
    maze = manager.add_maze(maze_row, maze_col)
    maze_list.append(maze)
    solver = QLearningManager(maze)
    debugViz = DebugViz()
    debugViz.set_filename("maze{}_generation_20x20".format(i))
    solver_list.append(solver)
    debugViz.show_maze(maze, display_mode=False)

# Define the image file names and paths
manager.combine_images('temp', 'generation', 'maze_output1.png', 'down')

print("============================")
print("     Task 3 Complete")
print("============================")


#========+================================================================================================#
# Task 4 | Implement the Q-Learning-based maze traversal algorithm for the randomly generated 20x20 mazes #
#========+================================================================================================#
solution_path_list = []
solution_cost_list = []
solution_q_table = []

debugViz = DebugViz()
for i in range(3):
    solver_list[i].q_learning(maze_list[i], episodes = 1500, learning_rate = 0.6, discount_factor = 0.6, exploration_rate = 0.95)
    manager.combine_images('temp', 'episode', 'maze{}_episode_solution.png'.format(i), 'right')
    solution_q_table.append(solver_list[i].q_table)
    maze_list[i].solution_path, maze_list[i].solution_cost, maze_list[i].solution_reward = solver_list[i].q_learning_path(maze_list[i], solution_q_table[i])

    debugViz.show_solution(maze_list[i], display_key = False, media_name="maze{}".format(i), learning_rate = 0.6, discount_factor = 0.6)
    solution_path_list.append(maze_list[i].solution_path)
    solution_cost_list.append(maze_list[i].solution_cost)

manager.combine_images('temp', 'solution','maze_q_learning_solution.png', 'down')

manager.combine_images('output', '_episode_','maze_output2.png', 'down')
manager.combine_images('output', '_output','maze_episode_table.png', 'right')


print("============================")
print("     Task 4 Complete")
print("============================")
# F. Use Visualization Func(at Codebase). Demonstartes the algorithm's performance from the 3 ramdonly gen. mazes
print("\nShow Solution Animation")
#solver_list[i].show_solution_animation(maze, media_name=f"Q-Learing_maze{i}")
for i in range(3):
    debugViz.show_solution_animation(maze_list[i])

#========+================================================================================================#
# Task 5 | Choose at least two params and change values of them to see the impact of the parameters.      #
#        |          e.g., a=(0.2, 0.4, 0.6, 0.8) and r=(0.2, 0.4, 0.6, 0.8)                               #
#========+================================================================================================#
shutil.rmtree('./temp')
solution2_path_list  = []
solution2_cost_list  = []
solution2_q_table    = []
solution2_reward     = []
solver_list         = []


a_list = [0.2, 0.4, 0.6, 0.8]
r_list = [0.2, 0.4, 0.6, 0.8]

manager_param = MazeManager()
manager_param.media_name="maze_for_sweep_show"
maze_param = manager_param.add_maze(maze_row, maze_col)
debugViz_param = DebugViz()
manager_param.show_maze(maze_param.id)

i = 0
j = 0
for a in a_list:
    solution2_path_list.append([])
    solution2_cost_list.append([])
    solution2_reward.append([])
    for r in r_list:
        #Make Solver Manager
        solver_param = QLearningManager(maze_param)
        solver_list.append(solver_param)

        #Learn Q Table
        solver_list[i].q_learning(maze_param, episodes = 1500, learning_rate = a, discount_factor = r, exploration_rate = 0.95)
        solution2_q_table.append(solver_list[i].q_table)

        # Solve Maze Using Learned Q_ TABLE
        temp_solution_path, temp_solution_cost, temp_solution_reward = solver_list[i].q_learning_path(maze_param, solution2_q_table[i])
        solution2_path_list[i].append(temp_solution_path)
        solution2_cost_list[i].append(temp_solution_cost)
        solution2_reward[i].append(temp_solution_reward)
        debugViz_param.show_solution(maze_param, display_key = False, media_name="maze_a_{}_r_{}_out".format(a, r),  learning_rate = a, discount_factor = r)
        j+=1

    manager_param.combine_images('temp', '_out', 'maze_a{}_solution.png'.format(a), 'right')
    i+=1

manager_param.combine_images('output', 'maze_a0.', 'maze_a_r_sweep_table.png', 'down')


# ================================= Plot ===============================
fig, axs = plt.subplots(2, 2, figsize=(10, 6), sharex=True)

markers = ['o', 's', '^', 'D']  # Define different markers for each 'a' value

for i, a in enumerate(a_list):
    reward_list = []
    for j, r in enumerate(r_list):
        reward_list.append(solution2_reward[i][j])
    row = i // 2  # Determine the row index of the subplot
    col = i % 2  # Determine the column index of the subplot
    axs[row, col].plot(r_list, reward_list, label=f'a={a}', marker=markers[i])  # Set marker based on 'a' value
    axs[row, col].set_ylabel('Reward')
    axs[row, col].set_title(f'a = {a}')

axs[-1, 0].set_xlabel('Discount Factor (r)')
axs[-1, 1].set_xlabel('Discount Factor (r)')

plt.tight_layout()

# Set the output directory
current_dir = os.getcwd()
output_dir = os.path.join(current_dir, 'output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the plot
file_path = os.path.join(output_dir, 'Reward_graph.png')
plt.savefig(file_path)
plt.show()

reward_table = np.zeros((len(a_list), len(r_list)))

for i, a in enumerate(a_list):
    for j, r in enumerate(r_list):
        reward_table[i, j] = solution2_reward[i][j]

norm = colors.Normalize(vmin=np.min(reward_table), vmax=np.max(reward_table))

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(reward_table, cmap='Blues', norm=norm)
ax.set_xticks(np.arange(len(r_list)))
ax.set_yticks(np.arange(len(a_list)))
ax.set_xticklabels(r_list)
ax.set_yticklabels(a_list)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

for i in range(len(a_list)):
    for j in range(len(r_list)):
        text = ax.text(j, i, f'{reward_table[i, j]:.1f}', ha="center", va="center", color="black")

cbar = ax.figure.colorbar(im, ax=ax)
ax.set_title("Reward Table")
ax.set_xlabel("Discount Factor (r)")
ax.set_ylabel("Learning Rate (a)")

output_dir = "./output"

file_path = os.path.join(output_dir, "Reward_Table.png")
plt.savefig(file_path)

plt.tight_layout()
plt.show()