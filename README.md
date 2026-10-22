# Genetic Algorithm Toolbox & Capacitated Vehicle Routing Problem (CVRP)

**Faculty of Computing and Artificial Intelligence, Cairo University**  
*Department of Computer Science — Soft Computing Course (Assignment 1)*

---

## 📌 Project Overview
This project consists of two core components built from scratch in Python (without third-party GA libraries):
1. **Generic Genetic Algorithm (GA) Toolbox:** A modular, object-oriented framework for solving optimization problems.
2. **Capacitated Vehicle Routing Problem (CVRP) Solver:** A real-world application utilizing the GA toolbox to optimize fleet delivery routes without exceeding vehicle load capacities.

---

## 🧰 Toolbox Features (Part 1)
- **Chromosome Representations:** Binary, Integer, and Floating-Point.
- **Selection Operators:** Tournament Selection, Roulette Wheel Selection.
- **Crossover Operators:** Multi-Point Crossover, Order Crossover (OX).
- **Mutation Operators:** Swap Mutation, Inversion Mutation, Scramble Mutation.
- **Replacement Strategies:** Elitist Replacement, Generational Replacement.
- **Constraint Handling:** Feasibility checks and penalty/repair functions for handling infeasible individuals.

---

## 🚚 CVRP Solver (Part 2)
- Models vehicle routes starting and ending at a central depot.
- Minimizes total travel distance across all routes.
- Enforces vehicle capacity constraints against customer demand.
- Outputs vehicle-by-vehicle routes, cumulative load, and total distance.

---

## 📁 Repository Structure
```
ga_toolbox/
├── chromosome/      # Binary, Integer, and Floating-Point representations
├── selection/       # Selection strategies
├── crossover/       # Crossover operators
├── mutation/        # Mutation operators
├── replacement/     # Generational & Elitist replacement
└── ga_engine.py     # Core Genetic Algorithm execution loop

cvrp/
├── problem.py       # Data model (distances, demands, vehicle limits)
├── decoder.py       # Permutation to vehicle routes decoder (Split algorithm)
├── fitness.py       # Distance evaluation
└── feasibility.py   # Capacity constraint checking

tests/               # Unit tests for all GA components and CVRP
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Git

### Running Tests
```bash
python -m unittest discover tests
```
