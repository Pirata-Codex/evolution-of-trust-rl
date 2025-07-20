# classic_strategies.py

import random
from collections import deque
from game_environment import PrisonersDilemma

class ClassicStrategy:
    """Base class for all classic strategies."""
    def __init__(self, name: str):
        self.name = name

    def choose_action(self, opponent_history: deque) -> int:
        """
        Chooses an action based on the opponent's history.
        To be implemented by subclasses.
        """
        raise NotImplementedError

    def reset(self):
        """Resets any internal state of the strategy (if any)."""
        pass # Most classic strategies are stateless or only need simple history

class AlwaysCooperate(ClassicStrategy):
    """Always cooperates, regardless of opponent's moves."""
    def __init__(self):
        super().__init__("AlwaysCooperate")

    def choose_action(self, opponent_history: deque) -> int:
        return PrisonersDilemma.COOPERATE

class AlwaysCheat(ClassicStrategy):
    """Always cheats, regardless of opponent's moves."""
    def __init__(self):
        super().__init__("AlwaysCheat")

    def choose_action(self, opponent_history: deque) -> int:
        return PrisonersDilemma.CHEAT

class TitForTat(ClassicStrategy):
    """
    Starts with cooperation, then mimics the opponent's last move.
    """
    def __init__(self):
        super().__init__("TitForTat")

    def choose_action(self, opponent_history: deque) -> int:
        if not opponent_history:
            return PrisonersDilemma.COOPERATE # Cooperate on first move
        return opponent_history[-1] # Mimic opponent's last move

class Grudger(ClassicStrategy):
    """
    Starts with cooperation, but defects forever if the opponent ever defects.
    """
    def __init__(self):
        super().__init__("Grudger")
        self.grudge = False

    def choose_action(self, opponent_history: deque) -> int:
        if self.grudge:
            return PrisonersDilemma.CHEAT

        if PrisonersDilemma.CHEAT in opponent_history:
            self.grudge = True
            return PrisonersDilemma.CHEAT
        return PrisonersDilemma.COOPERATE

    def reset(self):
        self.grudge = False

class Pavlov(ClassicStrategy):
    """
    Win-Stay, Lose-Shift strategy.
    Cooperate if both cooperated or both cheated in the last round (win).
    Cheat if one cooperated and the other cheated (lose).
    This agent needs its own last action as well as opponent's.
    """
    def __init__(self):
        super().__init__("Pavlov")
        self.last_own_action = None
        self.last_opponent_action = None

    def choose_action(self, opponent_history: deque) -> int:
        if self.last_own_action is None: # First move
            return PrisonersDilemma.COOPERATE

        if (self.last_own_action == PrisonersDilemma.COOPERATE and self.last_opponent_action == PrisonersDilemma.COOPERATE) or \
           (self.last_own_action == PrisonersDilemma.CHEAT and self.last_opponent_action == PrisonersDilemma.CHEAT):
            # Last round was a "win" (both cooperated or both cheated) -> Stay with current action (which was last_own_action)
            return self.last_own_action
        else:
            # Last round was a "loss" (one cooperated, one cheated) -> Shift action
            return PrisonersDilemma.COOPERATE if self.last_own_action == PrisonersDilemma.CHEAT else PrisonersDilemma.CHEAT

    def update_last_actions(self, own_action: int, opponent_action: int):
        self.last_own_action = own_action
        self.last_opponent_action = opponent_action

    def reset(self):
        self.last_own_action = None
        self.last_opponent_action = None

class RandomStrategy(ClassicStrategy):
    """Chooses actions randomly."""
    def __init__(self):
        super().__init__("Random")

    def choose_action(self, opponent_history: deque) -> int:
        return random.choice(PrisonersDilemma.ACTIONS)

# --- NEW STRATEGIES ADDED BELOW ---

class TitForTwoTats(ClassicStrategy):
    """
    Starts with cooperation, defects only if the opponent defects two times in a row.
    More forgiving than TitForTat.
    """
    def __init__(self):
        super().__init__("TitForTwoTats")

    def choose_action(self, opponent_history: deque) -> int:
        if len(opponent_history) < 2:
            return PrisonersDilemma.COOPERATE # Cooperate on first two moves
        # If opponent defected in the last two moves, defect. Otherwise, cooperate.
        if opponent_history[-1] == PrisonersDilemma.CHEAT and opponent_history[-2] == PrisonersDilemma.CHEAT:
            return PrisonersDilemma.CHEAT
        return PrisonersDilemma.COOPERATE

class TwoTitsForTat(ClassicStrategy):
    """
    Starts with cooperation. If the opponent defects, it defects twice in a row.
    More punitive than TitForTat.
    """
    def __init__(self):
        super().__init__("TwoTitsForTat")
        self.punish_count = 0 # How many more defects to dole out

    def choose_action(self, opponent_history: deque) -> int:
        if self.punish_count > 0:
            self.punish_count -= 1
            return PrisonersDilemma.CHEAT
        
        if not opponent_history:
            return PrisonersDilemma.COOPERATE # Cooperate on first move
        
        if opponent_history[-1] == PrisonersDilemma.CHEAT:
            self.punish_count = 1 # We've already decided to defect this round, so 1 more defect after this.
            return PrisonersDilemma.CHEAT
        
        return PrisonersDilemma.COOPERATE

    def reset(self):
        self.punish_count = 0

class GenerousTitForTat(ClassicStrategy):
    """
    Similar to TitForTat, but with a small probability of cooperating
    even if the opponent defected in the previous round.
    """
    def __init__(self, forgiveness_prob: float = 0.1):
        super().__init__("GenerousTitForTat")
        self.forgiveness_prob = forgiveness_prob # Probability of cooperating after opponent defects

    def choose_action(self, opponent_history: deque) -> int:
        if not opponent_history:
            return PrisonersDilemma.COOPERATE # Cooperate on first move
        
        if opponent_history[-1] == PrisonersDilemma.CHEAT:
            # Opponent defected, but we might forgive
            if random.random() < self.forgiveness_prob:
                return PrisonersDilemma.COOPERATE
            else:
                return PrisonersDilemma.CHEAT # Standard TFT response
        
        return PrisonersDilemma.COOPERATE # Opponent cooperated, we cooperate

class AdaptiveTitForTat(ClassicStrategy):
    """
    A more advanced TFT variant that adapts its 'forgiveness' or 'punishment'
    based on the opponent's perceived cooperativeness.
    Starts as TFT, but might become more forgiving or more punishing.
    This one is illustrative and a simple adaptation.
    """
    def __init__(self, initial_forgiveness=0.0, learning_rate=0.05):
        super().__init__("AdaptiveTitForTat")
        self.forgiveness = initial_forgiveness # Probability of cooperating when opponent defects
        self.learning_rate = learning_rate
        self.last_opponent_action = None # To track opponent's last move

    def choose_action(self, opponent_history: deque) -> int:
        if not opponent_history:
            self.last_opponent_action = None # Reset for first move
            return PrisonersDilemma.COOPERATE

        self.last_opponent_action = opponent_history[-1] # Update for learning in next step

        if self.last_opponent_action == PrisonersDilemma.CHEAT:
            # Opponent defected, decide based on current forgiveness
            if random.random() < self.forgiveness:
                return PrisonersDilemma.COOPERATE # Forgive
            else:
                return PrisonersDilemma.CHEAT # Punish
        else: # Opponent cooperated
            return PrisonersDilemma.COOPERATE

    # This agent needs its own way to "learn" from results, so it's a bit hybrid.
    # We'll need to call update_strategy from main.py after each round.
    def update_strategy(self, own_action: int, opponent_action: int):
        # If opponent cooperated, become slightly more forgiving (or maintain if already forgiving)
        if opponent_action == PrisonersDilemma.COOPERATE:
            self.forgiveness = min(1.0, self.forgiveness + self.learning_rate)
        # If opponent cheated, become slightly less forgiving (more punitive)
        elif opponent_action == PrisonersDilemma.CHEAT:
            self.forgiveness = max(0.0, self.forgiveness - self.learning_rate)

    def reset(self):
        self.forgiveness = 0.0 # Reset to initial state
        self.last_opponent_action = None

# For AdaptiveTitForTat, we need to adapt the run_match function in main.py
# similarly to how Pavlov is handled, to call `update_strategy` after each round.