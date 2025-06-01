# MAPF Solver

![Animation Preview](./data/path_animation.gif)  
*A visualization of agent movement before and after conflict resolution.*

## Overview

The **Multi-Agent Pathfinding (MAPF) Solver** computes collision-free paths for multiple agents in a shared, grid-based environment. This project combines a **fast, heuristic-driven approach** for initial path planning with a **local optimal solver** that resolves conflicts only where they occur.

By limiting the use of expensive global re-planning, this hybrid method scales better to complex environments and high agent counts—making it suitable for applications like autonomous robots, warehouse systems, or traffic simulations.

## How It Works

1. **Initial Pathfinding**  
   Agents independently compute their shortest paths using **A\*** or a **modified A\*** variant that discourages congestion by factoring in prior edge usage.

2. **Conflict Detection**  
   The solver detects collisions such as:
   - **Position conflicts** (two agents at the same cell)
   - **Edge conflicts** (two agents crossing the same edge)
   - **Path conflicts** (longer sequences of repeated interference)

3. **Local Conflict Resolution**  
   Conflicts are encapsulated into **subproblems**, which are solved using an **external optimal solver** (via Picat). This allows precise conflict handling without re-solving the entire problem.

4. **Iteration Until Resolution**  
   The solver dynamically reorders conflicts and escalates complexity when needed, re-solving only affected areas until all conflicts are resolved or the time limit is reached.

5. **Visualization**  
   Agent movements can be animated before and after resolution to clearly show how conflicts were resolved.

## Installation

1. **Install Python Dependencies**

```sh
pip install -r requirements.txt
```

2. **Install Picat**

Download Picat from [http://picat-lang.org/download.html](http://picat-lang.org/download.html) if not already downloaded.

## Usage

To run the MAPF solver:

```sh
python source/combined_solver.py -s path/to/scenario.scen -n 30 -m True -t 200
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `-s`, `--scen-file` | Path to scenario file |
| `-n`, `--number-agents` | Number of agents to use (-1 for all) |
| `-m`, `--modified-search` | Use congestion-aware A* |
| `-t`, `--timeout` | Max solver time in seconds |
| `-c`, `--concise` | Use concise logging format |

## Research Context

This solver was developed for a thesis exploring whether **combining fast heuristic search with local optimal conflict resolution** can improve scalability and performance in large-scale multi-agent systems.

The approach is tested across diverse map styles, sizes, and agent densities to evaluate how it compares to fully naive and fully optimal solvers in terms of both runtime and solution quality.


