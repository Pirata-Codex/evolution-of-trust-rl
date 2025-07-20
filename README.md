# The Evolution of Trust: An Iterated Prisoner's Dilemma Simulator

This project delves into the fascinating world of the Iterated Prisoner's Dilemma (IPD), a foundational concept in game theory, to observe the emergence of cooperation and competition. It provides a robust simulation environment where various classic strategies compete against each other and a Reinforcement Learning (RL) agent.

The core aim is to understand which strategies prove most effective in repeated interactions and how an RL agent, through trial and error, learns to navigate these complex social dilemmas.

## Table of Contents

  -  [Features](#features)
  -  [Getting Started](#getting-started)
      -  [Prerequisites](#prerequisites)
      -  [Installation](#installation)
      -  [Running the Simulation](#running-the-simulation)
  -  [Project Structure](#project-structure)
  -  [Strategies Implemented](#strategies-implemented)
  -  [Results & Analysis](#results--analysis)
  -  [Future Enhancements](#future-enhancements)
  -  [Contributing](#contributing)
  -  [License](#license)

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

  * Python 3.9+ (or use `typing.Tuple` for older versions if needed, as per earlier discussion)
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
```

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
└── requirements.txt        # Lists all Python dependencies.
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

After training the Q-Learner for `NUM_TRAINING_EPISODES` and evaluating all agents across `NUM_EVAL_MATCHES_PER_PAIR` (each consisting of `ROUNDS_PER_MATCH`), here's a snapshot of the performance:

-----

### Overall Average Scores Per Strategy (Higher is Better)

This ranking indicates how well each strategy performed on average across all opponents it faced in the evaluation tournament.

```
  Grudger: 139.65
  TwoTitsForTat: 137.01
  Pavlov: 133.38
  TitForTat: 133.37
  AdaptiveTitForTat: 132.87
  GenerousTitForTat: 132.00
  AlwaysCooperate: 119.85
  TitForTwoTats: 119.85
  AlwaysCheat: 114.57
  Random: 112.94
  QLearner (Eval): 111.51
```

**Interpretation:**

  * Strategies that combine initial cooperation with swift, firm (but sometimes forgiving) retaliation (e.g., Grudger, TwoTitsForTat, Pavlov, TitForTat) tend to perform best overall. They foster mutual cooperation when possible but protect themselves from exploitation.
  * The `QLearner (Eval)` is currently positioned lower. This could indicate it needs more training episodes, different hyperparameters (learning rate, discount factor, epsilon decay), or a more complex state representation (longer `MEMORY_LENGTH`) to discover more optimal strategies.

### Pairwise Average Scores (Rows play against Columns)

This matrix shows the average score obtained by the "row" strategy when playing against the "column" strategy. `NaN` indicates self-play (not evaluated).

```
                    QLearner (Eval)  ...  AdaptiveTitForTat
QLearner (Eval)               NaN  ...             126.80
AlwaysCooperate             74.34  ...             150.00
AlwaysCheat                149.52  ...              54.00
TitForTat                  123.20  ...             150.00
Grudger                    147.76  ...             150.00
Pavlov                     122.90  ...             150.00
Random                     111.10  ...             119.56
TitForTwoTats               74.34  ...             150.00
TwoTitsForTat              146.68  ...             150.00
GenerousTitForTat          118.52  ...             150.00
AdaptiveTitForTat          122.96  ...                NaN

[11 rows x 11 columns]
```

**Observations from the Matrix:**

  * Strategies like `AlwaysCooperate`, `TitForTwoTats`, `GenerousTitForTat` receive high scores (often 150.00) when playing against `AdaptiveTitForTat`, indicating `AdaptiveTitForTat` learned to be very cooperative with them.
  * `AlwaysCheat` consistently scores high (e.g., \~149.52 against `QLearner (Eval)`) while receiving low scores, demonstrating its exploitative nature.
  * The `QLearner (Eval)`'s scores against other agents vary, suggesting it adapts, but perhaps not yet optimally against all types of opponents. Its score of 74.34 against `AlwaysCooperate` and `TitForTwoTats` hints at it possibly exploiting these more naive/forgiving strategies, but its `111.51` overall average indicates it's struggling against the stronger retaliatory strategies.

*(For a full, un-truncated view of the pairwise matrix, run the `main.py` script locally.)*

## Future Enhancements

  * **Hyperparameter Optimization:** Implement a grid search or Bayesian optimization for the Q-Learning agent's `alpha`, `gamma`, and `epsilon` (and its decay schedule).
  * **Deeper States:** Increase `MEMORY_LENGTH` and potentially switch to Deep Q-Networks (DQN) for more complex state representations.
  * **Genetic Algorithms:** Introduce a genetic algorithm to evolve strategies, offering an alternative learning paradigm.
  * **Noisy Environment:** Add a probability of miscommunication (e.g., an intended cooperate becomes a cheat) to test strategy robustness in realistic scenarios.
  * **New Strategies:** Implement more advanced or less common game theory strategies.
  * **Visualizations:** Create more interactive and informative plots, possibly showing strategy dynamics over time.

## Contributing

Contributions are welcome\! If you have suggestions for new strategies, improvements to existing code, or ideas for further analysis, please feel free to fork the repo!

## License

This project is licensed under the MIT License - see the `LICENSE` file for details. *(Note: You should add an actual `LICENSE` file to your repository if you haven't already.)*

-----
