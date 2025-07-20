# rl_agents.py

import random
from collections import defaultdict
from game_environment import PrisonersDilemma

class QLearningAgent:
    """
    A Reinforcement Learning agent that uses Q-Learning to learn a strategy.
    """
    def __init__(self,
                 alpha: float = 0.1,    # Learning rate
                 gamma: float = 0.9,    # Discount factor
                 epsilon: float = 0.1,  # Exploration rate (for epsilon-greedy policy)
                 name: str = "QLearner"):
        self.q_table = defaultdict(lambda: [0.0, 0.0])  # Q[state] = [Q(state, Cooperate), Q(state, Cheat)]
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.name = name
        self.last_action = None
        self.last_state = None

    def choose_action(self, state: tuple) -> int:
        """
        Chooses an action (Cooperate or Cheat) based on epsilon-greedy policy.
        :param state: The current state of the game (opponent's last move, etc.).
        :return: Action (0 for Cooperate, 1 for Cheat).
        """
        # Epsilon-greedy exploration
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(PrisonersDilemma.ACTIONS) # Explore
        else:
            # Exploit (choose action with highest Q-value)
            q_values = self.q_table[state]
            if q_values[PrisonersDilemma.COOPERATE] >= q_values[PrisonersDilemma.CHEAT]:
                action = PrisonersDilemma.COOPERATE
            else:
                action = PrisonersDilemma.CHEAT
        return action

    def learn(self, state: tuple, action: int, reward: int, next_state: tuple):
        """
        Updates the Q-table based on the observed reward and next state.
        :param state: The state before the action.
        :param action: The action taken.
        :param reward: The immediate reward received.
        :param next_state: The state after the action.
        """
        old_q_value = self.q_table[state][action]
        # Max Q-value for the next state
        next_max_q = max(self.q_table[next_state])

        # Q-learning update rule
        new_q_value = old_q_value + self.alpha * (reward + self.gamma * next_max_q - old_q_value)
        self.q_table[state][action] = new_q_value

    def reset(self):
        """
        Resets the agent's internal state (e.g., for a new match or training epoch).
        Note: The Q-table is NOT reset to allow for cumulative learning across matches.
        If you want to reset learning for each match, clear self.q_table here.
        """
        self.last_action = None
        self.last_state = None
        # self.q_table.clear() # Uncomment to reset Q-table for each new training run