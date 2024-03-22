import optimal_solver
import informed_search
from conflicts import ConflictType
import heapq

class Subproblem:
    # all_agents is a list of all of the agents in the main problem
    def __init__(self, conflict, all_agents, main_map, size_inc = 0, map_size=10, sugg_min_radius = 2):
        self.conflict = conflict
        self.extra_time = len(conflict.agents)   
        self.radius = -1   

        if conflict.type == ConflictType.PATH:
            self.start_time = self.conflict.time - 2 
            if self.start_time < 0:
                self.start_time = 0
                print("Multiple agents have the same origin")
            self.end_time = conflict.time + (2 * len(conflict.path)) + (2 * len(conflict.agents))
            self.map, self.nodes_main_to_sub, self.nodes_sub_to_main = self.make_submap3(main_map, all_agents, size_inc)
            self.agents = []
            self.agent_index_main_to_sub = {}
            self.agent_index_sub_to_main = {}
            i = 1
            for ag in self.conflict.agents:
                agent = all_agents[ag]
                self.agent_index_main_to_sub[agent.index] = i 
                self.agent_index_sub_to_main[i] = agent.index
                ag_origin = agent.path[int(self.start_time / 2)]
                origin = self.nodes_main_to_sub[ag_origin]
                end_time_index = int(self.start_time / 2) + len(self.conflict.path) + 1
                if end_time_index < len(agent.path):
                    ag_dest = agent.path[end_time_index]
                else:
                    ag_dest = agent.path[-1]
                dest = self.nodes_main_to_sub[ag_dest]
                self.agents.append((origin, dest))
                i += 1

        else:
            max_radius = int(self.conflict.time / 2)
            if max_radius > 1:
                min_radius = sugg_min_radius
            else:
                min_radius = 1
            self.map, self.nodes_main_to_sub, self.nodes_sub_to_main, radius = self.make_submap5(main_map, all_agents, min_radius, map_size, max_radius)
            self.radius = radius
            if self.conflict.type == ConflictType.POSITION:
                self.start_time = self.conflict.time - (2 * radius)
                self.end_time = self.conflict.time + (2 * radius)
            else:   # edge conflict
                self.start_time = self.conflict.time - 1 - (2 * radius)
                self.end_time = self.conflict.time + 1 + (2 * radius)
            self.agents = []
            self.agent_index_main_to_sub = {}
            self.agent_index_sub_to_main = {}
            agent_i = 1
            for a in self.conflict.agents:
                ag = all_agents[a]
                origin = ag.path[int(self.start_time / 2)]
                if int(self.end_time / 2) >= len(ag.path):
                    dest = ag.path[-1]
                else:
                    dest = ag.path[int(self.end_time / 2)]
                origin = self.nodes_main_to_sub[origin]
                dest = self.nodes_main_to_sub[dest]
                self.agents.append((origin, dest))
                self.agent_index_main_to_sub[a] = agent_i
                self.agent_index_sub_to_main[agent_i] = a
                agent_i += 1
        self.avoids = self.find_avoids(all_agents)    # list of (position, time) pairs which other agents occupy (need all times that exist starting with start_time)

    def solve(self):
        # create optimal solver instance
        ms = int((self.end_time - self.start_time) / 2)
        os = optimal_solver.Optimal_Solver(self.agents, self.avoids, list(self.nodes_sub_to_main.keys()), self.map, makespan = ms) 
        result = os.call_solver()
        output = result.stdout.decode()
        return output, result.returncode
    
    def inc_ms_upd_avoids(self, all_agents, extra_time = 0):
        self.end_time += 2 * len(self.agents) + 2 * len(self.avoids) + extra_time
        self.avoids = self.find_avoids(all_agents)
        return

    def update_min_max(self, min_x, min_y, max_x, max_y, x, y):
        if x < min_x or min_x == -1:
            min_x = x 
        if x > max_x or max_x == -1:
            max_x = x 
        if y < min_y or min_y == -1:
            min_y = y 
        if y > max_y or max_y == -1:
            max_y = y 
        return min_x, min_y, max_x, max_y

    def get_neighbor_directions(self, x, y, min_x, min_y, max_x, max_y):
        dirs = [[0,0]]
        if y == min_y:
            dirs.append([0,1])
        elif y == max_y:
            dirs.append([0,-1])
        else:
            dirs.append([0,1])
            dirs.append([0,-1])
        if x == min_x:
            dirs.append([1,0])
        elif x == max_x:
            dirs.append([-1,0])
        else:
            dirs.append([1,0])
            dirs.append([-1,0])
        return dirs

    def add_pos_and_neighbors(self, pos, i, nodes_main_to_sub, nodes_sub_to_main, submap, neighbors):
        pos_index = i
        if pos not in nodes_main_to_sub.keys():
            nodes_main_to_sub[pos] = pos_index 
            nodes_sub_to_main[pos_index] = pos 
            submap[pos_index] = [pos_index] 
            i += 1
        else:
            pos_index = nodes_main_to_sub[pos]

        for n in neighbors:
            n_index = i 
            if n not in nodes_main_to_sub.keys():
                nodes_main_to_sub[n] = n_index
                nodes_sub_to_main[n_index] = n 
                submap[n_index] = [n_index]
                i += 1 
            else:
                n_index = nodes_main_to_sub[n]
            # add n to pos's neighbors 
            if n_index not in submap[pos_index]:
                submap[pos_index].append(n_index)
            # add pos to n's neigbors
            if pos_index not in submap[n_index]:
                submap[n_index].append(pos_index)
        return i, nodes_main_to_sub, nodes_sub_to_main, submap

    def rank_neighbors(self, next_pos, all_neighbors, conflict_path):
        distances = {}
        x2 = next_pos[0]
        y2 = next_pos[1]
        for n in all_neighbors:
            x1 = n[0]
            y1 = n[1]
            d = abs(x2 - x1) + abs(y2 - y1)
            if d in distances.keys():
                distances[d].append(n)
            else:
                distances[d] = [n]
        sorted_distances = sorted(distances.keys())
        ranked_neighbors = []
        while len(ranked_neighbors) < 2 and len(distances) > 0:
            d = sorted_distances[0]
            n = distances[d].pop(0)
            if n not in conflict_path:
                ranked_neighbors.append(n)
            if len(distances[d]) == 0:
                distances.pop(d)
                sorted_distances.remove(d)
        return ranked_neighbors
    
    # an attempt to make a smaller submap than in method make_submap2
    def make_submap3(self, main_map, all_agents, increase_size):
        submap = {}
        nodes_main_to_sub = {}
        nodes_sub_to_main = {}
        i = 1   # starting index of nodes
        # need to start at time -1 and end end at end time + 2
        start_time = int(self.start_time / 2)
        for a in self.conflict.agents:
            agent = all_agents[a]
            p = agent.path[start_time]
            neighbors_ranked = self.rank_neighbors(self.conflict.path[0], informed_search.get_neighbors(main_map, p), self.conflict.path)
            i, nodes_main_to_sub, nodes_sub_to_main, submap = self.add_pos_and_neighbors(p, i, nodes_main_to_sub, nodes_sub_to_main, submap, neighbors_ranked)

        for j in range(len(self.conflict.path) - 1):
            p = self.conflict.path[j]
            p2 = self.conflict.path[j + 1]
            neighbors_ranked = self.rank_neighbors(p2, informed_search.get_neighbors(main_map, p), self.conflict.path)
            i, nodes_main_to_sub, nodes_sub_to_main, submap = self.add_pos_and_neighbors(p, i, nodes_main_to_sub, nodes_sub_to_main, submap, neighbors_ranked)
      
        time = start_time + len(self.conflict.path) # last time step in conflict path
        loop_end = time + 3
        if increase_size != 0:
            loop_end += increase_size
        while time < loop_end:   # only want to add (last position of conflict) and the position after conflict (aka first nonconflicting position)
            for a in self.conflict.agents:
                if time < len(all_agents[a].path):
                    p = all_agents[a].path[time]
                    if time + 1 < len(all_agents[a].path):
                        p2 = all_agents[a].path[time + 1]
                    else:
                        p2 = p
                    neighbors_ranked = self.rank_neighbors(p2, informed_search.get_neighbors(main_map, p), self.conflict.path)
                    i, nodes_main_to_sub, nodes_sub_to_main, submap = self.add_pos_and_neighbors(p, i, nodes_main_to_sub, nodes_sub_to_main, submap, neighbors_ranked)

            time += 1

        for n in submap.keys():
            node = nodes_sub_to_main[n]
            possible_neighbors = informed_search.get_neighbors(main_map, node)
            for pn in possible_neighbors:
                if pn in nodes_main_to_sub.keys():
                    pn_sub = nodes_main_to_sub[pn]
                    if pn_sub not in submap[n]:
                        submap[n].append(pn_sub)

        return submap, nodes_main_to_sub, nodes_sub_to_main
        
    def make_submap5(self, main_map, all_agents, min_radius = 2, min_size = 7, max_radius = 200):
        queue = []
        submap = {}
        nodes_main_to_sub = {}
        nodes_sub_to_main = {}
        if self.conflict.type == ConflictType.EDGE:
            heapq.heappush(queue, (0, self.conflict.edge.first()))
            heapq.heappush(queue, (0, self.conflict.edge.second()))
        else:
            heapq.heappush(queue, (0, self.conflict.position))
        
        i = 1
        # want to do bfs from position or edge positions and go out to the minimum radius or minimum number of positions
        while len(queue) > 0:
            level, pos = heapq.heappop(queue)
            if pos not in nodes_main_to_sub:
                # don't re-explore already visited nodes
                pos_i = i 
                i += 1
                submap[pos_i] = [pos_i]
                nodes_main_to_sub[pos] = pos_i 
                nodes_sub_to_main[pos_i] = pos
                if level == min_radius and len(submap) < min_size:
                    min_radius += 1   
                if level < min_radius and level < max_radius:
                    for n in informed_search.get_neighbors(main_map, pos):
                        if n not in nodes_main_to_sub and (level + 1, n) not in queue:
                            heapq.heappush(queue, (level + 1, n))
            if len(queue) == 0:
                max_level = level

        # update neighbor lists
        for n in submap.keys():
            node = nodes_sub_to_main[n]
            possible_neighbors = informed_search.get_neighbors(main_map, node)
            for pn in possible_neighbors:
                if pn in nodes_main_to_sub.keys():
                    pn_sub = nodes_main_to_sub[pn]
                    if pn_sub not in submap[n]:
                        submap[n].append(pn_sub)

        return submap, nodes_main_to_sub, nodes_sub_to_main, max_level   

    def path_in_map(self, path):
        pairs = []
        start = -1
        end = -1
        for pos in path:
            if pos in self.nodes_main_to_sub.keys():
                if start == -1: # found start of a path in the map
                    start = path.index(pos)
            else:
                if start != -1:
                    end = path.index(pos) - 1
                    pairs.append([start, end])
                    start = -1
                    end = -1
        if end == -1 and start != -1:
            end = len(path) - 1
            pairs.append([start, end])
        return pairs

    def make_avoid(self, path, pos_time_pairs):
        result = []
        start = 0
    
        for pos in path:
            if pos in self.nodes_main_to_sub.keys():
                pair = (self.nodes_main_to_sub[pos], path.index(pos, start) + 1)
                start = path.index(pos, start) + 1
                if pair not in pos_time_pairs:
                    result.append(pair)
                    pos_time_pairs.append(pair)
        return result, pos_time_pairs
    
    def find_avoids(self, all_agents):
        pos_time_pairs = []     # a list of position time pairs that are already in the list avoids
        avoids = [] 
        end_pos_time = int(self.end_time / 2)
        start_pos_time = int(self.start_time / 2)
        for i in range(len(all_agents)):
            ag = all_agents[i]
            if not i in self.agent_index_main_to_sub.keys() and start_pos_time < len(ag.path):        # only want agents not present in the conflict
                    if len(ag.path) < end_pos_time:                 # agent ends before end of conflict
                        rel_path = ag.path[start_pos_time:]         
                    else:                                           # conflict ends before agent ends
                        rel_path = ag.path[start_pos_time: (end_pos_time + 1)]
                    # path in map has to change to return a list of tuples (start in map, end in map)
                    # because the agent can have multiple paths in the map but also leaves the map 
                    # in betweeen those sections
                    result, pos_time_pairs = self.make_avoid(rel_path, pos_time_pairs)
                    if len(result) > 0:
                        avoids.append(result)
        return avoids
    
    def avoid_on_dest(self):
        last_timestep = int((self.end_time - self.start_time) / 2) + 1
        destinations = [dest for (_,dest) in self.agents]
        for key in self.avoids:
            for pos,time in key:
                if time == last_timestep and pos in destinations:
                    return True
                
        return False

    def print_subproblem(self, all_agents):
        print("hello")
        for t in range(self.start_time, self.end_time, 2):
            timestep = int((t - self.start_time)/2)
            print("Time: " + str(t))
            min_y = min({y for _, y in self.nodes_main_to_sub.keys()})
            max_y = max({y for _, y in self.nodes_main_to_sub.keys()})
            min_x = min({x for x, _ in self.nodes_main_to_sub.keys()})
            max_x = max({x for x, _ in self.nodes_main_to_sub.keys()})

            # conflict's postition at time t, if exists
            if self.conflict.path != None:
                if t >= self.conflict.time:
                    if self.conflict.path != None and t < self.conflict.time + (2 * len(self.conflict.path)):
                        conflict_pos_t = self.conflict.path[int((t - self.conflict.time)/2)]
                    else:
                        conflict_pos_t = (-1, -1)
                else:
                    conflict_pos_t = (-1, -1)
                conflict_pos_t2 = (-1,-1)
            elif self.conflict.path == None and self.conflict.position == None:
                conflict_pos_t = (-1,-1)
                conflict_pos_t2 = (-1,-1)
                if t - 1 == self.conflict.time or t + 1 == self.conflict.time:
                    conflict_pos_t = self.conflict.edge.first()
                    conflict_pos_t2 = self.conflict.edge.second()
            else:
                conflict_pos_t = (-1,-1)
                conflict_pos_t2 = (-1, -1)
                if t == self.conflict.time:
                    conflict_pos_t = self.conflict.position

            # avoids at time t
            avoids_timestep = []
            for avoid_ag in self.avoids:
                for (pos, time) in avoid_ag:
                    if time - 1 == timestep:
                        avoids_timestep.append(self.nodes_sub_to_main[pos])

            # agents outside conflict at time t
            agents_at_t = {}
            lower_bound = 0
            upper_bound = 0
            if self.conflict.path != None:
                lower_bound = self.conflict.time
                upper_bound = self.conflict.time + (2 * len(self.conflict.path))
            elif self.conflict.path == None and self.conflict.position == None:
                lower_bound = self.conflict.time - 1
                upper_bound = self.conflict.time + 1
            if t < lower_bound or t > upper_bound:
                for ag in self.conflict.agents:
                    agents_at_t[all_agents[ag].path[int(t/2)]] = ag

            for y in range(min_y, max_y + 1):
                line = str(y) + ": "
                for x in range(min_x, max_x + 1):
                    if (x,y) in self.nodes_main_to_sub.keys():
                        con = 0
                        avoids = 0
                        agent_there = 0
                        agent_true = 0
                        if (x,y) == conflict_pos_t or (x,y) == conflict_pos_t2:
                            con += 1
                        if (x,y) in avoids_timestep:
                            avoids += 1
                        if (x,y) in agents_at_t.keys() and con == 0:
                            agent_there += agents_at_t[(x,y)]
                            agent_true = 1
                        total = con + avoids + agent_true 
                        if total > 1:
                            line += "K"
                        elif total > 0:
                            if con > 0:
                                line += "C"
                            elif avoids > 0:
                                line += "A"
                            elif agent_there > 0:
                                line += str(self.agent_index_main_to_sub[agent_there])
                        else:
                            line += "."

                    else :    # position not in submap
                        line += "X"
                print(line)