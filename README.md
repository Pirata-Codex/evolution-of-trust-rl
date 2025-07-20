# The Evolution of Trust: An Iterated Prisoner's Dilemma Simulator

This project delves into the fascinating world of the Iterated Prisoner's Dilemma (IPD), a foundational concept in game theory, to observe the emergence of cooperation and competition. It provides a robust simulation environment where various classic strategies compete against each other and a Reinforcement Learning (RL) agent.

The core aim is to understand which strategies prove most effective in repeated interactions and how an RL agent, through trial and error, learns to navigate these complex social dilemmas.

## Table of Contents

* [Features](#features)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
    * [Running the Simulation](#running-the-simulation)
* [Project Structure](#project-structure)
* [Strategies Implemented](#strategies-implemented)
* [Results & Analysis](#results--analysis)
* [Future Enhancements](#future-enhancements)
* [Contributing](#contributing)

  
## Features

* **Iterated Prisoner's Dilemma Environment:** A flexible simulation environment for multi-round games.
* **Q-Learning Agent:** A Reinforcement Learning agent capable of learning optimal strategies through interaction.
* **Comprehensive Classic Strategies:** Implementation of well-known game theory strategies for benchmarking.
* **Tournament Simulation:** A round-robin tournament framework to evaluate agent performance across various pairings.
* **Dynamic Adaptation:** Strategies like Pavlov and AdaptiveTitForTat demonstrate dynamic behavior.
* **Detailed Output:** Console logging for training progress and final evaluation metrics.
* **Data Visualization:** Plots to illustrate the Q-Learner's training progress and detailed match outcomes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.9+ (or use `typing.Tuple` for older versions if needed)
* `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/rl-ipd-project.git
    cd rl-ipd-project
    ```
    *(Replace `your-username/rl-ipd-project.git` with your actual repository URL)*

2.  **Install dependencies:**
    The project uses `numpy`, `matplotlib`, and `pandas`. These can be installed using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

### Running the Simulation

Execute the main script from the project's root directory:

```bash
python main.py
````

The simulation will:

1.  Train the Q-Learning agent against a diverse set of classic strategies.
2.  Run a comprehensive evaluation phase where all agents play against each other.
3.  Print detailed average scores and a pairwise performance matrix to the console.
4.  Display plots for Q-Learner training progress and a detailed example match.

## Project Structure

```
rl_ipd_project/
├── main.py                 # Orchestrates the simulation, training, and evaluation.
├── game_environment.py     # Defines the Iterated Prisoner's Dilemma game logic.
├── rl_agents.py            # Implements the Q-Learning agent.
├── classic_strategies.py   # Contains various hand-coded game theory strategies.
├── visualization.py        # Handles plotting of results using Matplotlib.
├── requirements.txt        # Lists all Python dependencies.
└── images/                 # Directory for storing generated plots.
    ├── Figure_1.png
    └── Figure_2.png
```

## Strategies Implemented

This simulation includes a rich set of strategies, each with a unique approach to cooperation and defection:

  * **AlwaysCooperate:** Unconditionally cooperates.
  * **AlwaysCheat:** Unconditionally defects.
  * **TitForTat:** Cooperates initially, then mirrors opponent's last move.
  * **Grudger:** Cooperates until the first defection, then defects forever.
  * **Pavlov:** (Win-Stay, Lose-Shift) Repeats action if successful, switches if not.
  * **RandomStrategy:** Randomly chooses to cooperate or defect.
  * **TitForTwoTats:** More forgiving; defects only after two consecutive opponent defections.
  * **TwoTitsForTat:** More punitive; defects twice after a single opponent defection.
  * **GenerousTitForTat:** TitForTat with a small probability of forgiving a defection.
  * **AdaptiveTitForTat:** Dynamically adjusts its forgiveness based on opponent behavior.
  * **QLearner (Eval/Training):** The Reinforcement Learning agent, which learns its strategy through repeated interaction.

## Results & Analysis

After training the Q-Learner for `NUM_TRAINING_EPISODES` (e.g., 2000) and evaluating all agents across `NUM_EVAL_MATCHES_PER_PAIR` (e.g., 50) matches, each consisting of `ROUNDS_PER_MATCH` (e.g., 50) rounds, here's a snapshot of the performance and the generated plots.

-----

### Q-Learner Training Progress

This plot shows the cumulative score of the Q-Learner during its training episodes, playing against randomly selected classic opponents.

**Analysis of Training Progress:**
The cumulative score of the Q-Learner fluctuates significantly throughout the 2000 training episodes. This high variability is typical when an RL agent is exploring and learning against a diverse set of opponents, some cooperative and some exploitative. The absence of a consistent upward trend to a stable high score suggests that while the Q-Learner is learning, its hyperparameters (learning rate, discount factor, epsilon decay) or the complexity of its state representation might need further fine-tuning to achieve more consistent optimal behavior against a varied opponent pool.

-----

### Single Match Example: QLearner vs TitForTat

This plot illustrates the cumulative scores of the trained Q-Learner and the TitForTat strategy over a single 50-round match.

**Analysis of Single Match:**
In this specific match against TitForTat, both the Q-Learner and TitForTat show a near-perfect linear increase in their cumulative scores, and their lines are almost identical. This is a strong indicator of **mutual cooperation** throughout the match. This outcome is highly desirable in the Iterated Prisoner's Dilemma, demonstrating that the Q-Learner successfully learned to reciprocate cooperation when paired with a forgiving yet firm strategy like TitForTat.

-----

### Overall Average Scores Per Strategy (Higher is Better)

This ranking indicates how well each strategy performed on average across all opponents it faced in the evaluation tournament.

```
  Grudger: 153.52
  TwoTitsForTat: 152.32
  TitForTat: 145.96
  AdaptiveTitForTat: 145.34
  GenerousTitForTat: 145.04
  Pavlov: 145.03
  AlwaysCooperate: 137.13
  TitForTwoTats: 127.19
  AlwaysCheat: 125.20
  Random: 121.95
  QLearner (Eval): 121.90
```

**Interpretation:**

  * Strategies that combine initial cooperation with swift, firm (but sometimes forgiving) retaliation (e.g., `Grudger`, `TwoTitsForTat`, `TitForTat`, `Pavlov`) tend to perform best overall. They foster mutual cooperation when possible but protect themselves from exploitation.
  * The `QLearner (Eval)` is positioned in the lower middle of the pack. Its score of `121.90` places it above `AlwaysCheat` and `Random`, indicating it has learned to avoid complete exploitation and achieve some cooperation. However, it still lags behind the top-performing classic strategies, suggesting room for improvement in its learning parameters or architecture.

### Pairwise Average Scores (Rows play against Columns)

This matrix shows the average score obtained by the "row" strategy when playing against the "column" strategy over all evaluation matches for that pairing.

| | QLearner (Eval) | AlwaysCooperate | AlwaysCheat | TitForTat | Grudger | Pavlov | Random | TitForTwoTats | TwoTitsForTat | GenerousTitForTat | AdaptiveTitForTat |
|:------------------|:---------------:|:---------------:|:-----------:|:---------:|:-------:|:--------:|:-------:|:---------------:|:---------------:|:------------------:|:------------------:|
| **QLearner (Eval)** | NaN | 152.36 | 1.3 | 148.66 | 92.6 | 148.96 | 77.0 | 152.24 | 145.28 | 149.3 | 151.44 |
| **AlwaysCooperate** | 146.4 | NaN | 0.0 | 150.0 | 150.0 | 150.0 | 74.88 | 150.0 | 150.0 | 150.0 | 150.0 |
| **AlwaysCheat** | 244.0 | 250.0 | NaN | 54.0 | 54.0 | 54.0 | 152.64 | 250.0 | 54.0 | 75.36 | 54.0 |
| **TitForTat** | 148.94 | 150.0 | 49.0 | NaN | 150.0 | 150.0 | 111.66 | 150.0 | 150.0 | 150.0 | 150.0 |
| **Grudger** | 189.92 | 150.0 | 49.0 | 150.0 | NaN | 150.0 | 146.24 | 150.0 | 150.0 | 150.0 | 150.0 |
| **Pavlov** | 148.32 | 150.0 | 49.0 | 150.0 | 150.0 | NaN | 112.98 | 150.0 | 150.0 | 150.0 | 150.0 |
| **Random** | 196.32 | 200.08 | 25.28 | 115.34 | 32.28 | 114.12 | NaN | 201.24 | 87.04 | 123.22 | 124.6 |
| **TitForTwoTats** | 146.58 | 150.0 | 0.0 | 150.0 | 150.0 | 150.0 | 75.3 | NaN | 150.0 | 150.0 | 150.0 |
| **TwoTitsForTat** | 150.88 | 150.0 | 49.0 | 150.0 | 150.0 | 150.0 | 123.32 | 150.0 | NaN | 150.0 | 150.0 |
| **GenerousTitForTat** | 148.72 | 150.0 | 43.84 | 150.0 | 150.0 | 150.0 | 107.86 | 150.0 | 150.0 | NaN | 150.0 |
| **AdaptiveTitForTat** | 146.92 | 150.0 | 49.0 | 150.0 | 150.0 | 150.0 | 107.46 | 150.0 | 150.0 | 150.0 | NaN |

**Observations from the Matrix:**

  * **QLearner (Eval) Performance:** The Q-Learner scores very high (around 145-152) against most cooperative and forgiving strategies like `AlwaysCooperate`, `TitForTat`, `Pavlov`, `GenerousTitForTat`, and `AdaptiveTitForTat`. This indicates it has learned to establish and maintain cooperation. However, it scores very low (`1.3`) when playing *against* `AlwaysCheat`, meaning `AlwaysCheat` heavily exploits it. Conversely, the Q-Learner scores high (`244.0`) *when playing against* `AlwaysCheat`, showing it successfully exploits the exploiter\! This suggests a somewhat "Tit-for-Tat"-like learning: if it sees cooperation, it cooperates; if it sees cheating, it might also cheat.
  * **Exploitation:** `AlwaysCheat` consistently achieves the highest scores (244.0-250.0) when playing against strategies that are easy to exploit (like `QLearner (Eval)`, `AlwaysCooperate`, `TitForTwoTats`, `Random`). This reaffirms its purely self-interested, opportunistic nature.
  * **Mutual Cooperation:** Many pairings among the cooperative and retaliatory strategies (e.g., `TitForTat` vs. `Grudger`, `Pavlov` vs. `TitForTat`) show scores around `150.0` for both sides, indicating sustained mutual cooperation.
  * **Random's Impact:** `Random` strategy creates mixed results for opponents, as its unpredictable nature can lead to lower scores for both sides in a match.
  * **Grudger and TwoTitsForTat:** These highly punitive strategies perform very well overall because they effectively deter defection, often leading to mutual cooperation or stable mutual defection (which is still better than being exploited).

-----

## Future Enhancements

  * **Hyperparameter Optimization:** Implement a grid search or Bayesian optimization for the Q-Learning agent's `alpha`, `gamma`, and `epsilon` (and its decay schedule).
  * **Deeper States:** Increase `MEMORY_LENGTH` and potentially switch to Deep Q-Networks (DQN) for more complex state representations.
  * **Genetic Algorithms:** Introduce a genetic algorithm to evolve strategies, offering an alternative learning paradigm.
  * **Noisy Environment:** Add a probability of miscommunication (e.g., an intended cooperate becomes a cheat) to test strategy robustness in realistic scenarios.
  * **New Strategies:** Implement more advanced or less common game theory strategies.
  * **Visualizations:** Create more interactive and informative plots, possibly showing strategy dynamics over time.

## Contributing

Contributions are welcome\! If you have suggestions for new strategies, improvements to existing code, or ideas for further analysis, please feel free to fork the repo!
