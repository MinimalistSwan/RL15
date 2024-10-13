# Base imports
import numpy as np                  # Library for arrays, matrices, mathematical functions, etc.
import matplotlib.pyplot as plt     # Good for visualisations.
from MazeVisual import maze
from QLearningModel import QLearningAgent, actions

# Reward system -> Parameters can be adjusted here for experimentation.
end_reward = 100                    # Reward for reaching the end goal state.
sub_reward = 50                     # Reward for reaching the sub goal state.
wall_penalty = -10                  # Penalty for touching any wall in the maze.
step_penalty = -1                   # Penalty for taking any step in the maze.

# This function simulates the agent's movements in the maze for a single episode.
def finish_episode(agent, maze, current_episode, train=True):

    # The starting position of the agent and the environment is initialised. 
    current_state = maze.start_position 
    end_reached = False
    final_reward = 0                # Calulation the reward at the end of an episode.
    episode_step = 0                # Tracks how many steps the agent has taken since the start.
    path = [current_state]
    sub_goal_reached = False  

    while not end_reached:
        action = agent.get_action(current_state, current_episode)
        next_state = (current_state[0] + actions[action][0], current_state[1] + actions[action][1])

        if next_state[0] < 0 or next_state[0] >= maze.maze_height or next_state[1] < 0 or next_state[1] >= maze.maze_width or maze.maze[next_state[1]][next_state[0]] == 1:
            reward = wall_penalty
            next_state = current_state

        elif next_state == maze.sub_goal_position:
            path.append(current_state)
            reward = sub_reward
            sub_goal_reached = True
            print(f"Sub-goal reached at: {next_state}") 

        elif next_state == maze.goal_position:
            if sub_goal_reached: 
                path.append(current_state)
                reward = end_reward
                end_reached = True
            else:
                reward = wall_penalty  
                next_state = current_state
       
        else:
            path.append(current_state)
            reward = step_penalty

        final_reward += reward
        episode_step += 1

        if train:
            agent.update_q_table(current_state, action, next_state, reward)

        current_state = next_state

    return final_reward, episode_step, path


def test_agent(agent, maze, num_episodes=1):
  
    episode_reward, episode_step, path = finish_episode(agent, maze, num_episodes, train=False)

    print("Final Path:")
    for row, col in path:
        print(f"({row}, {col})-> ", end='')
    print("End Reached")

    print("Total steps:", episode_step)
    print("Total reward:", episode_reward)

    plt.figure(figsize=(5, 5))
    plt.imshow(maze.maze, cmap='Pastel1')

    plt.text(maze.start_position[0], maze.start_position[1], 'S', ha='center', va='center', color='green', fontsize=15)
    plt.text(maze.goal_position[0], maze.goal_position[1], 'E', ha='center', va='center', color='red', fontsize=15)
    plt.text(maze.sub_goal_position[0], maze.sub_goal_position[1], 'G', ha='center', va='center', color='blue', fontsize=15)

    for position in path:
        plt.text(position[0], position[1], "o", va='center', color='white', fontsize=10)

    plt.xticks([]), plt.yticks([])
    plt.grid(color='black', linewidth=2)

    plt.show(block=True) 

    return episode_step, episode_reward

agent = QLearningAgent(maze)
test_agent(agent, maze)
