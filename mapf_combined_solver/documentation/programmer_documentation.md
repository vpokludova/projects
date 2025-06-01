# MAPF Solver - Program Documentation

## Table of Contents

- [MAPF Solver - Program Documentation](#mapf-solver---program-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Project Structure](#project-structure)
  - [Dependencies](#dependencies)
  - [Configuration and Command-line Arguments](#configuration-and-command-line-arguments)
  - [Component Breakdown](#component-breakdown)
    - [1. **Map and Agent Representation**](#1-map-and-agent-representation)
    - [2. **Pathfinding Algorithms**](#2-pathfinding-algorithms)
    - [3. **Conflict Detection and Handling**](#3-conflict-detection-and-handling)
    - [4. **High-Level Solver**](#4-high-level-solver)
  - [In-Depth Class and Method Description](#in-depth-class-and-method-description)
    - [Class `Agent`](#class-agent)
      - [Attributes](#attributes)
      - [Methods](#methods)
    - [Module `conflicts`](#module-conflicts)
      - [Class `Conflict`](#class-conflict)
        - [Attributes](#attributes-1)
        - [Methods](#methods-1)
      - [Other Functions in the Module](#other-functions-in-the-module)
        - [Function `identify_conflicts`](#function-identify_conflicts)
        - [Function `update_conflicts`](#function-update_conflicts)
        - [Function `get_conflict_pairs`](#function-get_conflict_pairs)
        - [Function `print_conflict_info`](#function-print_conflict_info)
        - [Function `sorting_key`](#function-sorting_key)
        - [Function `reorder_conflicts`](#function-reorder_conflicts)
        - [Function `update_agents_from_solution`](#function-update_agents_from_solution)
        - [Function `insert_new_subpath`](#function-insert_new_subpath)
        - [Function `split_agents`](#function-split_agents)
        - [Function `agents_stay_at_destination`](#function-agents_stay_at_destination)
    - [Class `Edge`](#class-edge)
      - [Attributes](#attributes-2)
      - [Methods](#methods-2)
    - [Class `Map`](#class-map)
      - [Attributes](#attributes-3)
      - [Methods](#methods-3)
    - [Function `read_agents(filename: str, n_of_agents: int = -1, percentage_of_agents: int = 100) -> Tuple[List[Agent], str]`](#function-read_agentsfilename-str-n_of_agents-int---1-percentage_of_agents-int--100---tuplelistagent-str)
    - [Module `informed_search`](#module-informed_search)
      - [Class `Vertex`](#class-vertex)
        - [Attributes](#attributes-4)
        - [Methods](#methods-4)
      - [Other Functions in the Module](#other-functions-in-the-module-1)
        - [Function `get_path(origin: Vertex, destination: Vertex) -> List[Tuple[int, int]]`](#function-get_pathorigin-vertex-destination-vertex---listtupleint-int)
        - [Function `valid_node(nodes: List[List[str]], node: Tuple[int, int]) -> bool`](#function-valid_nodenodes-listliststr-node-tupleint-int---bool)
        - [Function `get_neighbors(nodes: List[List[str]], node: Tuple[int, int]) -> List[Tuple[int, int]]`](#function-get_neighborsnodes-listliststr-node-tupleint-int---listtupleint-int)
        - [Function `heuristic(origin: Tuple[int, int], destination: Tuple[int, int]) -> int`](#function-heuristicorigin-tupleint-int-destination-tupleint-int---int)
        - [Function `informed_search(nodes: List[List[str]], origin_coord: Tuple[int, int], destination_coord: Tuple[int, int]) -> List[Tuple[int, int]]`](#function-informed_searchnodes-listliststr-origin_coord-tupleint-int-destination_coord-tupleint-int---listtupleint-int)
        - [Function `modified_informed_search(nodes: List[List[str]], origin_coord: Tuple[int, int], destination_coord: Tuple[int, int], used_edges_dict: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]) -> List[Tuple[int, int]]`](#function-modified_informed_searchnodes-listliststr-origin_coord-tupleint-int-destination_coord-tupleint-int-used_edges_dict-dicttupletupleint-int-tupleint-int-int---listtupleint-int)
        - [Function `rank_neighbors(coord: Tuple[int, int], neighbors_unranked: List[Tuple[int, int]], diction: Dict, dest: Tuple[int, int], time: int) -> Dict[Tuple[int, int], int]`](#function-rank_neighborscoord-tupleint-int-neighbors_unranked-listtupleint-int-diction-dict-dest-tupleint-int-time-int---dicttupleint-int-int)
    - [Class `Subproblem`](#class-subproblem)
      - [Attributes](#attributes-5)
      - [Methods](#methods-5)
    - [Class `Optimal_Solver`](#class-optimal_solver)
      - [Attributes](#attributes-6)
      - [Methods](#methods-6)
    - [Module `utils.py`](#module-utilspy)
      - [Function `update_edge_dict`](#function-update_edge_dict)
      - [Function `animate_paths`](#function-animate_paths)
    - [Main Entry Point `combined_solver`](#main-entry-point-combined_solver)
      - [Functions:](#functions)
        - [`main() -> None`](#main---none)

## Introduction
This project is a **Multi-Agent Pathfinding (MAPF) Solver** that aims to compute collision-free paths for multiple agents navigating a shared environment. It utilizes **A\*** or **modified A\*** to find initial paths, then detects and resolves conflicts using an **optimal solver-based repair approach**. 

The core functionality includes:

- **Pathfinding**: Uses informed search algorithms (A* or a modified version) to compute paths for agents from their origin to destination.
- **Conflict Detection**:  Identifies conflicts where multiple agents occupy the same position or traverse the same edge simultaneously.
- **Conflict Resolution**: Attempts to resolve conflicts by generating subproblems and using an optimal solver to compute alternative paths.
- **Dynamic Reordering**: Orders conflicts based on priority and iteratively resolves them until a valid solution is found or the timeout is reached.
- **Logging and Visualization**: Tracks execution progress and provides visual representation of final agent paths.

## Project Structure
The project contains the following files/directories:

```bash
RP-POKLUDOVA/                 # Root directory
├── README.md                 # Introductory project information
├── requirements.txt          # List of Python dependencies
├── data/                     # Experiment data and map images
├── documentation/            # Documentation files
└── source/                   # Source code directory
    ├── __pycache__/          # Python cache for source files
    ├── picat/                # Picat scripts for optimal solver
    ├── resources/            # Resource files (maps and scenarios)
    │   ├── maps/             # Saved .map files
    │   └── scens/            # Saved .scen files
    ├── agent.py              # Agent representation
    ├── combined_solver.py    # Main entry point for a single MAPF problem instance
    ├── conflicts.py          # Conflict detection and resolution logic
    ├── edges.py              # Edge representation
    ├── informed_search.py    # Informed search algorithms: A*, etc.
    ├── map.py                # Map and agent data structures, load functions
    ├── optimal_solver.py     # Optimal solver interface and logic
    ├── subproblem.py         # Handling of local subproblems or repairs
    └── utils.py              # Miscellaneous helper utilities
```

## Dependencies
The following dependencies are required 

- Python 3.x
- Required Python modules:
  - `pandas`
  - `matplotlib`
  - `numpy`

which you can install using:

```sh
pip install -r requirements.txt
```

Additionally, you must have picat binary installed (http://picat-lang.org/download.html), so that the optimal solver can run. 

## Configuration and Command-line Arguments
The program accepts several command-line arguments to modify its behavior:

| Argument | Description |
|----------|-------------|
| `-s`, `--scen-file` | Specify the scenario file (default: `maze-32-32-4-even-2.scen`). |
| `-n`, `--number-agents` | Number of agents to process (-1 for all, default: 30). |
| `-m`, `--modified-search` | Use modified A* algorithm (default: True). |
| `-t`, `--timeout` | Maximum execution time in seconds (default: 200). |
| `-c`, `--concise` | Print concise conflict information (default: False). |
| `--animate-paths` | Create animation of agent paths before and after solver (default: False). |


## Component Breakdown

### 1. **Map and Agent Representation**  
These modules define the core components of the Multi-Agent Pathfinding (MAPF) problem: the grid-based environment and the agents navigating it.

- **`map.py`** – Loads map data from `source/resources/maps/`, representing it as a 2D grid. It reads map files, initializes obstacles and free spaces, and links scenario files to the correct map.  
- **`agents.py`** – Defines the `Agent` class, which tracks each agent’s starting position, goal, index, and computed path. Agents are initialized from scenario files (`.scen`) in `source/resources/scens/`.  

These modules establish the problem space, enabling the solver to manage agent movement and validate constraints within the environment.


### 2. **Pathfinding Algorithms**  
This module implements pathfinding strategies for agents before considering conflicts.

- **`informed_search.py`** – Implements:  
  - **A*** – A heuristic-based pathfinding algorithm using Manhattan distance to find the shortest path.  
  - **Modified A*** – A variant that ranks paths partly based on edge usage to reduce congestion and balance agent movement.  

These algorithms take a map, an agent's start and goal positions, and optionally existing constraints, returning an optimal or congestion-aware path.

### 3. **Conflict Detection and Handling**  
After initial paths are found, the system detects and resolves conflicts iteratively to ensure collision-free agent movement.

- **`conflicts.py`** – Identifies and categorizes conflicts:  
  - **Position conflicts** – Two agents occupying the same cell simultaneously.  
  - **Edge conflicts** – Two agents using the same edge at the same time.
  - **Path conflicts** – Agents repeatedly colliding in sequence.  

  The module provides functions to reorder conflicts and apply path modifications to prevent future collisions.

- **`edges.py`** – Defines edge-based movement constraints and represents connections between nodes, enabling edge conflict detection.  

These modules work together to iteratively refine agent paths and maintain a feasible solution while resolving collisions dynamically.

### 4. **High-Level Solver**  
The MAPF (Multi-Agent Path Finding) solver implements a hierarchical approach to coordinate multiple agents' paths while avoiding conflicts.

- **`subproblem.py`** – Creates localized conflict resolution areas:
  - Extracts a relevant submap around identified conflicts
  - Defines time windows for conflict resolution (`start_time` to `end_time`)
  - Maps agents and positions between main problem and subproblem
  - Identifies "avoids" (positions occupied by other agents) that must be respected
  - Supports different conflict types: PATH, POSITION, and EDGE

- **`optimal_solver.py`** – Interfaces with an external SAT-based solver (uses Picat):
  - Translates the subproblem into the solver's required format
  - Transforms agent positions, map structure, and constraints into Picat code
  - Manages makespan (maximum path length) and sum-of-costs objectives
  - Runs the external solver and captures its output

- **Main solver loop** (in main function of `combined_solver.py`):
  - Uses modified or standard A* to find initial paths for all agents
  - Identifies conflicts between agent paths
  - Creates subproblems for each conflict and solves them iteratively
  - Updates agent paths based on subproblem solutions
  - Handles timeout conditions and tracks unsolvable conflicts
  - Uses an escalation strategy for difficult conflicts (increasing submap size, makespan)

This approach efficiently manages complex multi-agent coordination by focusing computational resources on conflict areas rather than re-planning entire paths, while using an optimal solver for the most difficult path conflicts.


## In-Depth Class and Method Description

### Class `Agent`
- **Description**: Represents an agent navigating a grid-based environment, storing its start position, goal, and current, computed path.

#### Attributes
- `origin: Tuple[int, int]` – The agent’s starting coordinates.
- `destination: Tuple[int, int]` – The target destination coordinates.
- `index: int` – The agent's unique index in the list of agents for the current scenario.
- `path: List[Tuple[int, int]]` – The computed path from origin to destination.

#### Methods
- `__init__(origin: Tuple[int, int], dest: Tuple[int, int], index: int) -> None`
  - **Description**: Initializes an agent with a start position, goal, and index.
  - **Parameters**:
    - `origin`: The agent's starting coordinates (x, y).
    - `dest`: The agent's goal coordinates (x, y).
    - `index`: The agent's index in the scenario.
  - **Example Usage**:
    ```python
    agent = Agent(origin=(0, 0), dest=(5, 5), index=1)
    ```

- `__repr__() -> str`
  - **Description**: Returns a string representation of the agent, which is its index. Allows for more readable and interpretable logging, printing, and debugging.
  - **Returns**: A string representation of the agent's index.
  - **Example Usage**:
    ```python
    agent = Agent(origin=(0, 0), dest=(5, 5), index=1)
    print(agent)  # Output: '1'
    ```
---
### Module `conflicts`

#### Class `Conflict`
- **Description**: Represents a conflict detected in the MAPF solver. Conflicts occur when multiple agents occupy the same position, traverse the same edge, or follow conflicting paths.

##### Attributes
- `type: ConflictType` – The type of conflict (EDGE, POSITION, or PATH).
- `time: int` – The timestep at which the conflict occurs.
- `agents: List[int]` – The indices of agents involved in the conflict.
- `position: Optional[Tuple[int, int]]` – The conflicting position (for position conflicts).
- `edge: Optional[Edge]` – The conflicting edge (for edge conflicts).
- `path: Optional[List[Tuple[int, int]]]` – The conflicting path (for path conflicts).

##### Methods
- `__init__(type: ConflictType, time: int, agents: List[int] = [], position: Optional[Tuple[int, int]] = None, edge: Optional[Edge] = None, path: Optional[List[Tuple[int, int]]] = None) -> None`
  - **Description**: Initializes a conflict instance with the specified attributes.
  - **Parameters**:
    - `type`: Type of conflict (EDGE, POSITION, or PATH).
    - `time`: The timestep when the conflict occurs.
    - `agents`: List of agent indices involved in the conflict.
    - `position`: The conflicting position (if applicable).
    - `edge`: The conflicting edge (if applicable).
    - `path`: The conflicting path (if applicable).
  - **Example Usage**:
    ```python
    conflict = Conflict(ConflictType.EDGE, time=5, agents=[1, 2], edge=Edge((2,3), (3,3)))
    ```

- `__eq__(other: object) -> bool`
  - **Description**: Checks equality between two conflicts by comparing their attributes.
  - **Parameters**:
    - `other`: Another `Conflict` instance.
  - **Returns**: `True` if conflicts are identical, otherwise `False`.

- `__hash__() -> int`
  - **Description**: Computes a unique hash value for the conflict using SHA-256 hashing.
  - **Returns**: A unique integer hash value.

- `__repr__() -> str`
  - **Description**: Provides a string representation, describing the conflict for logging and debugging purposes.
  - **Returns**: A formatted string describing the conflict type, time, agents, and relevant details.

#### Other Functions in the Module

##### Function `identify_conflicts`
- **Description**: Detects conflicts in agent paths by analyzing their movements at each time step throughout the scenario. The function systematically evaluates the positions and edges used by agents to identify and classify conflicts into three categories:
  - **Position conflicts**: Occur when multiple agents attempt to occupy the same position at the same time step, leading to direct collisions.
  - **Edge conflicts**: Occur when multiple agents attempt to traverse the same edge in the same direction or in opposite directions at the same time step.
  - **Path conflicts**: Extended movement conflicts derived from **edge conflicts**, where the movement patterns of multiple agents consistently overlap over several time steps, requiring long-term resolution strategies.
  
  The function iterates over each time step, checking for conflicts by grouping agents based on their locations or edges. It ensures that **early-stage conflicts** are detected and flagged before they escalate into larger, harder-to-resolve movement issues. Additionally, detected conflicts are refined and updated to prevent redundancy and improve the efficiency of conflict resolution in subsequent stages.
  
- **Parameters**:
  - `agents: List[Agent]` – The list of agents in the scenario, each with a computed path.
  - `max_length: int` – The maximum path length among all agents, used to determine the number of time steps for conflict detection.
  - `start: int` – The starting time step for conflict detection (default: `0`), allowing for partial checks in iterative resolution processes.

- **Returns**: 
  - `List[Conflict]` - List of identified conflicts.


##### Function `update_conflicts`
- **Description**: Processes and categorizes detected conflicts into **confirmed edge, position, and path conflicts** by refining the initially identified issues. It ensures that **edge conflicts** are properly recorded and, when applicable, extended into **path conflicts** to account for long-term movement constraints. Additionally, **unresolved path conflicts** are tracked and carried forward, preventing repetitive conflict cycles and improving resolution efficiency. The function also eliminates redundant or resolved conflicts, ensuring a cleaner and more effective conflict list.
- **Parameters**:
  - `conflicts: List[Conflict]` – The list of initially detected conflicts, including position, edge, and path conflicts.
  - `agents: List[Agent]` – The list of agents involved in the scenario, used to refine and validate conflict occurrences.
- **Returns**:
  - `List[Conflict]` - Updated list of conflicts.


##### Function `get_conflict_pairs`
- **Description**: Identifies and groups agents that share the same position or edge at a given time step, helping to detect **position conflicts** (multiple agents at the same location) and **edge conflicts** (multiple agents attempting to use the same edge simultaneously). This function efficiently maps agents to their respective locations or transitions, ensuring that conflicts are properly structured for further resolution.
- **Parameters**:
  - `agents: List[Agent]` – The list of agents whose paths are analyzed for conflicts.
  - `time: int` – The time step at which conflicts are checked, ensuring that conflicts are identified as they occur in real-time.
  - `is_position: bool` – Determines whether to check for **position conflicts** (`True`) or **edge conflicts** (`False`), allowing for targeted conflict detection.
- **Returns**: 
  - `Dict[Union[Tuple[int, int], Edge], List[int]]`- Returns a dictionary mapping either a position or Edge to a list of corresponding agent indexes.

##### Function `print_conflict_info`
- **Description**: Prints a summary of the number of conflicts detected, categorized into edge, position, and path conflicts.
- **Parameters**:
  - `conflicts: List[Conflict]` – The list of detected conflicts.
- **Returns**: `Tuple[int, int, int]` - Represents number of position conflicts, number of edge conflicts, number of path conflicts.

##### Function `sorting_key`
- **Description**: Defines a sorting key for conflict prioritization, giving precedence to path conflicts, followed by edge and position conflicts.
- **Parameters**:
  - `conflict: Conflict` – A conflict object to be sorted.
- **Returns**: 
  - `Tuple[int, int]` - A pair where first is time and second is priority value.

##### Function `reorder_conflicts`
- **Description**: Sorts conflicts based on their type and occurrence time to ensure efficient resolution. The function prioritizes **edge conflicts** first, as they often lead to path conflicts and require immediate handling. **Path conflicts** are sorted next, as they represent longer-term movement issues that may impact multiple agents. **Position conflicts** are given the lowest priority, as they are often the result of earlier unresolved issues. This ordering helps optimize the conflict resolution process by addressing the most critical issues first.
- **Parameters**:
  - `conflicts: List[Conflict]` – The list of conflicts to be reordered.
- **Returns**: 
  - `List[Conflict]` - The sorted list of conflicts.

##### Function `update_agents_from_solution`
- **Description**: Updates agent paths based on the solution provided by an optimal solver. It modifies agent paths by inserting the computed subpaths into the main paths and updates the maximum path length.
- **Parameters**:
  - `subproblem: Subproblem` – The subproblem containing localized conflict resolution.
  - `solver_output: str` – The output from the optimal solver.
  - `all_agents: List[Agent]` – The list of all agents.
  - `max_length: int` – The current maximum path length.
- **Returns**
  - `List[Agents]` - The updated list of agents.
  - `int` - New maximum length of an agent path.

##### Function `insert_new_subpath`
- **Description**: Inserts a newly computed subpath into an agent’s existing path, ensuring smooth integration of newly updated paths.
- **Parameters**:
  - `path: List[Tuple[int, int]]` – The original agent path.
  - `subpath: List[Tuple[int, int]]` – The computed subpath to be inserted.
  - `start_index: int` – The index at which the subpath should be inserted.
- **Returns**
  - `List[(int, int)]` - The updated path. 

##### Function `split_agents`
- **Description**: Split agents into two groups based on the direction of travel across the same edge, determining agent grouping based on their position at a specific time step.
- **Parameters**:
  - `edge_conflict: Conflict` – The edge conflict being analyzed.
  - `agents: List[Agent]` – The list of agents.
- **Returns**:
  - `List[int]` - The list of agent indices for agents moving in one direction
  - `List[int]` - The list of agent indices for agents moving in the other edge direction.

##### Function `agents_stay_at_destination`
- **Description**: Extends agent paths to all be of `max_length` length. If not of that length, then the final position in the current agent map (aka the destination position) is copied until the desired length is reached. This is used to emulate 'stay at destination' behavior of agents. As opposed to dissapearing once reaching the goal.
- **Parameters**:
  - `agents: List[Agent]`: The list of agents.
  - `max_length: int`: The length that all agent paths should be extended to.
- **Returns**:
  - `List[Agent]` - The updated agents list.

---
### Class `Edge`
- **Description**: Represents an undirected edge between two points in a grid-based environment. The edge is always stored in a consistent order to ensure equality comparisons work correctly.

#### Attributes
- `edge: Tuple[Tuple[int, int], Tuple[int, int]]` – A tuple representing an edge between two points, stored in a consistent order.

#### Methods
- `__init__(p1: Tuple[int, int], p2: Tuple[int, int]) -> None`
  - **Description**: Initializes an edge between two points, ensuring consistent ordering.
  - **Parameters**:
    - `p1`: The first point of the edge.
    - `p2`: The second point of the edge.
  - **Example Usage**:
    ```python
    edge = Edge((2, 3), (3, 3))
    ```

- `first() -> Tuple[int, int]`
  - **Description**: Returns the first point of the edge.
  - **Returns**: The first point of the edge.

- `second() -> Tuple[int, int]`
  - **Description**: Returns the second point of the edge.
  - **Returns**: The second point of the edge.

- `__eq__(other: object) -> bool`
  - **Description**: Checks equality between two edges by comparing their stored tuples.
  - **Parameters**:
    - `other`: Another `Edge` instance.
  - **Returns**: `True` if the edges are identical, otherwise `False`.

- `__hash__() -> int`
  - **Description**: Computes a hash value for the edge.
  - **Returns**: A unique integer hash value.

- `__repr__() -> str`
  - **Description**: Provides a string representation of the edge.
  - **Returns**: A formatted string representation of the edge.

---
### Class `Map`
- **Description**: Represents a grid-based environment for the MAPF solver. It loads the map and agent data from scenario files and provides methods to access the map structure.

#### Attributes
- `agents: List[Agent]` – A list of agents in the scenario.
- `map_file: str` – The filename of the map associated with the scenario.
- `nodes: List[List[str]]` – A 2D grid representation of the map, where each cell contains terrain information.

#### Methods
- `__init__(scen_file: str, n_of_agents: int = -1, percentage_of_agents = 100) -> None`
  - **Description**: Initializes a `Map` instance by loading agents and the map file from a given scenario.
  - **Parameters**:
    - `scen_file`: The scenario file containing agent information.
    - `n_of_agents`: The number of agents to process (`-1` to load all agents).
    - `percentage_of_agents`: The percentage of aggents to process.
  - **Example Usage**:
    ```python
    map_instance = Map("maze-32-32-4-even-2.scen", n_of_agents=30)
    ```

- `read_map() -> List[List[str]]`
  - **Description**: Reads the map file and constructs a 2D grid representation of the environment.
  - **Returns**: A 2D list where each entry is the character at a given coordinate.


### Function `read_agents(filename: str, n_of_agents: int = -1, percentage_of_agents: int = 100) -> Tuple[List[Agent], str]`
- **Description**: Reads agent data from a scenario file and initializes `Agent` instances. Can optionally limit the total number of agents and/or randomly select a percentage of the loaded agents.
- **Parameters**:
 - `filename`: The scenario file containing agent start and goal positions.
 - `n_of_agents`: The number of agents to process (`-1` to load all agents).
 - `percentage_of_agents`: The percentage of loaded agents to randomly select (default: 100, meaning all agents are selected).
- **Returns**: A tuple containing:
 - A list of `Agent` instances initialized from the file (possibly filtered by the specified percentage).
 - The name of the corresponding map file.
- **Example Usage**:
  ```python
  agents, map_file = read_agents("example.scen", n_of_agents=10)
  ```

---

### Module `informed_search`

#### Class `Vertex`
- **Description**: Represents a node in the A* search process, storing distance, heuristic, and predecessor information.

##### Attributes
- `coord: Tuple[int, int]` – The coordinates of the vertex.
- `distance: int` – The distance from the origin.
- `heuristic: int` – The estimated distance to the goal.
- `predecessor: Optional[Vertex]` – The predecessor node in the path.
- `explored: bool` – Whether the node has been processed by A*.
- `ranked: bool` – Whether ranking-based modifications are used.
- `ranked_score: int` – The score assigned for ranking-based pathfinding.
- `val: int` – The total cost of reaching the node (`distance + heuristic + ranked_score`).

##### Methods
- `__eq__(other: object) -> bool`
  - **Description**: Compares two vertices based on their distance or ranking score. If ranking modifications are being used then uses `self.val` which incorporates distance, heuristic, and ranking score; otherwise, uses just `self.distance`.
- `__ne__(other: object) -> bool`
  - **Description**: Analogous to the previous method, but for '*not* equal to'. 
- `__lt__(other: Vertex) -> bool`
  - **Description**: Compares two vertices for priority queue ordering. Again, uses `self.val` if ranked and `self.distance` otherwise.
- `__gt__(other: Vertex) -> bool`
  - **Description**: Analogous to the previous method, but for '*greater* than' not 'less than'.
- `__le__(self, other) -> bool`
  - **Description**: Implements 'less than or equal to' using previously defined methods.
- `__ge__(self, other) -> bool`
  - **Description**: Implements 'greater than or equal to' using previously defined methods.

#### Other Functions in the Module

#####  Function `get_path(origin: Vertex, destination: Vertex) -> List[Tuple[int, int]]`
- **Description**: Reconstructs the path from the origin to the destination using the predecessor chain.
- **Returns**: A list of coordinates representing the path.

##### Function `valid_node(nodes: List[List[str]], node: Tuple[int, int]) -> bool`
- **Description**: Checks if a node is within the map bounds and not an obstacle.
- **Returns**: `True` if valid, `False` otherwise.

##### Function `get_neighbors(nodes: List[List[str]], node: Tuple[int, int]) -> List[Tuple[int, int]]`
- **Description**: Finds valid neighboring positions for a given node that it can move it in one step. 
- **Returns**: A list of valid neighbor coordinates.

##### Function `heuristic(origin: Tuple[int, int], destination: Tuple[int, int]) -> int`
- **Description**: Computes the Manhattan distance heuristic between two points.
- **Returns**: The Manhattan distance.

##### Function `informed_search(nodes: List[List[str]], origin_coord: Tuple[int, int], destination_coord: Tuple[int, int]) -> List[Tuple[int, int]]`
- **Description**: Implements the A* algorithm to find an optimal path from the origin to the destination.
- **Notable Optimizations in `informed_search`**
  1. **Priority Queue Optimization (Heap-Based Expansion)**
     - The use of Python’s `heapq` ensures efficient O(log N) insertion and deletion, improving performance over list-based approaches.

  2. **Lazy Update Instead of Decrease-Key**
     - Since Python’s `heapq` lacks an efficient decrease-key operation, the algorithm pushes a new copy of the vertex with an updated `g` value rather than modifying an existing entry.
     - This avoids an expensive search-and-update operation but results in extra heap insertions. The check `assert not visit.explored` ensures that once a node is fully processed, outdated entries are ignored.

  These optimizations improve efficiency without sacrificing correctness, making the implementation more practical in Python while avoiding unnecessary computations.

- **Returns**: A list of coordinates representing the computed path.

##### Function `modified_informed_search(nodes: List[List[str]], origin_coord: Tuple[int, int], destination_coord: Tuple[int, int], used_edges_dict: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]) -> List[Tuple[int, int]]`
- **Description**: Implements a modified A* algorithm that considers edge usage ranking.
- **Modifications & Improvements in `modified_informed_search`**
  1. **Edge Usage Ranking for Neighbor Prioritization**  
   - Instead of expanding neighbors purely based on `g + h`, the function `rank_neighbors` prioritizes edges based on prior usage (`used_edges_dict`). This modifies the search order, favoring less frequently used paths while still considering heuristic estimates.
   - This ranking mechanism helps distribute path selection more evenly across the graph, potentially avoiding congestion in frequently used routes.
  
  2. **Enhanced Node Representation with Ranking Score**
     - Each `Vertex` now includes a `ranked_score`, affecting its priority in the queue. This helps guide the search dynamically based on historical path usage.

  3. **Priority Queue Adjustments Based on Edge Ranking**
     - When revisiting a node with a shorter path, the ranking score is updated to ensure that reinserted nodes maintain the adjusted priority.

  These modifications introduce an adaptive pathfinding approach that leverages past traversal data to influence routing decisions, potentially reducing congestion in repeated searches.

- **Returns**: A list of coordinates representing the computed path.

##### Function `rank_neighbors(coord: Tuple[int, int], neighbors_unranked: List[Tuple[int, int]], diction: Dict, dest: Tuple[int, int], time: int) -> Dict[Tuple[int, int], int]`
- **Description**: The function `rank_neighbors` assigns a ranking score to each neighbor based on two factors: heuristic distance to the goal and previous edge usage.
  1. **Ranking by Heuristic Distance (`h`)**  
     - The function groups neighbors by their heuristic values (`h = heuristic(n, dest)`), sorting them in ascending order.
     - Neighbors with lower heuristic values (closer to the destination) are given a lower rank (better priority).
     - This ensures that A* still prioritizes nodes that seem closer to the goal.

  2. **Adjusting Ranking Based on Past Edge Usage**  
     - The function checks how frequently each edge `(coord, n)` has been used (`diction[edge]`).
     - Neighbors are again grouped and ranked based on their edge usage count, with lower-ranked paths receiving priority.
     - This ranking is added to the heuristic-based rank, meaning that among equally promising paths, the algorithm favors less frequently used edges.

- **Returns**: A dictionary mapping neighbors to ranking scores.
---

### Class `Subproblem`
- **Description**: Represents a localized conflict resolution subproblem extracted from the main MAPF problem. This subproblem is solved separately to resolve conflicts efficiently.

#### Attributes
- `conflict: Conflict` – The conflict being addressed.
- `extra_time: int` – Additional time allocated for conflict resolution.
- `radius: int` – The radius of the extracted subproblem area.
- `increased_makespan` - How much additional time has been added.
- `start_time: int` – The start time of the subproblem.
- `end_time: int` – The end time of the subproblem.
- `map: Dict[int, List[int]]` – A reduced version of the main map for localized conflict resolution.
- `nodes_main_to_sub: Dict[Tuple[int, int], int]` – Mapping from main map coordinates to subproblem indices.
- `nodes_sub_to_main: Dict[int, Tuple[int, int]]` – Mapping from subproblem indices to main map coordinates.
- `agents: List[Tuple[int, int]]` – List of agent origin-destination pairs.
- `agent_index_main_to_sub: Dict[int, int]` – Mapping from main problem agent indices to subproblem indices.
- `agent_index_sub_to_main: Dict[int, int]` – Mapping from subproblem agent indices to main problem indices.
- `avoids: List[List[Tuple[int, int]]]` – Positions and times that other agents must avoid.

#### Methods
- `__init__(conflict: Conflict, all_agents: List[Agent], main_map: List[List[str]], size_inc: int = 0, map_size: int = 10, sugg_min_radius: int = 2) -> None`
  - **Description**: This constructor initializes a subproblem for resolving conflicts in a multi-agent pathfinding scenario. It dynamically adjusts the time window and spatial constraints based on the type of conflict to create a localized submap for conflict resolution.

  1. **Dynamic Time Window Adjustment**
     - The time range `[start_time, end_time]` is **adaptively determined** based on conflict type:
       - **Path Conflict**: Expands the window relative to the number of conflicting agents and the conflict path length.
       - **Position Conflict**: Uses a radius-based approach to define an adaptive sub-region.
       - **Edge Conflict**: Similar to position conflicts but with an extra buffer to account for movement transitions.
     - This avoids unnecessary computations on large search spaces while ensuring enough context for conflict resolution.

  2. **Submap Creation with Context-Aware Scaling**
     - The function calls either `make_submap_path` (for path conflicts) or `make_submap_other` (for position/edge conflicts), dynamically adjusting:
       - **Map size** based on the severity of the conflict.
       - **Radius selection** using an adaptive minimum threshold (`sugg_min_radius`).
       - **Agent position mappings** from the main map to the local submap.
     - This localized submap reduces the complexity of conflict resolution while still capturing relevant interactions.

  3. **Agent Reindexing for Efficient Lookups**
     - Two mappings (`agent_index_main_to_sub` and `agent_index_sub_to_main`) allow quick translation between the global agent index and the local subproblem.
     - This ensures that agent data remains efficiently accessible without unnecessary lookups.

  4. **Handling Variable Agent Path Lengths**
     - The end destination is determined based on `end_time`, but if the agent’s path is too short, it defaults to the last available position.
     - This prevents out-of-bounds errors and ensures all agents have a valid destination even in truncated paths.

  5. **Avoiding Conflicting Positions**
     - The function `find_avoids` precomputes a list of occupied positions over time, ensuring that future conflict resolution respects other agents' movements.
     - This list is necessary for the input to the picat optimal solver.


- `solve() -> Tuple[str, int]`
  - **Description**: Runs an optimal solver on the subproblem instance.
  - **Returns**: A tuple containing the solver output and return code.

- `inc_ms_upd_avoids(all_agents: List[Agent], extra_time: int = 0) -> None`
  - **Description**: Increases makespan and updates avoid constraints. Used for subproblem instances that need to be retried.

- `add_pos_and_neighbors(...) -> Tuple[int, Dict, Dict, Dict]`
  - **Description**: Adds a position and its neighbors to the submap.

- `rank_neighbors(next_pos: Tuple[int, int], all_neighbors: List[Tuple[int, int]], conflict_path: List[Tuple[int, int]]) -> List[Tuple[int, int]]`
  - **Description**: This function ranks neighboring positions based on their Manhattan distance to `next_pos`, prioritizing the closest ones while avoiding conflicts. It first groups neighbors by distance, sorting them in ascending order for efficient retrieval. The function then selects up to two valid neighbors, skipping those in `conflict_path` to avoid ongoing conflicts. As distances are processed, exhausted entries are removed dynamically to maintain efficiency.

- `make_submap_path(...) -> Tuple[Dict, Dict, Dict]`
  - **Description**: This function constructs a localized submap around a conflict to efficiently resolve agent pathing issues. It selectively adds relevant positions and their neighbors to limit unnecessary computations while preserving path continuity.

    1. **Initializing Submap Structures**
    - The function initializes mappings between the global (`main_map`) and local (`submap`) coordinate systems.
    - It assigns unique indices to nodes (`nodes_main_to_sub`, `nodes_sub_to_main`) for efficient lookups.

    1. **Building the Submap Around the Conflict**
    - The process begins at `start_time`, ensuring that the submap includes positions leading up to the conflict.
    - For each agent in the conflict, it adds their position at `start_time` along with ranked neighbors using `rank_neighbors`, which prioritizes paths that avoid congestion.

    1. **Adding Conflict Path Positions**
    - Iterates through `self.conflict.path`, ensuring that every position and its direct neighbors are included in the submap.
    - The function ranks neighbors of each position, adding only the most relevant ones to keep the submap minimal but effective.

    1. **Extending Beyond the Conflict**
    - The function extends the submap to include the last conflict position and the subsequent non-conflicting positions (up to `loop_end`).
    - If `increase_size` is set, it extends further to allow for larger maneuvering space.

    1. **Connecting Submap to Main Map**
    - Once all conflict-related positions are added, it establishes connections to surrounding positions in `main_map`.
    - The final loop ensures that every node in the submap correctly references its possible neighbors in `main_map`, maintaining pathfinding consistency.


- `make_submap_other(...) -> Tuple[Dict, Dict, Dict, int]`
  - **Description**: This function generates a localized submap for conflict resolution using **Breadth-First Search (BFS)**, expanding outward from the conflict position or edge until a predefined radius or minimum submap size is reached.

  1. **Initializing BFS Expansion**
     - If the conflict is an **edge conflict**, both endpoints of the conflicting edge are added as starting positions in the priority queue.
     - Otherwise, the conflict's position is the single starting point.
     - A **priority queue (`heapq`)** is used to ensure nodes are processed in increasing order of distance (BFS-like behavior).

  2. **Expanding the Submap with BFS**
     - The function iterates through the queue, processing each position level by level.
     - Positions are added to the submap only if they haven't been visited before (`if pos not in nodes_main_to_sub`), preventing duplicate processing.
     - Each new position is assigned a unique index (`pos_i`) and mapped between the main map and submap.

  3. **Adaptive Radius Adjustment**
     - If the search reaches `min_radius` but the submap is still too small (`len(submap) < min_size`), the radius is increased dynamically.
     - This ensures that even in sparse areas, the submap has enough positions for meaningful conflict resolution.
     - The search stops at `max_radius` to prevent unnecessary computation in large open spaces.

  4. **Connecting the Submap to the Main Map**
     - After BFS completes, a second pass ensures all nodes in the submap correctly reference their neighbors from `main_map`.
     - This maintains connectivity between submap nodes and the broader environment, preventing pathfinding inconsistencies.

- `make_avoid(path: List[Tuple[int, int]], pos_time_pairs: List[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]`
  - **Description**: Creates avoidance constraints for agents not in the conflict.

- `find_avoids(all_agents: List[Agent]) -> List[List[Tuple[int, int]]]`
  - **Description**: This function determines positions and time steps that must be avoided by agents resolving a conflict, ensuring safe navigation without interfering with other agents' planned movements.

  1. **Filtering Non-Conflicting Agents**
     - Iterates through all agents, *excluding those already involved in the conflict*.
     - Only considers agents that have a valid path during the conflict period.

  2. **Extracting Relevant Time Windows**
     - If the agent's path **ends before the conflict**, it includes only the remaining portion of their path from `start_pos_time` onward.
     - Otherwise, it **trims the agent's path** to match the conflict window.
     - This ensures that only relevant agent movements are included in the avoid list.

  3. **Generating Avoidance Zones**
     - Calls `make_avoid(rel_path, pos_time_pairs)` to **convert agent paths into avoidable position-time pairs**.
     - This accounts for scenarios where agents may leave and re-enter the map, handling discontinuities in movement.
     - If avoid positions are found, they are appended to `avoids`.
  
- `print_subproblem(all_agents: List[Agent]) -> None`
  - **Description**: Prints a visualization of the subproblem at different timesteps. Useful for debugging and for possibly determining the cause of unsolveable conflicts. 

---

### Class `Optimal_Solver`
- **Description**: Represents an interface to an external optimal solver that finds the best paths for agents while respecting constraints and avoiding conflicts.

#### Attributes
- `agents: str` – String representation of agents with their start and destination points.
- `restrictions: List[List[Tuple[int, int]]]` – List of restricted positions and times to avoid.
- `nodes: List[int]` – List of nodes in the local subgraph.
- `neighbors: Dict[int, List[int]]` – Mapping of nodes to their respective neighbors.
- `makespan: int` – Maximum time allowed for agents to reach their destinations.
- `sum_of_costs: int` – Sum of individual agent path lengths.

#### Methods
- `__init__(agents: List[Tuple[int, int]], restrictions: List[List[Tuple[int, int]]], local_nodes: List[int], neighbors: Dict[int, List[int]], makespan: int = -1, sumCosts: int = -1) -> None`
  - **Description**: Initializes the solver with agent information, constraints, and map structure.

- `list_to_string(arr: List, array_of_agents: bool = False) -> str`
  - **Description**: Converts a list into a formatted string representation for Picat input. Used to convert agents list into a string representation.
  - **Returns**: A string representation of the input list.

- `call_solver() -> subprocess.CompletedProcess`
  - **Description**: Calls the external Picat solver to compute optimal agent paths.
  - **Returns**: A subprocess result containing solver output and execution details.

- `create_translation() -> None`
  - **Description**: This function generates a Picat input file (`opt_solver_1.pi`) that defines the problem for the solver. The input must include:
    - **Graph Representation**: Written from `get_neighbors_lines()`, defining valid movements.
    - **Agent List (`As`)**: Specifies all agents that need paths.
    - **Avoidance Constraints (`Avoid`)**: Generated from `get_avoid_lines()`, marking restricted position, time pairs.
    - **Optimization Metrics**: Includes `Makespan` (total time) and `SumOfCosts` (total path cost).


- `get_neighbors_lines() -> List[str]`
  - **Description**: Formats the neighborhood graph into Picat-compatible lines.
  - **Returns**: A list of strings representing the neighborhood structure.

- `get_avoid_lines() -> List[str]`
  - **Description**: Formats avoidance constraints for the solver.
  - **Returns**: A list of strings representing avoidance rules in Picat syntax.

---

### Module `utils.py`

- **Description**: This module provides utility functions for data manipulation and animation in the Multi-Agent Pathfinding (MAPF) solver.

#### Function `update_edge_dict`
- **Description**: Updates a dictionary tracking how frequently each edge is used in agent paths.
- **Parameters**:
  - `path: List[Tuple[int, int]]` – A list of coordinates representing the agent's path.
  - `diction: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]` – Dictionary mapping edges to their usage count.
- **Returns**:
  - `Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]` – The updated dictionary with incremented edge usage counts.

#### Function `animate_paths`
- **Description**: Utilizes `matplotlib.pyplot` and `matplotlib.animation` to animate agent paths before and after conflict resolution. Please note that this function was written with the help of ChatGPT.
- **Parameters**:
  - `initial_agents: List[Agent]` – The initial agent paths before conflict resolution.
  - `final_agents: List[Agent]` – The resolved agent paths after conflict resolution.
  - `max_length: int` – The maximum length of any agent's path.
  - `map_size: Tuple[int, int]` – The dimensions of the grid-based map.
  - `map_data: List[List[str]]` – The grid-based map data.
- **Returns**:
  - `None` – Saves the animation as a `.gif` file and displays it interactively.

---

### Main Entry Point `combined_solver`

- **Description**: This module serves as the main entry point for running the Multi-Agent Pathfinding (MAPF) solver. It initializes the environment, processes command-line arguments, computes initial paths, detects conflicts, and iteratively resolves them using an optimal solver.

#### Functions:

##### `main() -> None`
- **Description**: The primary function that orchestrates the MAPF solving process.
- **Steps:**
  1. **Parse Command-Line Arguments**  
     - Uses `argparse.ArgumentParser` to define and parse input arguments:
       - `--scen-file (-s)`: Specifies the `.scen` file containing the scenario data.
       - `--number-agents (-n)`: Defines how many agents to read and process (default: 30).
       - `--percentage-agents (-p)`: Defines the percentage of agents to read and process (default: 100(%)).
       - `--modified-search (-m)`: Enables modified A* search (default: `True`).
       - `--timeout (-t)`: Sets a timeout for conflict resolution (default: 200 seconds).
       - `--concise (-c)`: Enables concise output mode (default: `False`).
     - Logs the received arguments.

  2. **Load Map and Agents**  
     - Determines the scenario file name (defaults to `"maze-32-32-4-even-2.scen"` if not specified).
     - Reads map and agent data from the scenario file.
     - Logs that the map and agents have been loaded.

  3. **Compute Initial Agent Paths Using A* or Modified A***  
     - Initializes `max_length` (maximum path length) for conflict detection.
     - Uses either:
       - **Modified A*** (if `--modified-search` is enabled), tracking edge usage.
       - **Standard A*** otherwise.
     - Iterates over agents and calculates their paths.
     - Updates `max_length` accordingly.

  4. **Identify and Reorder Conflicts**  
     - Identifies conflicts from the initially computed paths.
     - Reorders conflicts to improve resolution efficiency.
     - Logs the number of initial conflicts.
     - Prints conflict information.

  5. **Iteratively Resolve Conflicts Using Subproblems**  
     - Tracks execution time to enforce the timeout constraint.
     - Maintains:
       - `unsolveable_conflicts`: Stores conflicts that remain unresolved after multiple attempts.
       - `flagged_conflicts`: Tracks conflicts that failed multiple resolution attempts.
     - Resolves conflicts iteratively while:
       - There are remaining conflicts.
       - The execution time is within the timeout limit.

     **Conflict Resolution Process:**
     - Retrieves and analyzes conflicts, checking if they have been flagged multiple times.
     - If flagged more than 30 times, marks them as unsolvable.
     - If previously solved, increases the subproblem size.
     - Creates a subproblem instance around the conflict.
     - Uses an optimal solver to attempt resolution:
       - If unsuccessful, increases the allowed time and retries.
       - If successful, updates agent paths and re-evaluates conflicts.
       - If unsuccessful after two attempts, reflags the conflict.

  6. **Handle Timeout and Final Conflict Reporting**  
     - If the timeout is reached, logs and prints a timeout message.
     - Logs the number of remaining conflicts.
     - Displays unresolved conflicts.

  7. **Visualize Final Paths**  
     - Animates the movement of agents before and after conflict resolution.

---
