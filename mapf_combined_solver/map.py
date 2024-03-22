from agents import Agent

class map:
    def __init__(self, scen_file, n_of_agents = -1):
        self.agents, self.map_file = read_agents(scen_file, n_of_agents)
        self.nodes = self.read_map()

    def read_map(self):
        fileReader = open("./maps/" + self.map_file, "r")

        # read first lines of file which describe the map
        line = fileReader.readline() # type of map 
        line = fileReader.readline() # height 
        tokens = line.split(" ")     # line looks like "height X" where X is an integer
        height = int(tokens[1])
        line = fileReader.readline() # width
        tokens = line.split(" ")
        width = int(tokens[1])
        fileReader.readline() # line just says "map"

        # read actual map into a 2D array
        line = 1
        nodes = []    
        while line <= height:
            s = fileReader.readline()
            row = list(s)
            row.pop()     # remove '\n' which is the last element of the list
            if len(row) != width:
                print("Map defined incorecctly.") # TODO: maybe change this comment or do throw an error??
            nodes.append(row)
            line += 1

        fileReader.close()
        return nodes

def read_agents(filename, n_of_agents=-1):
    fileReader = open("./scens/" + filename, "r")

    if n_of_agents != -1:   # if number of agents to process was specified
        max_agents = True
    else:                   # number of agents not specified; read all
        max_agents = False

    # read agent information from file
    keep_reading = True
    agents = []
    line = fileReader.readline()    # first line of file is of type "version X" TODO: check if this is always true
    i = 0                           # keeps track of number of agents read
    line = fileReader.readline()    # read first agent
    
    read_map_file = True

    while keep_reading and n_of_agents != 0:
        tokens = line.split("\t")
        if len(tokens) >= 7:
            if read_map_file:
                map_filename = tokens[1]
                read_map_file = False
            agent = Agent((int(tokens[4]),int(tokens[5])), (int(tokens[6]), int(tokens[7])), i)
            agents.append(agent)
            i += 1
        else:
            print("Information for agent " + str(i) + " is not sufficient.")
        
        line = fileReader.readline()
        if len(line) > 0:
            if max_agents:
                keep_reading = len(agents) < n_of_agents
        else:
            keep_reading = False
            
    return agents, map_filename