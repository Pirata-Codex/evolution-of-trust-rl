# visualization.py

import matplotlib.pyplot as plt
import numpy as np

def plot_scores(results: dict, num_episodes: int, total_rounds: int, title: str = "Agent Scores Over Training"):
    """
    Plots the cumulative scores for each agent.
    :param results: A dictionary where keys are agent names and values are lists of cumulative scores.
    :param num_episodes: Total number of training episodes/matches.
    :param total_rounds: Number of rounds per match.
    :param title: Title of the plot.
    """
    plt.figure(figsize=(12, 7))
    for agent_name, scores_history in results.items():
        # Ensure scores_history is a list of episode-end cumulative scores
        plt.plot(range(1, num_episodes + 1), scores_history, label=agent_name)

    plt.title(title)
    plt.xlabel("Training Episode (Match Number)")
    plt.ylabel(f"Cumulative Score (over {total_rounds} rounds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_single_match_scores(agent1_name: str, agent2_name: str, scores1: list, scores2: list, total_rounds: int):
    """
    Plots the cumulative scores of two agents in a single match over rounds.
    :param agent1_name: Name of agent 1.
    :param agent2_name: Name of agent 2.
    :param scores1: List of cumulative scores for agent 1 per round.
    :param scores2: List of cumulative scores for agent 2 per round.
    :param total_rounds: Total rounds played in the match.
    """
    rounds = list(range(1, total_rounds + 1))
    plt.figure(figsize=(10, 6))
    plt.plot(rounds, np.cumsum(scores1), label=agent1_name)
    plt.plot(rounds, np.cumsum(scores2), label=agent2_name)

    plt.title(f"Cumulative Scores: {agent1_name} vs {agent2_name} (Single Match)")
    plt.xlabel("Round Number")
    plt.ylabel("Cumulative Score")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()