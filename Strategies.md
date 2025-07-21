The core of the Prisoner's Dilemma is choosing between **Cooperate (C)** and **Cheat (D)** (also known as Defect). Here's the standard payoff matrix your game uses, from the perspective of Player 1 (P1), when playing against Player 2 (P2):

| P1's Action | P2's Action | P1's Reward | P2's Reward | Outcome Name     |
| :---------- | :---------- | :---------- | :---------- | :--------------- |
| Cooperate   | Cooperate   | 3           | 3           | Mutual Cooperation (R) |
| Cooperate   | Cheat       | 0           | 5           | Sucker's Payoff (S) for P1, Temptation (T) for P2 |
| Cheat       | Cooperate   | 5           | 0           | Temptation (T) for P1, Sucker's Payoff (S) for P2 |
| Cheat       | Cheat       | 1           | 1           | Mutual Punishment (P) |

The general conditions are T > R > P > S (5 > 3 > 1 > 0) and 2R > T + S (6 > 5), which makes mutual cooperation stable and individually rational defection tempting.

Now, let's look at the strategies:

---

### **1. AlwaysCooperate (AllC)**

* **Logic:** This strategy always chooses to Cooperate, regardless of what the opponent has done in the past. It is unconditionally benevolent.
* **Behavior:**
    * **Against another AllC:** Both will always cooperate, resulting in (3, 3) for every round. This is the best mutual outcome.
    * **Against AlwaysCheat:** AllC will always cooperate, and AlwaysCheat will always cheat. AllC will get 0 points each round (the Sucker's Payoff), while AlwaysCheat gets 5 points each round (the Temptation payoff). AllC will be heavily exploited.
    * **Against TitForTat (TFT):** AllC and TFT will cooperate indefinitely after the first round, as TFT mimics AllC's cooperation. This leads to mutual cooperation.
* **Strengths:** Can achieve the highest possible joint score with other cooperative strategies.
* **Weaknesses:** Extremely vulnerable to exploitation by any cheating strategy.

---

### **2. AlwaysCheat (AllD)**

* **Logic:** This strategy always chooses to Cheat, regardless of what the opponent has done. It is unconditionally selfish.
* **Behavior:**
    * **Against AllC:** AllD will always cheat, getting 5 points each round, while AllC gets 0. AllD is a pure exploiter here.
    * **Against another AllD:** Both will always cheat, resulting in (1, 1) for every round. This is a poor outcome for both, but better than being the "sucker."
    * **Against TFT:** AllD will cheat on the first round. TFT will then mimic this and cheat on the second. Both will then continue to cheat indefinitely, leading to (1, 1) for all subsequent rounds.
* **Strengths:** Cannot be exploited by any strategy. Maximizes its score against unconditionally cooperative strategies.
* **Weaknesses:** Leads to poor outcomes when playing against other non-cooperative or retaliatory strategies. Never achieves mutual cooperation.

---

### **3. TitForTat (TFT)**

* **Logic:** This strategy is based on reciprocity. It starts by Cooperating. In subsequent rounds, it simply mirrors the opponent's previous move. If the opponent cooperated last, TFT cooperates. If the opponent cheated last, TFT cheats.
* **Behavior:**
    * **Against AllC:** TFT cooperates initially, AllC cooperates. TFT mimics, AllC cooperates. They fall into mutual cooperation (3, 3).
    * **Against AllD:** TFT cooperates initially, AllD cheats. TFT mimics AllD and cheats. AllD cheats, TFT mimics and cheats. They fall into mutual defection (1, 1) after the first round.
    * **Against another TFT:** Both cooperate indefinitely.
    * **Against Grudger:** Similar to AllC, they will cooperate indefinitely unless a communication error occurs.
* **Strengths:** Simple, clear, retaliatory, and forgiving. It punishes defection quickly but is quick to forgive upon repentance. This makes it very robust and often leads to cooperation.
* **Weaknesses:** Can get stuck in cycles of mutual defection if there's a single "miscommunication" (e.g., one agent's intended cooperation is registered as a defection due to noise).

---

### **4. Grudger (Grim Trigger)**

* **Logic:** This strategy starts by Cooperating. It continues to cooperate indefinitely *unless* the opponent ever defects. If the opponent defects even once, Grudger will defect (cheat) for all subsequent rounds, forever. It holds a permanent grudge.
* **Behavior:**
    * **Against AllC:** Cooperates indefinitely.
    * **Against AllD:** Grudger cooperates on round 1, AllD cheats. Grudger gets 0, AllD gets 5. From round 2 onwards, Grudger defects forever. Both will then likely get (1, 1) or (0,5) if AllD keeps defecting.
    * **Against TFT:** Cooperates indefinitely, as TFT won't defect against a cooperating Grudger.
* **Strengths:** Extremely effective at deterring defection. Any single defection by the opponent leads to a swift and permanent punishment, making defection undesirable.
* **Weaknesses:** Unforgiving. A single accidental defection (or "noise" in the environment) can lead to eternal mutual defection, even if the opponent is otherwise cooperative.

---

### **5. Pavlov (Win-Stay, Lose-Shift)**

* **Logic:** This strategy is based on "if it worked, keep doing it; if it didn't, change it."
    * If the previous round resulted in a "win" (both cooperated (R,R) or both cheated (P,P) - i.e., both got the same outcome, which is considered a stable outcome), Pavlov keeps its last action.
    * If the previous round resulted in a "loss" (one cooperated, one cheated (S,T or T,S) - i.e., an unbalanced outcome), Pavlov switches its last action.
* **Behavior:**
    * **Against AllC:** Cooperates indefinitely (C,C -> stay C).
    * **Against AllD:** Starts C, AllD D. (C,D) is a loss for Pavlov, so it shifts to D. (D,D) is a win for Pavlov, so it stays D. It stabilizes at mutual defection (1,1).
    * **Against another Pavlov:** Cooperates indefinitely.
    * **Unique aspect:** Pavlov can restore mutual cooperation even after a single isolated defection (noise). If (C,C) happens, then noise makes it (C,D). Pavlov shifts to D, opponent shifts to D (if also Pavlov). Now it's (D,D), which is a "win" for both, so they both stay D. Wait, actually, the classic Pavlov handles this slightly differently based on rewards, but the simple "Win-Stay, Lose-Shift" logic gets them to mutual defection (1,1) if one defects and the other cooperates.
* **Strengths:** Can correct from mutual defection back to mutual cooperation in some scenarios (e.g., if one player tries to exploit, but the other also defects). More resilient to certain types of errors than TFT.
* **Weaknesses:** Less intuitive for some. Can get stuck in cycles depending on specific opponent behavior.

---

### **6. RandomStrategy**

* **Logic:** Simply chooses Cooperate or Cheat with a 50% probability for each action, in every round. It has no memory and no strategy.
* **Behavior:** Highly unpredictable. Its average score against most strategies will be mediocre, as it neither consistently exploits nor consistently cooperates.
* **Strengths:** Cannot be predicted or exploited by opponents attempting to learn its pattern.
* **Weaknesses:** Rarely achieves high scores.

---

### **7. TitForTwoTats (TFTT)**

* **Logic:** A more forgiving variant of Tit-for-Tat. It starts by Cooperating. It will only defect if the opponent has defected in the **last two consecutive rounds**. If the opponent defects once, TFTT will still cooperate in the next round, giving them a chance to re-cooperate.
* **Behavior:**
    * **Against AllC:** Cooperates indefinitely.
    * **Against AllD:** TFTT gets exploited for two rounds (0,5), then starts defecting, stabilizing at (1,1).
    * **Against TFT:** Cooperates indefinitely.
    * **Benefit:** More robust to single "noisy" defections. If an opponent accidentally defects once, TFTT doesn't retaliate immediately, allowing cooperation to resume.
* **Strengths:** Forgiving, good for noisy environments.
* **Weaknesses:** More susceptible to exploitation by "opportunistic" strategies that might defect once knowing TFTT won't retaliate immediately.

---

### **8. TwoTitsForTat (TTFT)**

* **Logic:** A more punitive variant of Tit-for-Tat. It starts by Cooperating. If the opponent defects, TTFT will retaliate by defecting for **two consecutive rounds**, even if the opponent immediately re-cooperates.
* **Behavior:**
    * **Against AllC:** Cooperates indefinitely.
    * **Against AllD:** Starts C, AllD D. TTFT retaliates with D for two rounds. AllD keeps D. Stabilizes at (1,1).
    * **Against TFT:** After an initial defection from AllD, both TTFT and TFT will enter a cycle of mutual defection.
    * **Benefit:** Stronger deterrence. A single defection from an opponent results in a more significant punishment.
* **Strengths:** Punishes defection more harshly, potentially discouraging future defections more effectively.
* **Weaknesses:** Can escalate conflicts more easily and lead to longer periods of mutual defection, even from minor provocations or noise. Less forgiving.

---

### **9. GenerousTitForTat (GTFT)**

* **Logic:** Similar to Tit-for-Tat, but with an element of "generosity" or "forgiveness." If the opponent defects in the previous round, GTFT will still retaliate by defecting most of the time, but with a `forgiveness_prob` (e.g., 10%) chance, it will choose to Cooperate instead.
* **Behavior:**
    * **Against AllC:** Cooperates indefinitely.
    * **Against AllD:** Mostly cheats, but occasionally "forgives" and cooperates, getting exploited. Ends up with lower scores than pure TFT against AllD.
    * **Against another GTFT:** Tends to maintain cooperation. If a defection happens, there's a chance it will be quickly resolved due to forgiveness.
* **Strengths:** Can help re-establish cooperation after an error or a single opportunistic defection. More robust in noisy environments than pure TFT.
* **Weaknesses:** More exploitable than pure TFT because of its forgiveness.

---

### **10. AdaptiveTitForTat (ATFT)**

* **Logic:** This is a more dynamic strategy. It starts with a base (TFT-like) behavior. It then `update_strategy` method that modifies its internal "forgiveness" parameter based on the opponent's behavior.
    * If the opponent **cooperates**, the ATFT agent becomes slightly *more forgiving* (increases its probability of cooperating even after a defect).
    * If the opponent **defects**, the ATFT agent becomes slightly *less forgiving* (decreases its probability of cooperating after a defect).
* **Behavior:**
    * **Against consistently cooperative agents (AllC, TFT, Grudger):** ATFT will gradually become more forgiving, eventually acting like AllC.
    * **Against consistently cheating agents (AllD):** ATFT will quickly become less forgiving, acting more like AllD or a strict TFT.
    * **Against mixed or changing strategies:** It attempts to adapt its level of retaliation/forgiveness to the opponent's tendencies.
* **Strengths:** Attempts to optimize its behavior to the specific opponent it's facing, potentially leading to better long-term outcomes than a fixed strategy. It embodies a form of learning.
* **Weaknesses:** Its initial parameters (`initial_forgiveness`, `learning_rate`) can influence its adaptation speed and final strategy. It can be slow to adapt if learning rate is too low, or unstable if too high. It's also more complex than fixed strategies.

---

By running your tournament with all these strategies, you'll see how robust (or fragile) cooperation can be, and how different levels of forgiveness and retaliation play out in a repeated interaction scenario. You'll likely observe that a well-tuned Q-Learning agent can often learn behaviors similar to the more successful classic strategies like TFT or Pavlov, demonstrating the power of reinforcement learning to discover effective game-playing policies.
