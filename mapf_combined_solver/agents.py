class Agent:
    def __init__(self, origin, dest, index):
        self.origin = origin        # starting position in the form of a position (x,y)
        self.destination = dest     # goal position (x,y)
        self.index = index          # index of agent instance in array of agents for the current scenario
        self.path = []              # current calculated path for the agent

    def __repr__(self):
        return str(self.index)