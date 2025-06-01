import subprocess

class Optimal_Solver:
    def __init__(self, agents, restrictions, local_nodes, neighbors, makespan = -1, sumCosts = -1):
        self.agents = self.list_to_string(agents, True)                # list of agents in the form (origin, destination)
        self.restrictions = restrictions    # list of restrictions/ paths to avoid, is a list of pairs (position, time)
        self.nodes = local_nodes            # list of nodes
        self.neighbors = neighbors          # dictionary with key node, value list of neighbors
        self.makespan = makespan
        self.sum_of_costs = sumCosts
        self.create_translation()

    def list_to_string(self, arr, array_of_agents = False):
        result = "["
        for el in arr:
            if array_of_agents:
                origin = el[0]
                dest = el[1]
                result += "(" + str(origin) + "," + str(dest) + ")"
            else:
                result += str(el)
            if arr.index(el) != (len(arr) - 1):
                result += ","
            else:
                result += "]"
        return result

    def call_solver(self):
        result = subprocess.run(['picat', './source/picat/mks', './source/picat/opt_solver_1.pi'], shell=True, capture_output= True)
        return result

    def create_translation(self):
        file = open('./source/picat/opt_solver_1.pi', "w")   
        file.write("ins(Graph, As, Avoid, Makespan, SumOfCosts) =>\n")      # header
        file.write("    Graph = [\n")                                         # start of graph
        file.writelines(self.get_neighbors_lines())
        file.write("    ],\n")         # end of graph                           
        file.write("    As = " + self.agents + ",\n")                    # agents
        file.writelines(self.get_avoid_lines())
        file.write("    Makespan = " + str(self.makespan) + ",\n")               # makespan
        file.write("    SumOfCosts = " + str(self.sum_of_costs) + ".")           # sum of costs
        file.close()                                                         
        return file

    def get_neighbors_lines(self):
        result = []
        for node in self.nodes:
            if len(self.neighbors[node]) > 0:
                neighbors_str = self.list_to_string(self.neighbors[node])
                s = ("    $neibs(" + str(node) + "," + neighbors_str + ")")
                if self.nodes.index(node) != len(self.nodes) - 1:
                    s += ","
                s += "\n"
                result.append(s)
        return result
    
    def get_avoid_lines(self):
        result = []
        if len(self.restrictions) == 0:
            result = ["    Avoid = new_array(0,0),\n"]
        else:
            max_len = self.makespan
            num_agents = len(self.restrictions)
            result = ["    Avoid = new_array(" + str(max_len) + "," + str(num_agents) + "),\n"]
            i = 1
            for path in self.restrictions:
                positions = {}
                for t in range(1, max_len + 1):
                    positions[t] = 0
                for pair in path:
                    pos = pair[0]
                    time = pair[1]
                    positions[time] = pos
                for t in range(1, max_len + 1):
                    pos = positions[t]
                    result.append("    Avoid[" + str(t) + "," + str(i) + "] = " + str(pos) + ",\n")
                i += 1  # index of agent in avoids array


        return result
        
    