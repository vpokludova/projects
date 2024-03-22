class Edge:
    def __init__(self, p1, p2):
        if p1 < p2:
            self.edge = (p1, p2)
        else:
            self.edge = (p2, p1)
    
    def first(self):
        return self.edge[0]

    def second(self):
        return self.edge[1]
    
    def __eq__(self, other):
        return self.edge == other.edge 

    def __hash__(self):
        return hash(self.edge)
    
    def __repr__(self):
        return str(self.edge)