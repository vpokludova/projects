import argparse
import time
import logging
import copy
import pandas as pd

import informed_search
import map
import subproblem
from conflicts import update_agents_from_solution, identify_conflicts, reorder_conflicts, print_conflict_info, agents_stay_at_destination
from utils import update_edge_dict, animate_paths

logging.basicConfig(filename='mapf_solver.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the MAPF solver program")

    # check arguments
    parser = argparse.ArgumentParser()  
    parser.add_argument("-s", "--scen-file", type = str)       # user can specify name of .scen file
    parser.add_argument("-n", "--number-agents", type = int, default=30)   # user can specify how many agents to read and process, -1 means read all
    parser.add_argument("-p", "--percentage-agents", type=int, default=100) # user can specify the percentage of agents to read and process
    parser.add_argument("-m", "--modified-search", action = 'store_true', default=True)   # indicates use of modified A* 
    parser.add_argument("-t", "--timeout", type = int, default=200) 
    parser.add_argument("-c", "--concise", action='store_true', default=False)
    parser.add_argument("--animate-paths", action='store_true', default=False) 
    args = parser.parse_args()                                  # read arguments from input
    
    logger.debug(f"Arguments received: {args}")
    
    # change value of var only if user specified it
    if args.scen_file:
        s_filename = args.scen_file
    else:
        s_filename = "maze-32-32-4-even-2.scen"         # default .scen file
        logger.info(f"No scenario file specified. Using default: {s_filename}")

    # read map and agent information from files
    main_map = map.map(s_filename, args.number_agents, args.percentage_agents)
    logger.info("Map and agent information loaded.")

    max_length = 0      # used in finding conflicts

    # start time for measuring total length of A* calls
    start_time_init = time.time()

    if args.modified_search:
        # find path for each agent using modified A*
        logger.info("Using modified A* for pathfinding.")
        edge_use_dict = {}
        for agent in main_map.agents:
            search_path = informed_search.modified_informed_search(main_map.nodes, agent.origin, agent.destination, edge_use_dict)
            agent.path = search_path
            if len(agent.path) > max_length:
                max_length = len(agent.path)
            edge_use_dict= update_edge_dict(search_path, edge_use_dict)
    else:
        # find path for each agent using A*
        logger.info("Using standard A* for pathfinding.")
        for agent in main_map.agents:
            search_path = informed_search.informed_search(main_map.nodes, agent.origin, agent.destination) 
            agent.path = search_path  
            if len(agent.path) > max_length:
                max_length = len(agent.path)     

    finding_init_paths_time = time.time() - start_time_init
    logger.info(f"Non-optimal solver took {finding_init_paths_time} seconds to find initial paths for agents")

    # find conflicts from initially found paths
    main_map.agents = agents_stay_at_destination(main_map.agents, max_length)
    conflicts = identify_conflicts(main_map.agents, max_length)
    conflicts = reorder_conflicts(conflicts)
    pos_count, edge_count, path_count = print_conflict_info(conflicts)
    logger.info(f"Initial conflicts identified: {len(conflicts)}")
    logger.info(f"Initial number of position conflicts: {pos_count}")
    logger.info(f"Initial number of edge conflicts: {edge_count}")
    logger.info(f"Initial number of path conflicts: {path_count}")
    logger.info(f"Maximum agent path legnth after non-optimal solver: {max_length}")

    # track time for timeout
    start_time = time.time()
    current_time = time.time()

    # Make a deep copy of initial agents
    initial_agents = copy.deepcopy(main_map.agents)
    #animate_paths(main_map.agents, max_length, (len(main_map.nodes), len(main_map.nodes[0])), main_map.nodes)

    unsolveable_conflicts = []  
    flagged_conflicts = {}      # conflicts that have been unsolveable mulitple times - they get extra extra time
    conflict_counts_data = []   # initialize structure for storing conflict type distribution and counts
    unsolveable_outputs = []
    while len(conflicts) > 0 and current_time - start_time < args.timeout:
        conflict = conflicts.pop(0)

        if conflict in flagged_conflicts:
            unsolveable = False
            retry_count = flagged_conflicts[conflict]   
            logging.info(f"Retrying conflict {conflict} for the {retry_count} time")

            if retry_count > 30:     # giving up on the conflict 
                unsolveable_conflicts.append(conflict)
                unsolveable = True  
                logging.info(f"Marking conflict {conflict} as unsolvable after {retry_count} attempts")

            # increase size of area around conflict endpoints in the submap by retry_count
            # and increase suggested minimum radius relative to retry count but no more than 10
            sugg_radius = min(10, retry_count)
            subproblem1 = subproblem.Subproblem(conflict, main_map.agents, main_map.nodes, size_inc=retry_count, sugg_min_radius=sugg_radius)
            # increase makespan in a way that's proportional to retry_count
            subproblem1.inc_ms_upd_avoids(main_map.agents, 4 * retry_count)

            if unsolveable:
                if not args.concise:
                    unsolveable_outputs.append(subproblem1.print_subproblem(main_map.agents))
                    print("unsolveable")
                    
                continue

        else:
            subproblem1 = subproblem.Subproblem(conflict, main_map.agents, main_map.nodes) 

        logging.info(f"Created subproblem instance for conflict {conflict}")

        # call optimal solver on created subproblem
        output, exitcode = subproblem1.solve()
        if exitcode != 0:
            logging.info("Optimal solver was not successful the first time")
            # optimal solver failed to solve the subproblem
            subproblem1.inc_ms_upd_avoids(main_map.agents)  # increase available time
            output, exitcode = subproblem1.solve()          # try to solve again
        if exitcode == 0:
            logging.info("Optimal solver was successful")
            # optimal solver successfully solved the subproblem
            main_map.agents, max_length = update_agents_from_solution(subproblem1, output, main_map.agents, max_length) # update agent paths based on optimal solver's solution
            main_map.agents = agents_stay_at_destination(main_map.agents, max_length)
            conflicts1 = identify_conflicts(main_map.agents, max_length)        
            conflicts = []
            for c in conflicts1:
                if c not in unsolveable_conflicts:
                    conflicts.append(c)
            conflicts = reorder_conflicts(conflicts)
            pos, edge, path = print_conflict_info(conflicts)
            conflict_counts_data.append({'Position': pos, 'Edge': edge, 'Path': path, 'Total': pos+edge+path})
        else:
            logging.info("Optimal solver was not successful the second time")
            # optimal solver wasn't successful even after 2nd attempt
            if conflict in flagged_conflicts:
                flagged_conflicts[conflict] += 1
            else:
                flagged_conflicts[conflict] = 1
                conflicts.insert(0, conflict)

        current_time = time.time()

    if (current_time - start_time) > args.timeout:
        logging.info("Timeout occurred")
        print("Timeout occured")  

    logger.info(f"Fixing conflicts took {current_time - start_time} seconds")
    logger.info(f"Total combined solver runtime is {current_time - start_time_init} seconds")

    logger.info(f"Number of conflicts at termination: {len(conflicts)}")
    logger.info(f"Number of unsolveable conflicts at termination: {len(unsolveable_conflicts)}")

    logger.info(f"Maximum agent path legnth after optimal solver: {max_length}")


    print("Current conflicts:")
    pos_count, edge_count, path_count = print_conflict_info(conflicts)
    logger.info(f"Number of position conflicts post solver: {pos_count}")
    logger.info(f"Number of edge conflicts post solver: {edge_count}")
    logger.info(f"Number of path conflicts post solver: {path_count}")

    print("Unsolveable conflict information:")
    pos_count, edge_count, path_count = print_conflict_info(unsolveable_conflicts)
    logger.info(f"Number of 'unsolveable' position conflicts post solver: {pos_count}")
    logger.info(f"Number of 'unsolveable' edge conflicts post solver: {edge_count}")
    logger.info(f"Number of 'unsolveable' path conflicts post solver: {path_count}")

    # Animate final agent paths
    if args.animate_paths:
        animate_paths(initial_agents, main_map.agents, max_length, (len(main_map.nodes), len(main_map.nodes[0])), main_map.nodes)

    df = pd.DataFrame(conflict_counts_data)
    df.to_csv('conflict_counts_df.csv')

    with open("unsolveable.txt", 'w') as f:
        f.writelines(unsolveable_outputs)


if __name__ == "__main__":
    main()