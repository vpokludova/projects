# Multi-Agent Pathfinding (MAPF) Solver

## Overview
The MAPF Solver is a command-line tool for solving multi-agent pathfinding problems using informed search algorithms. It takes a scenario file containing agent start positions and destinations and finds agent paths using A* or a modified A* search algorithm. The tool then detects conflicts and resolves them iteratively.

## Features
- Supports standard A* and modified A* search algorithms
- Detects and resolves conflicts among agents
- Configurable number of agents and search parameters
- Timeout mechanism to prevent infinite execution
- Logs detailed information for debugging
- Provides animation of agent paths

## Installation
Ensure you have the following dependencies installed:

- Python 3.x
- Required Python modules:
  - `matplotlib`
  - `numpy`
  - `pandas`

Additionally, you must have picat binary installed (http://picat-lang.org/download.html), so that the optimal solver can run. 

## Usage
Run the MAPF solver from the command line with the following options:

```sh
python mapf_solver.py [-s SCEN_FILE] [-n NUMBER_AGENTS] [-m] [-t TIMEOUT] [-c] [--animate-paths]
```

### Command-line Arguments
| Argument | Description |
|----------|-------------|
| `-s`, `--scen-file` | Specify the scenario file (default: `maze-32-32-4-even-2.scen`). |
| `-n`, `--number-agents` | Number of agents to process (-1 for all, default: 30). |
| `-p`, `--percentage-agents` | Specify the percentage of agents to read and process. |
| `-m`, `--modified-search` | Use modified A* algorithm (default: True). |
| `-t`, `--timeout` | Maximum execution time in seconds (default: 200). |
| `-c`, `--concise` | Print concise conflict information (default: False). |
| `--animate-paths` | Create animation of agent paths before and after solver (default: False). |

## Execution Flow
1. **Parse command-line arguments**: Reads input parameters and sets defaults if not provided.
2. **Load map and agents**: Reads the scenario file and initializes the map and agents.
3. **Pathfinding**:
   - Uses either modified A* or standard A* to compute initial paths for each agent.
4. **Conflict Detection**:
   - Identifies conflicts between agents and prioritizes them.
5. **Conflict Resolution**:
   - Iteratively resolves conflicts using a subproblem solver.
   - Keeps track of unsolvable conflicts to avoid infinite loops.
6. **Timeout Handling**:
   - If execution time exceeds the specified timeout, the solver terminates.
7. **Logging and Debugging**:
   - Logs relevant execution details to `mapf_solver.log`.
8. **Animation**:
   - Displays an animation of the final agent paths.

## Logging
The solver logs events to `mapf_solver.log`. Logging levels include:
- **INFO**: General execution details.
- **DEBUG**: Detailed debug information.

## Example Usage
### Run with default settings:
```sh
python mapf_solver.py
```

### Specify a scenario file and number of agents:
```sh
python mapf_solver.py -s my_scenario.scen -n 50
```

### Disable modified A* and set a timeout:
```sh
python mapf_solver.py -m False -t 300
```

### Enable concise output:
```sh
python mapf_solver.py -c
```