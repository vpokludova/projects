import matplotlib.pyplot as plt
import numpy as np

def update_edge_dict(path, diction):
    for i in range(len(path) - 1):
        edge = (path[i], path[i+1])
        if edge in diction:
            diction[edge] += 1
        else:
            diction[edge] = 1
    return diction 

def print_conflicting_paths(conflict, agents, map, subprob = None):
    if conflict.path != None:
        min_length = min(len(agents[index].path) for index in conflict.agents)
        for i in range(min_length):
            print("Step " + str(i))

            if i >= int(conflict.time / 2):
                if conflict.path != None and i < int(conflict.time / 2) + len(conflict.path):
                    conflict_pos_i = conflict.path[i - int(conflict.time / 2)]
                elif conflict.position != None:
                    conflict_pos_i = conflict.position
                else:
                    conflict_pos_i = (-1,-1)
            else: 
                conflict_pos_i = (-1,-1) 

            for y in range(0,32):
                line = ""
                for x in range(0,32):
                    ag_on_pos = agent_on_position(conflict.agents, (x,y), agents, i)
                    if conflict_pos_i == (x,y):
                        line += "C"
                    elif ag_on_pos != -1:
                        line += "*"
                    else:
                        line += map[y][x]
                print(line)
    
def agent_on_position(conflict_agents, pos, agents, t):
    for ag in conflict_agents:
        if agents[ag].path[t] == pos:
            return ag
    return -1

def parse_data(file_path):
    scenarios = {}
    current_scenario = None
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('maze'):
                current_scenario = line.strip()
                scenarios[current_scenario] = {
                    "Total conflicts": [],
                    "Edge conflicts": [],
                    "Position conflicts": [],
                    "Path conflicts": [],
                }
            elif 'conflicts:' in line:
                tokens = line.strip().split(': ')
                if len(tokens) == 2:
                    metric = tokens[0]
                    value = tokens[1]
                scenarios[current_scenario][metric].append(int(value))
    
    return scenarios

def plot_scenario_progression(scenarios):
    for scenario, data in scenarios.items():
        plt.figure(figsize=(14, 6))
        plt.title(f'Conflict Progression: {scenario}')
        for conflict_type in ["Total conflicts", "Edge conflicts", "Position conflicts", "Path conflicts"]:
            plt.plot(data[conflict_type], label=conflict_type)
        
        plt.xlabel('Time Step')
        plt.ylabel('Number of Conflicts')
        plt.legend()
        plt.grid(True)
        plt.show()

def combined_analysis(scenarios):
    total_decrease_rates = []
    final_conflict_reductions = []
    
    for data in scenarios.values():
        total_conflicts = data["Total conflicts"]
        if len(total_conflicts) > 1:
            initial, final = total_conflicts[0], total_conflicts[-1]
            decrease_rate = (initial - final) / len(total_conflicts)
            total_decrease_rates.append(decrease_rate)
            final_conflict_reductions.append(initial - final)
    
    average_decrease_rate = np.mean(total_decrease_rates)
    average_final_conflict_reduction = np.mean(final_conflict_reductions)
    
    print(f'Average Rate of Conflict Decrease Across Scenarios: {average_decrease_rate:.2f}')
    print(f'Average Final Conflict Reduction Across Scenarios: {average_final_conflict_reduction:.2f}')

def analyze_results(file_path):
    scenarios = parse_data(file_path)

    # Plot progression for each scenario
    plot_scenario_progression(scenarios)

    # Perform combined analysis
    combined_analysis(scenarios)