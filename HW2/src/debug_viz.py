


from src.maze_viz import Visualizer


class DebugViz(object):


    def save_q_table(self, q_table, filename):
        with open(filename, 'w') as f:
            f.write("================================================================\n")
            f.write("                             Q-Table                            \n")
            f.write("+----------+------------+------------+------------+------------+\n")
            f.write("|   State  |    Left    |    UP      |  Right     |    Down    |\n")
            f.write("+----------+------------+------------+------------+------------+\n")
            for state, action_values in q_table.items():
                f.write("| ({0:^2}, {1:^2}) | {2:^10.4f} | {3:^10.4f} | {4:^10.4f} | {5:^10.4f} |\n".format(
                    state[0], state[1], action_values[0], action_values[1], action_values[2], action_values[3]))
            f.write("+---------+----------+----------+----------+----------+\n")


    def print_q_table(self, q_table):
        print("================================================================")
        print("                            Q-Table                             ")
        print("+----------+------------+------------+------------+------------+")
        print("|   State  |    Left    |    UP      |  Right     |    Down    |")
        print("+----------+------------+------------+------------+------------+")
        for state, action_values in q_table.items():
            print("| ({0:^2}, {1:^2}) | {2:^10.4f} | {3:^10.4f} | {4:^10.4f} | {5:^10.4f} |".format(
                state[0], state[1], action_values[0], action_values[1], action_values[2], action_values[3]))
        print("+---------+----------+----------+----------+----------+\n")


    def show_maze(self, maze, display_mode = True, cell_size=1):
        """Just show the generation animation and maze"""
        vis = Visualizer(maze, cell_size, self.media_name)
        vis.show_maze(display_mode)

    def show_solution(self, maze, episodes = None, display_key = False, media_name=None,  learning_rate = None, discount_factor = None, cell_size=1):
        vis = Visualizer(maze, cell_size, media_name)
        vis.show_maze_solution(episodes, display_key, learning_rate, discount_factor)

    def show_solution_animation(self, maze,  media_name = None, cell_size=1):
        """
        Shows the animation of the path that the solver took.

        Args:
            id (int): The id of the maze whose solution will be shown
            cell_size (int):
        """
        vis = Visualizer(maze, cell_size, media_name)
        vis.animate_maze_solution()
        
    def set_filename(self, filename):
        """
        Sets the filename for saving animations and images
        Args:
            filename (string): The name of the file without an extension
        """

        self.media_name = filename
