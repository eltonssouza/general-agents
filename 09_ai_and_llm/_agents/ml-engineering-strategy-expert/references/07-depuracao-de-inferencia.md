# 07 - Debugging inference algorithms: the Optimization Verification Test (MLY ch. 44-46, p.85-89)

## Pattern (ch. 44, p.85-86)
- [from source] Many systems learn a **scoring function Score_A(S)** (e.g. speech recognition with Score_A(S) = P(S|A), the probability of transcription S given audio A) and then search for the S that maximizes it (arg max). With 50,000 words there are 50,000^N sentences of length N, so approximate search is used, such as **beam search** (keeps K candidates); such algorithms **do not guarantee** finding the maximum (p.85).
- [from source] If the output is wrong ("I love robots" instead of "I love machine learning"), there are two causes: (1) **search algorithm problem** (it did not find the S that maximizes); (2) **objective/scoring function problem** (the estimate failed to recognize the correct transcription). The priorities differ greatly and choosing at random wastes effort (p.85).
- [from source] **Optimization Verification Test:** let S_out be the output and S* the correct transcription; compute Score_A(S*) and Score_A(S_out) and compare (p.86):
  - **Case 1: Score_A(S*) > Score_A(S_out)** -> the score is right; the **search** failed to choose the S with the highest score; improve the search (e.g. increase the beam width) (p.86).
  - **Case 2: Score_A(S*) <= Score_A(S_out)** -> the **scoring function** failed to give the correct output a strictly higher score; improve how you learn/approximate Score_A (p.86).
- [from source] In practice, apply it to each dev error and count: if 95% of errors come from the scoring function and 5% from optimization, improving the search eliminates only ~5% of errors; focus on the scoring (p.86).

## General form (ch. 45, p.87)
- [from source] It applies when, given input x, you can compute Score_x(y) and use an approximate algorithm for arg max_y Score_x(y), suspecting the search sometimes fails. If Score_x(y*) > Score_x(y_out), blame the **optimization**; otherwise, blame the computation of Score_x(y) (p.87).
- [from source] Example of Chinese->English translation with Score_C(E) = P(E|C) and heuristic search (p.87). It is a common "design pattern" in AI: learn an approximate score and use an approximate maximizer (p.87).

## Reinforcement learning (ch. 46, p.88-89)
- [from source] Helicopter example in an **autorotation** maneuver (landing with the engine off): define a **reward function R(T)** over the trajectory T (e.g. crash = -1,000; safe landing positive, depending on smoothness); R is usually chosen by hand and is not easy to design; the RL algorithm tries to maximize R(T) with various approximations and may fail (p.88-89).
- [from source] If performance is worse than the human pilot's: let T_human be the pilot's trajectory and T_out the algorithm's; test **R(T_human) > R(T_out)?** If so, the reward is right and RL fails -> improve the RL algorithm; if not (R(T_human) <= R(T_out)), the reward does not capture what a good landing is -> improve R (p.89).
- [from source] In this case Score(T) = R(T) and the "optimization" is the RL algorithm; with no input x, Score(.) is enough. Difference: you compare against a human (good, not necessarily optimal); it is enough to have some y* that is **superior** to the current output, even if not optimal (p.89).

Tool: `python -I scripts/mly_diagnose.py optverify --pairs "s*:sout;..."` (counts cases 1 and 2 and shows the ceiling) (p.86-87, 89).
