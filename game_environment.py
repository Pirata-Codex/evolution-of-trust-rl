# game_environment.py

from collections import deque
from typing import Tuple 

class PrisonersDilemma:
    """
    Represents the Iterated Prisoner's Dilemma game environment.
    """
    COOPERATE = 0
    CHEAT = 1
    ACTIONS = [COOPERATE, CHEAT]
    ACTION_NAMES = {COOPERATE: "Cooperate", CHEAT: "Cheat"}

    # Standard payoff matrix for (player_1_action, player_2_action) -> (p1_reward, p2_reward)
    # T > R > P > S  (Temptation > Reward > Punishment > Sucker's Payoff)
    # 2R > T + S (ensures mutual cooperation is better than alternating)
    PAYOFFS = {
        (COOPERATE, COOPERATE): (3, 3),  # R: Reward for mutual cooperation
        (COOPERATE, CHEAT): (0, 5),      # S: Sucker's payoff, T: Temptation
        (CHEAT, COOPERATE): (5, 0),      # T: Temptation, S: Sucker's payoff
        (CHEAT, CHEAT): (1, 1)           # P: Punishment for mutual defection
    }

    def __init__(self, memory_length=1):
        """
        Initializes the game environment.
        :param memory_length: How many previous moves to consider for the state.
        """
        if memory_length < 0:
            raise ValueError("Memory length cannot be negative.")
        self.memory_length = memory_length

    def play_round(self, action_p1: int, action_p2: int) -> tuple[int, int]:
        """
        Plays a single round of the Prisoner's Dilemma.
        :param action_p1: Action of player 1 (COOPERATE or CHEAT).
        :param action_p2: Action of player 2 (COOPERATE or CHEAT).
        :return: A tuple of (reward_p1, reward_p2).
        """
        if action_p1 not in self.ACTIONS or action_p2 not in self.ACTIONS:
            raise ValueError("Invalid action. Use COOPERATE or CHEAT.")
        return self.PAYOFFS[(action_p1, action_p2)]

    def get_state(self, p1_history: deque, p2_history: deque) -> tuple:
        """
        Generates a state representation based on the last 'memory_length' moves.
        A state is a tuple: (p1_last_n_moves_tuple, p2_last_n_moves_tuple)
        Each inner tuple contains 0s for COOPERATE and 1s for CHEAT.
        If history is shorter than memory_length, pad with -1s (or a distinct "START" value).
        """
        p1_state_part = tuple(list(p1_history)[-self.memory_length:])
        p2_state_part = tuple(list(p2_history)[-self.memory_length:])

        # Pad with a neutral value if history is shorter than memory_length
        # This is important for the beginning of a match when not enough history exists
        if len(p1_state_part) < self.memory_length:
            p1_state_part = (-1,) * (self.memory_length - len(p1_state_part)) + p1_state_part
        if len(p2_state_part) < self.memory_length:
            p2_state_part = (-1,) * (self.memory_length - len(p2_state_part)) + p2_state_part

        return (p1_state_part, p2_state_part)

# Example Usage (for testing the environment)
if __name__ == "__main__":
    env = PrisonersDilemma(memory_length=2)
    p1_hist = deque()
    p2_hist = deque()

    print(f"Initial state (empty history): {env.get_state(p1_hist, p2_hist)}")

    r1, r2 = env.play_round(env.COOPERATE, env.COOPERATE)
    p1_hist.append(env.COOPERATE)
    p2_hist.append(env.COOPERATE)
    print(f"Round 1 (C, C): Rewards={r1},{r2}, State={env.get_state(p1_hist, p2_hist)}")

    r1, r2 = env.play_round(env.CHEAT, env.COOPERATE)
    p1_hist.append(env.CHEAT)
    p2_hist.append(env.COOPERATE)
    print(f"Round 2 (D, C): Rewards={r1},{r2}, State={env.get_state(p1_hist, p2_hist)}")

    r1, r2 = env.play_round(env.COOPERATE, env.CHEAT)
    p1_hist.append(env.COOPERATE)
    p2_hist.append(env.CHEAT)
    print(f"Round 3 (C, D): Rewards={r1},{r2}, State={env.get_state(p1_hist, p2_hist)}")

    # Test state with short history
    env_short_memory = PrisonersDilemma(memory_length=1)
    p1_hist_s = deque([env.COOPERATE])
    p2_hist_s = deque([env.CHEAT])
    print(f"State (memory=1, 1 move): {env_short_memory.get_state(p1_hist_s, p2_hist_s)}")

    p1_hist_s.append(env.COOPERATE) # Now 2 moves, but memory_length is 1
    p1_hist_s.popleft() # keep deque limited if needed
    print(f"State (memory=1, after popleft): {env_short_memory.get_state(p1_hist_s, p2_hist_s)}")