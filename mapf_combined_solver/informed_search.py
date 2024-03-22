import heapq

class Vertex:
    """ Additional data for every vertex visited by A* """
    def __init__(self, coord, distance, heuristic, predecessor, ranked = False, ranked_score = 0):
        self.coord = coord          # tuple (x,y)
        self.distance = distance    # distance from origin
        self.heuristic = heuristic  # estimated distance to goal
        self.predecessor = predecessor # predecessor to this vertex in path from origin to goal
        self.explored = False           # whether A* has processed this node already
        self.ranked = ranked
        self.ranked_score = ranked_score
        self.val = self.distance + self.heuristic + self.ranked_score
            
    def __eq__(self, other):
        if self.ranked:
            return self.val == other.val
        else:
            return self.distance == other.distance
        
    def __ne__(self, other):
        if self.ranked:
            return self.val != other.val
        else:
            return self.distance != other.distance

    def __lt__(self, other):
        if self.ranked:
            return self.val < other.val
        else:
            return self.distance < other.distance
        
    def __gt__(self, other):
        if self.ranked:
            return self.val > other.val
        else:
            return self.distance > other.distance   
    
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)


def get_path(origin, destination):
    path = []
    vertex = destination 
    path.append(vertex.coord)   # start from the goal node 
    while vertex.predecessor:   # work backwards until we get to origin, which has no predecessor
        assert vertex.distance == vertex.predecessor.distance + 1 # make sure there is only one step between nodes
        path.append(vertex.predecessor.coord)
        vertex = vertex.predecessor
    assert vertex == origin 
    path1 = list(reversed(path)) 
    return path1

def valid_node(nodes, node):
    if node[0] >= 0 and node[0] < len(nodes[0]): # x is within bounds
        if node[1] >= 0 and node[1] < len(nodes): # y is within bounds
            if nodes[node[1]][node[0]] != "@": # check for presence of obstacle
                return True
    return False

def get_neighbors(nodes, node):
    nextNodes = []
    possibleDirections = [[0,1], [1,0], [0,-1], [-1,0]] # all possible moves agent can make
    for d in possibleDirections:
        dx = d[0]
        dy = d[1]
        n = (node[0]+dx, node[1]+dy) # new coordinate value after move
        if valid_node(nodes, n): # check validity of new coordinate
            nextNodes.append(n)
    return nextNodes

# calculates Manhattan distance between origin and destination
def heuristic(origin, destination):     
    return abs(destination[0] - origin[0]) + abs(destination[1] - origin[1])

# A* on the map nodes from origin_coord to destination_corrd, returns path
def informed_search(nodes, origin_coord, destination_coord):
    h = heuristic(origin_coord, destination_coord)  # estimate of distance from origin to destination
    origin = Vertex(origin_coord, 0, h, None)       
    visited =  { origin_coord : origin }            # a dictionary that gives corresponding Vertex object for visited coordinates
    queue = []
    heapq.heappush(queue, (origin.distance+origin.heuristic, origin)) # vertices in queue are ordered by estimated distance to destination

    while len(queue) > 0:
        _,explore = heapq.heappop(queue)
        assert not explore.predecessor or explore.distance == explore.predecessor.distance + 1 

        #terminate when the destination is reached
        if explore.coord == destination_coord:
            return get_path(origin, explore)

        # explore all neighbours if this vertex hasn't been explored yet
        elif not explore.explored:
            explore.explored = True
            distance = explore.distance + 1

            # visit all neighbours
            for visit_coord in get_neighbors(nodes, explore.coord):
                if not visit_coord in visited:
                    h = heuristic(visit_coord, destination_coord)
                    visit = Vertex(visit_coord, distance, h, explore)
                    visited[visit_coord] = visit
                    heapq.heappush(queue, (visit.distance + visit.heuristic, visit))
                else:
                    visit = visited[visit_coord]
                    if visit.distance > distance:
                        assert not visit.explored
                        # priority in queue should be decreased,
                        # but finding the vertex in queue or updating its position not efficient
                        visit.distance = distance
                        visit.predecessor = explore
                        heapq.heappush(queue, (visit.distance+visit.heuristic, visit))
    return [] # no path was found

def modified_informed_search(nodes, origin_coord, destination_coord, used_edges_dict):
    h = heuristic(origin_coord, destination_coord)
    origin = Vertex(origin_coord, 0, h, None, ranked=True)
    visited = { origin_coord : origin }
    queue = []
    heapq.heappush(queue, origin)

    while len(queue) > 0:
        explore = heapq.heappop(queue)
        assert not explore.predecessor or explore.distance == explore.predecessor.distance + 1

        #terminate when the destination is reached
        if explore.coord == destination_coord:
            return get_path(origin, explore)
    
        # explore all neighbours if this vertex hasn't been explored yet
        elif not explore.explored:
            explore.explored = True
            distance = explore.distance + 1

            # visit all neighbors but rank while taking into account already used edges from this position
            neighbors_unranked = get_neighbors(nodes, explore.coord)
            ranked = rank_neighbors(explore.coord, neighbors_unranked, used_edges_dict, destination_coord, explore.distance)
            for visit_coord in neighbors_unranked:
                if visit_coord not in visited:
                    h = heuristic(visit_coord, destination_coord)
                    visit = Vertex(visit_coord, distance, h, explore, True, ranked[visit_coord])
                    visited[visit_coord] = visit 
                    heapq.heappush(queue, visit)
                else: 
                    visit = visited[visit_coord]
                    if visit.distance > distance and not visit.explored:
                        visit.distance = distance 
                        visit.predecessor = explore 
                        visit.ranked = True 
                        visit.ranked_score = ranked[visit_coord]
                        heapq.heappush(queue, visit)
    return []

def rank_neighbors(coord, neighbors_unranked, diction, dest, time):
    # first rank by heuristic
    neighb_heur = {}    # maps heuristic values to list of neighbors
    for n in neighbors_unranked:
        h = heuristic(n, dest)
        if h not in neighb_heur:
            neighb_heur[h] = [n]
        else:
            neighb_heur[h].append(n)

    ranked = {} # assigns each neighbor a score - the lower the better
    i = 0
    sorted_keys = sorted(neighb_heur.keys())
    for h in sorted_keys:
        for n in neighb_heur[h]:
            ranked[n] = i 
        i += 1

    # rank using dictionary which shows which edges have been used already
    neighb_uses = {}        # maps count of edge uses to list of neighbors
    for n in neighbors_unranked:
        edge = (coord, n)
        if edge in diction.keys():
            val = diction[edge]
        else:
            val = 0
        if val in neighb_uses.keys():
            neighb_uses[val].append(n)
        else:
            neighb_uses[val] = [n]
    
    i = 0
    sorted_keys = sorted(neighb_uses.keys())
    for v in sorted_keys:
        for n in neighb_uses[v]:
            ranked[n] += i 
        i += 1

    return ranked

    sorted_scores = set(sorted(ranked.values()))
    neighbors = []
    for s in sorted_scores:
        nodes = get_keys(ranked, s)
        for n in nodes:
            neighbors.append(n)

    return neighbors

def get_keys(diction, value):
    nodes = []
    for k in diction.keys():
        if diction[k] == value:
            nodes.append(k)
    return nodes
    


