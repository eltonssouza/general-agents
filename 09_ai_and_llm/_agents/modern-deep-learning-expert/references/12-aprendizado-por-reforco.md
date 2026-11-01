# 12 — Reinforcement learning (RL) and RLHF

Source: UDL ch.19 (PDF p.387-414). Body and notes read through p.412; p.413-414 (end of the notes and problems) NOT read. NNDL only mentions RL in passing (Atari with convolutional networks, NNDL p.295-296 `[DATED 2015]`). The book warns that this is a "superficial" treatment (UDL p.29, p.412).

## 1. Formulation
- `[from source]` RL = sequential decision-making: agent, environment, actions, rewards; challenges: sparse reward, temporal credit assignment, stochastic environment, exploration × exploitation (UDL p.387; also p.25-26).
- `[from source]` Markov process (`Pr(s_{t+1}|s_t)`), Markov reward process (return **`G_t = Σ_{k≥0} γ^k r_{t+k+1}`**, γ ∈ (0,1], eq. 19.1), MDP (actions) and POMDP (observations) (UDL p.388-391). Policy `π[a|s]` stochastic or deterministic, stationary or not (UDL p.391).
- `[from source]` State value `v[s|π] = E[G_t|s,π]` and action value `q[s,a|π]` (eq. 19.2-19.3); optimal policy and values `v*`, `q*` (eq. 19.4-19.6, UDL p.392-393); **Bellman equations** `v[s] = Σ_a π[a|s] q[s,a]` and `q[s,a] = r[s,a] + γ Σ_{s'} Pr(s'|s,a) v[s']` and their combinations (eq. 19.7-19.10, UDL p.393-395). For MDPs there is always a deterministic, stationary optimal policy; for POMDPs there is not (UDL p.393).
- `[checked in dl_calc.py returns]`: rewards [0,0,1] with γ=0.9 give G = 0.81 (direct application of eq. 19.1; the book does not give this number).

## 2. Tabular RL (UDL p.395-399)
Model-based (dynamic programming, when the transitions are known) vs model-free (estimate values or policy). Dynamic programming: policy evaluation `v[s] ← Σ_a π[a|s](r + γ Σ Pr v[s'])` (eq. 19.11; bootstrapping) and greedy improvement (eq. 19.12), in policy iteration or value iteration (UDL p.396-397). Monte Carlo: averages of returns, exploring starts, ε-greedy, on-policy × off-policy (UDL p.397-398). TD: **SARSA** `q ← q + α[r + γ q[s',a'] − q]` (eq. 19.14, on-policy) and **Q-learning** `q ← q + α[r + γ max_a q[s',a] − q]` (eq. 19.15, off-policy); they converge if all pairs are visited infinitely often (UDL p.398). Fig. 19.12: example with γ=0.9, α=0.1 and next maximum 0.43 updating to 1.12 (UDL p.399; the previous value of q is not in the text).

## 3. Q-learning with networks (UDL p.399-402)
`[from source]` Fitted Q-learning: loss `(r + γ max_a q[s_{t+1},a,φ] − q[s_t,a_t,φ])²` (eq. 19.16-19.17); no convergence guarantee. **DQN** (Atari, 49 games): 220×160 images → 84×84 grayscale, 4 frames per state, 3 convolutional layers + FC with one output per action (fig. 19.14: 8×8 stride 4, 4×4 stride 2); rewards clipped to ±1, *experience replay* and frozen target parameters `φ⁻` (eq. 19.18); performance comparable to a professional tester, but ~38 days of experience per game; fails on Montezuma's Revenge (UDL p.400-401). Double Q-learning/double DQN for the overestimation bias of the max (eq. 19.19-19.21, UDL p.401-402). Notes: dueling, noisy DQN, distributional DQN, Rainbow, "deadly triad" (bootstrapping + off-policy + function approximation) (UDL p.410-411).

## 4. Policy gradient (UDL p.402-407)
- Reasons for a stochastic policy: exploration, a loss that is smooth in the parameters, and POMDPs (UDL p.402).
- `Pr(τ|θ) = Pr(s1) Π π[a_t|s_t,θ] Pr(s_{t+1}|s_t,a_t)` (eq. 19.22); maximize `E[r[τ]]` and use the log trick `∂log f/∂z = (1/f)∂f/∂z` (eq. 19.26): `θ ← θ + α (1/I) Σ_i Σ_t ∂log π[a_it|s_it,θ]/∂θ · r[τ_i]` (eq. 19.29); past rewards do not affect the current step and can be dropped (eq. 19.31); the dynamics term vanishes, so the Markov property is not assumed (UDL p.403-405).
- **REINFORCE**: discounted return from t and `γ^t` in the step (eq. 19.32-19.33) (UDL p.405). High variance → baseline `b` (eq. 19.34-19.37) and state-dependent baseline `b[s] = v[s,φ]` (advantage; eq. 19.38-19.39) (UDL p.405-407). Control variates (UDL p.406).
- **Actor-critic**: approximate the future return by `r_t + γ v[s_{t+1},φ]`; actor = policy network, critic = value network, training by bootstrapping (eq. 19.40-19.42) (UDL p.407-408).

## 5. Offline RL and Decision Transformer (UDL p.408-409)
`[from source]` Offline/batch RL learns from past trajectories without interacting; it differs from imitation learning (which does not see rewards and replicates). The **decision transformer** treats it as sequence prediction: states, actions and *returns-to-go* `R_{t:T} = Σ r` as inputs of a decoder with masked attention; at inference the desired return is set and decremented.

## 6. RLHF and modern policy methods (UDL p.411-412 — notes)
- `[from source]` Modern methods: natural policy, **TRPO** (KL constraint between policies), **PPO** ("clipped" loss to limit the update), GAE, A3C, soft actor-critic (UDL p.411-412).
- `[from source]` **RLHF** (InstructGPT → ChatGPT): (1) fine-tuning a decoder with human-written prompt-response pairs; (2) annotators indicate which of several responses they prefer and a **reward model** is trained (another transformer that returns a scalar); (3) the chatbot is trained to maximize the reward, with PPO, because gradients cannot be derived through text sampling (UDL p.412). `[DATED 2023]`.
- `[extrapolation]` Later variants (DPO, RLAIF, GRPO etc.) are not in the collection.

## 7. Landmarks cited (UDL p.410) `[DATED]`
DQN (Mnih 2015), AlphaGo (2016), Dota 2 (2019), Cicero (2022), AlphaTensor (2022), TSP.

## 8. Decisions
- Choosing between value-based (DQN) and policy-based: a stochastic policy is needed when the state is partially observable (UDL p.402).
- Scarce/dangerous data (cars, finance): offline RL and decision transformer (UDL p.408).
- Safety: see `14-etica-e-uso-responsavel.md` (outer alignment: misspecified loss; e.g., rewarding piece captures yields draws, UDL p.435).
