import argparse
import time
import logging

import informed_search
import map
import subproblem
from conflicts import update_agents_from_solution, identify_conflicts, reorder_conflicts, print_conflict_info
from utils import update_edge_dict

logging.basicConfig(filename='mapf_solver.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the MAPF solver program")

    # check arguments
    parser = argparse.ArgumentParser()  
    parser.add_argument("-s", "--scen-file", type = str)       # user can specify name of .scen file
    parser.add_argument("-n", "--number-agents", type = int, default=30)   # user can specify how many agents to read and process, -1 means read all
    parser.add_argument("-m", "--modified-search", action = 'store_true', default=True)   # indicates use of modified A* 
    parser.add_argument("-t", "--timeout", type = int, default=200) 
    parser.add_argument("-c", "--concise", action='store_true', default=False)
    args = parser.parse_args()                                  # read arguments from input
    
    logger.debug(f"Arguments received: {args}")
    
    # change value of var only if user specified it
    if args.scen_file:
        s_filename = args.scen_file
    else:
        s_filename = "maze-32-32-4-even-2.scen"         # default .scen file
        logger.info(f"No scenario file specified. Using default: {s_filename}")

    # read map and agent information from files
    main_map = map.map(s_filename, args.number_agents)
    logger.info("Map and agent information loaded.")

    max_length = 0      # used in finding conflicts

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

    # find conflicts from initially found paths
    conflicts = identify_conflicts(main_map.agents, max_length)
    conflicts = reorder_conflicts(conflicts)
    print_conflict_info(conflicts)
    logger.info(f"Initial conflicts identified: {len(conflicts)}")

    # track time for timeout
    start_time = time.time()
    current_time = time.time()

    # keep a dictionary of solved conflicts to prevent cyclic solving of conflicts
    solved_conflicts = {}

    unsolveable_conflicts = []  
    flagged_conflicts = {}      # conflicts that have been unsolveable mulitple times - they get extra extra time
    while len(conflicts) > 0 and current_time - start_time < args.timeout:
        conflict = conflicts.pop(0)

        unsolveable = False
        if conflict in flagged_conflicts:
            retry_count = flagged_conflicts[conflict]   
            logging.info(f"Retrying conflict {conflict} for the {retry_count} time")

            if retry_count > 3:     # giving up on the conflict 
                unsolveable_conflicts.append(conflict)
                unsolveable = True  
                logging.info(f"Marking conflict {conflict} as unsolvable after {retry_count} attempts")

        # check if conflict has been solved before if yes increase submap size to prevent repetition
        tup = None
        tup2 = None
        solve_count = 0
        if conflict.position is not None:
            tup = (conflict.position, (-1,-1))
        elif conflict.edge is not None:
            tup = conflict.edge
        if tup is not None:
            tup2 = (tup, tuple(conflict.agents))
        if tup2 in solved_conflicts.keys():
            # increase radius of graph in proportion to solve_count
            logging.info(f"The conflict {conflict} has been solved before at an earlier time")
            solve_count = solved_conflicts[tup2]
            subproblem1 = subproblem.Subproblem(conflict, main_map.agents, main_map.nodes, sugg_min_radius=3 * solve_count)
        else:
            subproblem1 = subproblem.Subproblem(conflict, main_map.agents, main_map.nodes)
            logging.info(f"Created subproblem instance for conflict {conflict}")

        # print unsolveable conflict to output if applicable
        if unsolveable:
            if not args.concise:
                subproblem1.print_subproblem(main_map.agents)
            continue

        if conflict in flagged_conflicts:
            # increase size of area around conflict endpoints in the submap by retry_count
            subproblem1 = subproblem.Subproblem(conflict, main_map.agents, main_map.nodes, retry_count)
            # increase makespan in a way that's proportional to retry_count
            subproblem1.inc_ms_upd_avoids(main_map.agents, 2 * retry_count)

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
            if tup is not None:
                tup2 = (tup, tuple(conflict.agents))
                if tup2 not in solved_conflicts.keys():
                    solved_conflicts[tup2] = 1
                else:
                    solved_conflicts[tup2] += 1
            main_map.agents, max_length = update_agents_from_solution(subproblem1, output, main_map.agents, max_length) # update agent paths based on optimal solver's solution
            conflicts1 = identify_conflicts(main_map.agents, max_length)        
            conflicts = []
            for c in conflicts1:
                if c not in unsolveable_conflicts:
                    conflicts.append(c)
            conflicts = reorder_conflicts(conflicts)
            print_conflict_info(conflicts)
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

    logger.info(f"Conflicts after at the end: {len(conflicts)}")
    logger.info(f"Unsolveable conflicts at the end: {len(unsolveable_conflicts)}")

    print("Current conflicts:")
    print_conflict_info(conflicts)
    print("Unsolveable conflict information:")
    print_conflict_info(unsolveable_conflicts)


if __name__ == "__main__":
    main()