# Multi-Agent Pathfinding: Combined Solver Approach

## Overview

Multi-Agent Pathfinding (MAPF) aims to find collision-free paths for multiple agents, ensuring no intersections or collisions occur. This challenge is critical in environments where autonomous entities operate simultaneously, such as robotics, video game development, and logistics. The combined solver strategy initially employs algorithms similar to A* for path creation. It identifies conflicts, attempting resolution with an optimal solver up to three times. If unresolved, the scenario is labeled unsolvable, maintaining a balance between solving speed and solution quality. Optimal resolutions are integrated back into the agent paths, iterating until all conflicts are resolved or deemed unsolvable.

## Using `combined_solver.py`: Detailed Process

### Configuration Options

All arguments are optional, each with a default setting ensuring immediate usability.

- `-s`, `--scen-file`: Specifies the path to a scenario (*.scen*) file. A default scenario is included in the repository.
- `-n`, `--number-agents`: Defines the number of agents to find paths for, defaulting to the first 30 agents.
- `-m`, `--modified-search`: Toggles between modified A* (default, true) and classic A* for initial pathfinding. Modified A* aims to diversify paths by prioritizing unvisited vertices with equal heuristic and distance values.
- `-t`, `--timeout`: Sets the maximum allowed time for solving, measured in seconds.
- `-c`, `--concise`: Controls output verbosity. By default (false), it prints detailed visualizations of conflicts and unsolvable scenarios to the output.

### Execution Flow

1. **Initial Pathfinding:** Utilizes A* or modified A* for preliminary paths.
   - Modified A* enhances path diversity by preferring less traveled vertices, detailed in `informed_search.py`.
2. **Conflict Identification and Ordering:**
   - Conflicts, categorized into edge, position, and path types, are detected and prioritized by occurrence time in `conflicts.py`.
3. **Resolution Loop:** Repeats until a timeout or no resolvable conflicts remain.
   - Early conflicts are tackled first, with repetitive unsolvable ones marked accordingly.
   - A `Subproblem` instance encapsulates each conflict, tailoring the submap size and agent considerations based on conflict type and previous attempts.
   - The optimal solver addresses the subproblem; successful resolutions update agent paths and conflict lists, while unresolved issues queue for reattempts.

### Note on the Optimal Solver Integration

The `optimal_solver.py` uses an optimal solver in Picat, created by my supervisor. Unfortunately, I can't share this part publicly due to copyright and privacy reasons. Your understanding is appreciated.


