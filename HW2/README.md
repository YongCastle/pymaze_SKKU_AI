# Maze Solver using Q-Learning

This code provides a maze-solving solution using the Q-learning algorithm. It can generate and solve 20x20 mazes using a reinforcement learning approach.

## Dependencies
- Python 3.8.5
- matplotlib == 3.5.3

## Setup and Installation
1. Clone the repository or download the code files.
2. Make sure you have Python 3.8.5 installed on your system.


## How to Run
1. Open a terminal or command prompt.
2. Navigate to the directory where the code files are located.
3. Run the following command to execute the maze-solving code:
   ```
   python example/solve_q_learning.py
   ```

During the execution of the code, temporary images and a text file containing Q_TABLE information will be generated in the temp folder. The visualization images for the results will be stored in the OUTPUT folder.

The code solves a 20x20 maze using Q-Learning and performs the following tasks:

### Task 1 & 2
- Function creation: `q_learning` and `q_learning_path`
- Prints completion message

### Task 3
- Trains 3 randomly generated 20x20 mazes with visualization
- Displays the mazes using DebugViz

### Task 4
- Implements the Q-Learning-based maze traversal algorithm for the randomly generated 20x20 mazes
- Combines images to visualize the solution paths and outputs

### Task 5
- Sweeps the learning rate (a) and discount factor (r) values to observe their impact
- Generates maze solutions and visualizes the reward trends
- Saves the reward graph and reward table

**Note:** Please ensure that the necessary folders (`temp` and `output`) are removed before running the code.

You can find the code implementation in the provided code snippet.

**Show Solution Animation:** Uncomment the relevant line to display the solution animation for each maze.

**Reward Graph:** The reward graph illustrates the impact of different discount factors (r) on the reward values for various learning rates (a).

**Reward Table:** The reward table shows the reward values for different combinations of learning rates (a) and discount factors (r).

Feel free to modify the code parameters and explore different maze-solving scenarios using Q-Learning.

