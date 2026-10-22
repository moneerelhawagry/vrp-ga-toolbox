# Member 4 — Crossover & Mutation

Contains the Member 4 assignment part:
- `crossover/multi_point.py`: configurable n-point crossover for binary/float sequences.
- `crossover/order_crossover.py`: Order Crossover (OX) for valid permutations.
- `mutation/swap.py`: swaps two positions.
- `mutation/inversion.py`: reverses a selected segment.
- `mutation/scramble.py`: shuffles a selected segment.
- tests for crossover and mutation.

Run tests from this folder:
`python -m unittest discover -s tests -v`

No third-party packages are required.

Integration note: these classes expose `crossover(...)` and `mutate(...)`. Match signatures to your team's shared base classes if needed. Use OX for CVRP permutations; multi-point crossover can create duplicate/missing customer IDs.
