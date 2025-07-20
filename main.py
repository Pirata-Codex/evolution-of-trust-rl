# main.py

import random
from collections import deque
import sys
import pandas as pd

from game_environment import PrisonersDilemma
from rl_agents import QLearningAgent
from classic_strategies import (
    AlwaysCooperate, AlwaysCheat, TitForTat, Grudger, Pavlov, RandomStrategy, ClassicStrategy,
    TitForTwoTats, TwoTitsForTat, GenerousTitForTat, AdaptiveTitForTat # NEW IMPORTS
)
from visualization import plot_scores, plot_single_match_scores


def run_match(agent1, agent2, num_rounds: int, env: PrisonersDilemma, is_training: bool = False, verbose: bool = False):
    """
    Runs a single match between two agents.
    ... (This function remains largely the same, but with the added AdaptiveTitForTat update) ...
    """
    agent1_history = deque(maxlen=env.memory_length)
    agent2_history = deque(maxlen=env.memory_length)
    agent1_total_score = 0
    agent2_total_score = 0
    agent1_round_scores = []
    agent2_round_scores = []

    # Reset agents for a new match
    agent1.reset()
    agent2.reset()

    if verbose:
        print(f"\n--- Match: {agent1.name} vs {agent2.name} (Rounds: {num_rounds}) ---")

    for round_num in range(num_rounds):
        state_for_agent1 = env.get_state(agent1_history, agent2_history)
        state_for_agent2 = env.get_state(agent2_history, agent1_history)

        if isinstance(agent1, QLearningAgent):
            action_a1 = agent1.choose_action(state_for_agent1)
        elif isinstance(agent1, ClassicStrategy):
            action_a1 = agent1.choose_action(agent2_history)
        else:
            raise TypeError(f"Unknown agent type for agent1: {type(agent1)}")

        if isinstance(agent2, QLearningAgent):
            action_a2 = agent2.choose_action(state_for_agent2)
        elif isinstance(agent2, ClassicStrategy):
            action_a2 = agent2.choose_action(agent1_history)
        else:
            raise TypeError(f"Unknown agent type for agent2: {type(agent2)}")

        # Special handling for Pavlov and AdaptiveTitForTat
        if isinstance(agent1, Pavlov):
            agent1.update_last_actions(action_a1, action_a2)
        if isinstance(agent2, Pavlov):
            agent2.update_last_actions(action_a2, action_a1)

        reward_a1, reward_a2 = env.play_round(action_a1, action_a2)

        agent1_total_score += reward_a1
        agent2_total_score += reward_a2
        agent1_round_scores.append(reward_a1)
        agent2_round_scores.append(reward_a2)

        agent1_history.append(action_a1)
        agent2_history.append(action_a2)

        # NEW: Update strategy for AdaptiveTitForTat if it's one of the agents
        if isinstance(agent1, AdaptiveTitForTat):
            agent1.update_strategy(action_a1, action_a2)
        if isinstance(agent2, AdaptiveTitForTat):
            agent2.update_strategy(action_a2, action_a1)

        if is_training:
            next_state_for_agent1 = env.get_state(agent1_history, agent2_history)
            next_state_for_agent2 = env.get_state(agent2_history, agent1_history)

            if isinstance(agent1, QLearningAgent):
                agent1.learn(state_for_agent1, action_a1, reward_a1, next_state_for_agent1)
            if isinstance(agent2, QLearningAgent):
                agent2.learn(state_for_agent2, action_a2, reward_a2, next_state_for_agent2)

        if verbose:
            print(f"  Rnd {round_num + 1}: {agent1.name} {env.ACTION_NAMES[action_a1]} ({reward_a1}) "
                  f"| {agent2.name} {env.ACTION_NAMES[action_a2]} ({reward_a2}) "
                  f"| Scores: {agent1.name}={agent1_total_score}, {agent2.name}={agent2_total_score}")

    if verbose:
        print(f"--- Match End --- Final Scores: {agent1.name}={agent1_total_score}, {agent2.name}={agent2_total_score}")

    return agent1_total_score, agent2_total_score, agent1_round_scores, agent2_round_scores


def main():
    # --- Configuration ---
    NUM_TRAINING_EPISODES = 2000 # How many matches the Q-Learner trains
    ROUNDS_PER_MATCH = 50       # Number of rounds in each match
    MEMORY_LENGTH = 1           # How many past moves the state considers (0 for no memory, 1 for last move)
    NUM_EVAL_MATCHES_PER_PAIR = 50 # How many times each pair plays in evaluation phase

    # --- Setup Environment ---
    env = PrisonersDilemma(memory_length=MEMORY_LENGTH)

    # --- Define Agents ---
    q_agent_train = QLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.2, name="QLearner (Training)")
    q_agent_eval = q_agent_train
    q_agent_eval.name = "QLearner (Eval)"
    q_agent_eval.epsilon = 0.05

    # UPDATED: Add new strategies here
    classic_agents = [
        AlwaysCooperate(),
        AlwaysCheat(),
        TitForTat(),
        Grudger(),
        Pavlov(),
        RandomStrategy(),
        TitForTwoTats(),         # NEW
        TwoTitsForTat(),         # NEW
        GenerousTitForTat(),     # NEW
        AdaptiveTitForTat()      # NEW
    ]

    print(f"--- Starting RL Training ({NUM_TRAINING_EPISODES} episodes, {ROUNDS_PER_MATCH} rounds/episode) ---")
    print(f"RL Agent: {q_agent_train.name} (alpha={q_agent_train.alpha}, gamma={q_agent_train.gamma}, epsilon={q_agent_train.epsilon})")
    print(f"Environment Memory Length: {MEMORY_LENGTH}\n")

    # UPDATED: Ensure training opponents include new strategies
    training_opponents = [
        TitForTat(), AlwaysCheat(), AlwaysCooperate(), RandomStrategy(), Grudger(), Pavlov(),
        TitForTwoTats(), TwoTitsForTat(), GenerousTitForTat(), AdaptiveTitForTat()
    ]

    q_learner_training_scores = []

    for episode in range(NUM_TRAINING_EPISODES):
        opponent_class = random.choice([type(a) for a in training_opponents])
        current_opponent = opponent_class()

        q_score, opponent_score, _, _ = run_match(q_agent_train, current_opponent, ROUNDS_PER_MATCH, env, is_training=True)
        q_learner_training_scores.append(q_score)

        if (episode + 1) % (NUM_TRAINING_EPISODES // 10) == 0 or episode == 0:
            print(f"Training Episode {episode + 1}/{NUM_TRAINING_EPISODES}. "
                  f"{q_agent_train.name} Score: {q_score} (vs {current_opponent.name}). "
                  f"Avg Q-Score so far: {sum(q_learner_training_scores)/(episode+1):.2f}")
            sys.stdout.flush()

    print("\n--- Training Complete ---")

    # --- Evaluation Phase ---
    print(f"\n--- Starting Evaluation ({NUM_EVAL_MATCHES_PER_PAIR} matches per pair) ---")
    print(f"QLearner Eval Epsilon: {q_agent_eval.epsilon}")

    all_agents_for_eval = [q_agent_eval] + classic_agents

    pairwise_scores = {agent.name: {opponent.name: 0.0 for opponent in all_agents_for_eval} for agent in all_agents_for_eval}

    for i, agent1_template in enumerate(all_agents_for_eval):
        for j, agent2_template in enumerate(all_agents_for_eval):
            if i == j:
                continue

            print(f"  Evaluating: {agent1_template.name} vs {agent2_template.name}...", end='')
            sys.stdout.flush()

            agent1 = agent1_template if isinstance(agent1_template, QLearningAgent) else type(agent1_template)()
            agent2 = agent2_template if isinstance(agent2_template, QLearningAgent) else type(agent2_template)()

            total_score_agent1_this_pairing = 0

            for _ in range(NUM_EVAL_MATCHES_PER_PAIR):
                s1, s2, _, _ = run_match(agent1, agent2, ROUNDS_PER_MATCH, env, is_training=False, verbose=False)
                total_score_agent1_this_pairing += s1

            avg_score_agent1_vs_agent2 = total_score_agent1_this_pairing / NUM_EVAL_MATCHES_PER_PAIR

            pairwise_scores[agent1_template.name][agent2_template.name] = avg_score_agent1_vs_agent2
            print(" Done.")
            sys.stdout.flush()

    print("\n--- Pairwise Average Scores (rows play against columns) ---")
    df_pairwise_scores = pd.DataFrame(pairwise_scores).transpose()
    for agent_name in df_pairwise_scores.index:
        df_pairwise_scores.loc[agent_name, agent_name] = float('nan')
    print(df_pairwise_scores.round(2))

    final_avg_scores = {}
    for agent_name, scores_dict in pairwise_scores.items():
        opponent_scores = [score for opponent, score in scores_dict.items() if opponent != agent_name]
        if opponent_scores:
            final_avg_scores[agent_name] = sum(opponent_scores) / len(opponent_scores)
        else:
            final_avg_scores[agent_name] = 0.0

    print("\n--- Overall Average Scores Per Strategy (Higher is Better) ---")
    sorted_scores = sorted(final_avg_scores.items(), key=lambda item: item[1], reverse=True)
    for name, score in sorted_scores:
        print(f"  {name}: {score:.2f}")

    # --- Visualization ---

    plot_scores({"QLearner (Training)": q_learner_training_scores},
                NUM_TRAINING_EPISODES, ROUNDS_PER_MATCH,
                "QLearner Cumulative Score During Training (vs. Random Opponents)")

    print("\n--- Showing an example match: QLearner (Eval) vs TitForTat (verbose) ---")
    q_agent_eval.epsilon = 0.0
    tft_agent_demo = TitForTat()

    q_scores, tft_scores, q_round_scores, tft_round_scores = run_match(q_agent_eval, tft_agent_demo, ROUNDS_PER_MATCH, env, is_training=False, verbose=True)
    plot_single_match_scores(q_agent_eval.name, tft_agent_demo.name, q_round_scores, tft_round_scores, ROUNDS_PER_MATCH)


if __name__ == "__main__":
    main()