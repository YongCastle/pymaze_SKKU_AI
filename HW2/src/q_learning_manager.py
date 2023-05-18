import csv
import logging
import os
import random
import sys
from matplotlib import animation, pyplot as plt

from src.debug_viz import DebugViz
from src.maze import Maze
from src.maze_viz import Visualizer



class QLearningManager(object):

    def __init__(self, maze, debug_mode = True):

        self.mazes = []
        self.maze = maze
        self.media_name = "NONE"
        self.name = ""
        self.q_table = {}                       
        self.rewards = {}                       #{Episode1 : [-1, -1, -1, -1, -1, 100], Episode2 : [-1, -1, -1, -1, -1, 100], ... }
        self.before_action = None

    def add_maze(self, maze):
        self.mazes.append(maze)

    #=====================================================================================
    def get_reward(self, maze, current_state, next_state):
        if next_state == maze.exit_coor:
            reward = 100
        elif maze.is_wall(next_state, current_state):
            reward = -1
        else:
            reward = -0.1
        return reward

    def log_iteration_info(self, episode, episodes, epi_cost, total_reward, max_iter):
        if max_iter != 0:
            if (episode + 1) % (episodes//3) == 0:
                print("")
                print("    Solution Cost: {0:3} steps".format(epi_cost))
                print("    Reward: {0:3.1f}".format(total_reward))
        else:
            if (episode + 1) % (episodes//3) == 0:
                print("")
                print("    Breaking out of loop. Maximum iterations reached.")



    #=====================================================================================

    def q_learning(self, maze, episodes, learning_rate, discount_factor, exploration_rate) :

        # A. Initialize the Q-Table with zeros and set values of parameters by yourself.
        self.q_table = self._initialize_q_table(maze)
        maze.solution_path = None
        maze.solution_cost = None
        self.solution_reward = None
        print("   Take some minute ... Pleas Wait ...")
        action_list = ["LEFT", "UP", "RIGHT", "DOWN"]

        for episode in range(episodes):
            temp_episode_path = list()
            steps = 0
            epi_cost = 1
            total_reward = 0
            self.before_action = None

            #Predefined Maximum number of iteration
            max_iter = 10000
            #print for debug
            if((episode+1) % (episodes//3) == 0):
                print("===========================================")
                print("Episode : {0:4}, max_iter: {1:5}, a: {2:2.1f} r: {3:2.1f}  e: {4:3.2f}  | Start ...".format(episode+1, max_iter, learning_rate, discount_factor, exploration_rate))
                
            # B. Set the Initial State (the starting position of the agent).
            current_state = maze.entry_coor

            # G. Repeat Steps c-f until the agent reaches the gaol or a predefined maximum number of iterations is reached.
            while (current_state != maze.exit_coor):
                if(max_iter == 0 and episode > 100):
                    print("Episode {} is Ended Becuase of Max_iteration set".format(episode))
                    print("==================================================")
                    break
                max_iter -= 1
                steps += 1
                temp_episode_path.append((current_state, False))

                # C. Choose an action based on the current state and the Q-Table, using the e-greedy staregy.
                action = self._choose_action(current_state, exploration_rate, self.q_table)   #Return ex) LEFT

                # D. Perform the action and observe the reward and the next state.
                next_state = self.do_action(maze, current_state, action)
                reward = self.get_reward(maze, current_state, next_state)

                action_idx = self.find_word_idx(action, action_list)

                # E. Update the Q-Table using the Q-Leaning update rule.
                # output 폴더 생성
                # if(episode % 10 ==0):
                #     debugViz=DebugViz()
                #     output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../', 'temp')
                #     if not os.path.exists(output_folder):
                #         os.makedirs(output_folder)
                        
                #     # 파일 생성 및 저장
                #     filename = os.path.join(output_folder, f"DEBUG_Q_Table_of_Episode{episode+1}.txt")
                #     debugViz.save_q_table(self.q_table, filename)
                #---------------------------------------------------------------\
                self.q_table[current_state][action_idx] += learning_rate * (reward + discount_factor * max(self.q_table[next_state]) - self.q_table[current_state][action_idx])
                total_reward += reward
                # #for Debug...
                # temp = DebugViz()  
                # output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../', 'output')
                # filename = os.path.join(output_folder, f"Q_Table_of_Episode_ing.txt")
                # temp.save_q_table(self.q_table, filename)
                # print("{0},{1}\n{2}".format(current_state,maze.grid[current_state[0]][current_state[1]].walls,self.q_table[current_state]))
                # print("이제 다음 행동 : "+action)
                # input("입력을 기다립니다: ")

                # F. Set the next state as the current state..
                current_state = next_state
                epi_cost += 1

            temp_episode_path.append((current_state, False))
            # Reduce the exploration rate over time.
            exploration_rate = exploration_rate * 0.999

            #-------------This is for Debugging--------------------------
            #print log
            self.log_iteration_info(episode, episodes, epi_cost, total_reward, max_iter)

            if (episode == 0 or (episode + 1) % (episodes//3) == 0):
                maze.solution_path = temp_episode_path

                debugViz = DebugViz()    
                debugViz.show_solution(maze, episodes = episode ,display_key = False, media_name=f"solve_maze_episode{episode+1}")
                
                # output 폴더 생성
                output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../', 'temp')
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                    
                # 파일 생성 및 저장
                filename = os.path.join(output_folder, f"Q_Table_of_Episode{episode+1}.txt")
                debugViz.save_q_table(self.q_table, filename)

        print("=====================================================")
            
        
    def q_learning_path(self, maze, learned_q_table):
        # Set the start and goal positions
        start_pos = maze.entry_coor
        goal_pos = maze.exit_coor

        # Set the initial position
        curr_pos = start_pos

        self.before_action = None
        solution_path = []
        solution_cost = 0
        solution_reward = 0
        action_list = ["LEFT", "UP", "RIGHT", "DOWN"] 

        max_cnt = 0
        print("================================================================")
        print("                       Solution PATH Q-TABLE                    ")
        print("+----------+------------+------------+------------+------------+")
        print("|   State  |    Left    |    UP      |  Right     |    Down    |")
        print("+----------+------------+------------+------------+------------+")

        #before_action = "nope"
        # Move until reaching the goal
        while curr_pos != goal_pos:
            if max_cnt > 1000:
                print("Path Fail")
                break
            max_cnt += 1

            # Get Valid Action List. Can't Go Through Walls
            # sorted_actions = np.argsort(-action_values) 
            # selected_action = sorted_actions[0]  

            # Move to the next position
            action = self._choose_action(curr_pos, 0, learned_q_table)


            # Format the Q-table values and highlight the selected action
            formatted_values = [
                f"\033[91m{value:^10.4f}\033[0m" if action_list[index] == action else f"{value:^10.4f}" for index, value in enumerate(learned_q_table[curr_pos])
            ]
            print("| ({0:^2}, {1:^2}) | {2} | {3} | {4} | {5} |".format(
                curr_pos[0], curr_pos[1], formatted_values[0], formatted_values[1], formatted_values[2], formatted_values[3]))
            
            solution_path.append(((curr_pos[0], curr_pos[1]), False))  # Append current cell to total search path

                
            next_pos = self.do_action(maze, curr_pos, action)
            
            solution_reward += self.get_reward(maze, curr_pos, next_pos)
            #before_action = action
            curr_pos = next_pos
            solution_cost += 1


        print("+---------+---------+---------+---------+---------+\n")
        solution_path.append(((curr_pos[0], curr_pos[1]), False))

        #-----------Save Soltion png----------------
        temp_episode_path = solution_path
        maze.solution_path = temp_episode_path
            
        return solution_path, solution_cost, solution_reward
    
    #=====================================================================================
 
    def _initialize_q_table(self, maze):
        q_table = {}
        for row in range(maze.num_rows):
            for col in range(maze.num_cols):
                state = (row, col)
                q_table[state] = [0, 0, 0, 0]  #Actions :[LEFT, RIGHT, UP, DOWN]
                    
        return q_table
    
    def _random_argmax_word(self, action_q_list):
        max_value = max(action_q_list)
        max_indices = [i for i, value in enumerate(action_q_list) if value == max_value]
        selected_index = random.choice(max_indices)
        
        action_list = ["LEFT", "UP", "RIGHT", "DOWN"]
        
        return action_list[selected_index]

    def _choose_action(self, current_coors, exploration_rate, q_table):
        """
        Actions :[LEFT, UP, RIGHT, DOWN]
        """
        # Using e-greedy staregy
        # Cant' go before State

        action_q_list = q_table[current_coors]
        action_list = ["LEFT","UP","RIGHT","DOWN"]
        if random.uniform(0, 1) < exploration_rate:
            random.shuffle(action_list)
            explor_act = action_list[0]
        else:
            explor_act = self._random_argmax_word(action_q_list)

        return explor_act #LEFT, UP, RIGHT, DOWN
    
    def do_action(self, maze, current_state, action):
        curr_k, curr_i = current_state
        
        if action == "LEFT":               
            next_k = curr_k
            next_i = curr_i - 1
        elif action == "UP":    
            next_k = curr_k + 1
            next_i = curr_i 
        elif action == "RIGHT":
            next_k = curr_k 
            next_i = curr_i + 1
        elif action == "DOWN":
            next_k = curr_k - 1
            next_i = curr_i
        else:
            raise ValueError("Invalid action value: {}".format(action))
        
        if(next_k < 0 or next_i < 0 or next_k >= maze.num_rows or next_i >= maze.num_cols):
            next_k = curr_k
            next_i = curr_i
            #print("Stupid Act : Can't go Outside Maze")
        
        next_state = (next_k, next_i)

        return next_state
   
    def find_argmax(self, lst):
        if not lst:
            print("No List ERROR at find_argmax")
            return None  # Handle empty list

        max_value = lst[0]
        max_index = 0

        for i, value in enumerate(lst):
            if value > max_value:
                max_value = value
                max_index = i

        return max_index


    def find_word_idx(self, word, list):
        
        for idx in range(len(list)):
            if(word == list[idx]):
                return idx
            
        print("Cant find Word IDX ERROR")
        return None
