from enum import Enum 
import hashlib
from edges import Edge

class ConflictType(Enum):
    EDGE = 0
    POSITION = 1
    PATH = 2

class Conflict:
    def __init__(self, type, time, agents = [], position = None, edge = None, path = None):
        self.type = type    # ConflictType
        self.time = time
        self.agents = agents
        self.position = position
        self.edge = edge
        self.path = path

    def __eq__(self, other):
        if not isinstance(other, Conflict):
            return False
        return (self.type == other.type and
                self.time == other.time and
                self.agents == other.agents and
                self.position == other.position and
                self.edge == other.edge and
                self.path == other.path)
    
    def __hash__(self):
        # Create a tuple of relevant attributes and convert it to a string
        attributes = (self.type, self.time, tuple(self.agents), self.position, self.edge, self.path)
        attributes_string = ",".join(map(str, attributes))
        
        # Use hashlib to create a hash from the string
        return int(hashlib.sha256(attributes_string.encode()).hexdigest(), 16)
    
    def __repr__(self):
        if self.type == ConflictType.EDGE:
            return "{" + " edge " + str(self.time) + " " + str(self.agents) + " " + str(self.edge) + " " + "}"
        elif self.type == ConflictType.POSITION:
            return "{" + " position " + str(self.time) + " " + str(self.agents) + " " + str(self.position) + " " + "}"
        else:
            return "{" + " path " + str(self.time) + " " + str(self.agents) + " " + str(self.path) + " " + "}"
    
def identify_conflicts(agents, max_length, start = 0): 
    conflicts = [] 
    # iterate over every possible edge and position one at a time and identify edge and position conflicts
    # position conflict is when mulitple agents occupy the same position at a given time 
    # edge conflict is when multiple agents use the same edge at the same time
    for i in range(start, max_length * 2 - 1):
        # position conflict
        if i % 2 == 0:  
            pos_cons = get_conflict_pairs(agents, i)
            for pos in pos_cons.keys():
                if len(pos_cons[pos]) > 1: 
                    conflicts.append(Conflict(ConflictType.POSITION, time = i, agents = pos_cons[pos], position=pos))
        # edge conflict
        else:                              
            edge_cons = get_conflict_pairs(agents, i, False)
            for ed in edge_cons.keys():
                if len(edge_cons[ed]) > 1:
                    conflicts.append(Conflict(ConflictType.EDGE, time = i, agents = edge_cons[ed], edge = ed))
    # identify path conflicts
    conflicts = update_conflicts(conflicts, agents)
    return conflicts

def update_conflicts(conflicts, agents):
    # get all edge conflicts and replicate as path conflicts - add to stack of "unfinished" path conflicts
    stack = []
    edge_paths = []     # list of path conflicts which are created from existing path conflicts
    pos_conflicts = {}  # dictionary of (x,y,time) keys which are position conflicts where value is the actual conflict
    edge_conflicts = {} # dictionary of (x1, y1, x2, y2, time) 
    i = 0
    confirmed_conflicts = []
    while i < len(conflicts):
        con = conflicts[i]
        if con.type == ConflictType.EDGE:
            p1 = con.edge.first()
            p2 = con.edge.second()
            group1, group2 = split_agents(con, agents)
            if len(group1) > 1:
                edge_paths.append(Conflict(ConflictType.PATH, time = con.time - 1, agents = group1, path = [p1,p2]))
            if len(group2) > 1:
                edge_paths.append(Conflict(ConflictType.PATH, time = con.time - 1, agents = group2, path = [p2,p1]))
            if len(group1) > 0 and len(group2) > 0:
                # actual edge conflict (agents are moving in opposite directions)
                confirmed_conflicts.append(con) 
        else:
            pos_conflicts[(con.position[0], con.position[1], con.time)] = con
        i += 1
    
    conflicts = confirmed_conflicts
    used_edges = [] # a set of used edges where elements are of the type (p1,p2,time,[agents]) 
    while len(edge_paths) > 0 or len(stack) > 0:
        while len(stack) > 0:   # give priority to adding finishing paths that are in the process of being "built"
            con = stack.pop()   # take from back/top
            if len(con.path) >= 2:
                p1 = con.path[-2]
                p2 = con.path[-1]
                time = con.time + (2 * (len(con.path) - 1)) - 1
                key = (p1, p2, time, con.agents)
                if key in used_edges:
                    continue
                else:
                    used_edges.append(key)
            last_pos = con.path[-1]
            pos_time = con.time + (2 * (len(con.path) - 1))
            indexes = [] # indexes of edge conflicts in edge_paths that start with pos at time pos_time and its agents are a subset of con.agents
            updated_edge_paths = []
            for ec in edge_paths:
                if ec.path[0] == last_pos and ec.time == pos_time:
                    indexes.append(edge_paths.index(ec))
                    updated_edge_paths.append(ec)
                else:
                    updated_edge_paths.append(ec)
            extended = False
            only_some_continuing = False
            if len(indexes) > 0:
                i = 0
                while i < len(indexes) and not extended:
                    ind = indexes[i]
                    ec = edge_paths[ind]
                    intersection = []           # agents in both ec and con
                    con_remainder = []          # agents in con but not in ec
                    ec_remainder = []           # agents in ec but not in con
                    for ag in con.agents:   
                        if ag in ec.agents:
                            intersection.append(ag)
                        else:
                            con_remainder.append(ag)
                    for ag in ec.agents:
                        if ag not in intersection:
                            ec_remainder.append(ag)
                            
                    if len(intersection) > 1:   # can extend path, add this extended path with agents from intersection to stack
                        appended_path = con.path.copy()
                        appended_path.append(ec.path[1])
                        stack.append(Conflict(ConflictType.PATH, time = con.time, agents = intersection, path = appended_path))
                        key = (ec.path[0], ec.path[1], ec.time, intersection)
                        used_edges.append(key)
                        extended = True

                    if len(ec_remainder) == 0:  # whole edge path used
                        updated_edge_paths.remove(ec)
                    i += 1
                
                edge_paths = updated_edge_paths

            if len(indexes) == 0 or (len(indexes) > 0 and not extended) or only_some_continuing:
                if len(con.path) > 2 and len(con.agents) > 1:       # finished path conflict
                    conflicts.append(con)
                elif len(con.path) == 2 and len(con.agents) > 1:    # relevant edge conflict
                    edge = Edge(con.path[0], con.path[1])
                    p1 = edge.first()
                    p2 = edge.second()
                    key = (p1[0], p1[1], p2[0], p2[1], con.time)
                    if key in edge_conflicts.keys():
                        for ag in con.agents:
                            if ag not in edge_conflicts[key].agents:
                                edge_conflicts[key].agents.append(ag)
                    else:
                        edge_conflicts[key] = con

                for i in range(len(con.path)):          # remove unnecessary position conflicts
                    p = con.path[i]
                    p_time = con.time + (2 * i)
                    p_con = None                        # find corresponding position conflict
                    key = (p[0], p[1], p_time)
                    if key in pos_conflicts.keys():
                        p_con = pos_conflicts[key]
                    if p_con != None:
                        rem_agents = []                 # agents that aren't in the path conflict
                        for ag in p_con.agents:
                            if ag not in con.agents:
                                rem_agents.append(ag)
                        if len(rem_agents) > 1:
                            pos_conflicts[key].agents = rem_agents
                        else:
                            pos_conflicts.pop(key)
                
        # when no more path conflicts waiting to be "finished"/made add one from edge_paths
        if len(edge_paths) == 0:
            break
        next_pc = edge_paths.pop(0)
        stack.append(next_pc)

    # add remaining edge and position conflicts to conflicts
    for pc_key in pos_conflicts.keys():
        conflicts.append(pos_conflicts[pc_key])
    for ec_key in edge_conflicts.keys():
        con = edge_conflicts[ec_key]
        if con.path != None:
            if len(con.path) > 2:
                conflicts.append(con)
            else:
                if con.time % 2 == 0:
                    con.time += 1
                conflicts.append(Conflict(ConflictType.EDGE, con.time, con.agents, edge = Edge(con.path[0], con.path[1])))
      
    return conflicts

def get_conflict_pairs(agents, time, is_position=True):
    pairs = {}
    if is_position: # position conflict
        i = int(time / 2) 
    else: # doing edge conflict
        i = int((time + 1) / 2)
    for ag in agents:
        if len(ag.path) > i:
            if is_position:
                key = ag.path[i]
            else:
                key = Edge(ag.path[i-1], ag.path[i])

            if key in pairs:
                pairs[key].append(ag.index)
            else:
                pairs[key] = [ag.index]
    return pairs

def print_conflict_info(conflicts):
    print("Total conflicts: " + str(len(conflicts)))
    edge_cs = 0
    pos_cs = 0
    path_cs = 0
    for i in range(len(conflicts)):
        if conflicts[i].type == ConflictType.EDGE:
            edge_cs += 1
        elif conflicts[i].type == ConflictType.POSITION:
            pos_cs += 1
        else:
            path_cs += 1
    print("Edge conflicts: " + str(edge_cs))
    print("Position conflicts: " + str(pos_cs))
    print("Path conflicts: " + str(path_cs))
    print()
    return (pos_cs, edge_cs, path_cs)
    
def sorting_key(conflict):
    if conflict.type == ConflictType.PATH:
        time = conflict.time + 2 * len(conflict.path)
        return (time, 0)  # First priority: path conflicts sorted by time
    elif conflict.type == ConflictType.EDGE:
        return (conflict.time, 1)  # First priority: edge conflicts sorted by time
    elif conflict.type == ConflictType.POSITION:
        return (conflict.time, 2)  # Third priority: position conflicts sorted by time

def reorder_conflicts(conflicts):
    sorted_conflicts = sorted(conflicts, key=sorting_key)
    return sorted_conflicts

# using output from optimal solver update agent paths and also maximum path length
def update_agents_from_solution(subproblem, solver_output, all_agents, max_length):
    lines = solver_output.split("\r\n")
    lines = lines[9:]
    agent_index = 1
    if len(lines) < len(subproblem.agents):
        print("insufficient number of agent paths")
        return
    start_index = int(subproblem.start_time / 2)
    while agent_index <= len(subproblem.agents):
        agent_main_index = subproblem.agent_index_sub_to_main[agent_index]
        line = lines[agent_index - 1]
        path_orig = line.split()
        path = []
        for p in path_orig:
            path.append(subproblem.nodes_sub_to_main[int(p)])
        agent_index += 1
        all_agents[agent_main_index].path = insert_new_subpath(all_agents[agent_main_index].path, path, start_index)
        if len(all_agents[agent_main_index].path) > max_length:
            max_length = len(all_agents[agent_main_index].path)
    return all_agents, max_length

def insert_new_subpath(path, subpath, start_index):
    rem_start_index = path.index(subpath[-1], start_index) + 1
    path = path[:start_index] + subpath + path[rem_start_index:]
    return path

def split_agents(edge_conflict, agents):
    p1 = edge_conflict.edge.first()
    p2 = edge_conflict.edge.second()
    group1 = [] # agents going from p1 to p2
    group2 = [] # agents going from p2 to p1    
    for ag in edge_conflict.agents:
        pos = agents[ag].path[int((edge_conflict.time - 1)/2)]
        if pos == p1:
            group1.append(ag)
        else:
            group2.append(ag)
    return group1, group2

# Extend agent paths to the maximum length of all paths to keep them at destination positions
def agents_stay_at_destination(agents, max_length):
    def extend_list(lst, target_length):
        if not lst:
            raise ValueError("List cannot be empty")
        if len(lst) >= target_length:
            return lst[:target_length]
        
        return lst + [lst[-1]] * (target_length - len(lst))


    for agent in agents:
        agent.path = extend_list(agent.path, max_length)

    return agents