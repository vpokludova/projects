This is a manual for solving MAPF problems using Picat. A picat binary is needed (http://picat-lang.org/download.html).

usage: ./picat [model name] [instance path]

example: ./picat mks example_instance.pi

The format of the instance is as follows:

ins(Graph, As, Avoid, Makespan, SumOfCosts) =>		% a header
    Graph = [										% description of the underlying graph
    $neibs(1,[1,3]),								% graph is in the format of list of neighbors for each vertex (vertices are indexed form 1)
    $neibs(2,[2,3]),
    $neibs(3,[3,4,1,2]),
    $neibs(4,[4,3,5,6]),
    $neibs(5,[5,4]),
    $neibs(6,[6,4])
    ],
    As = [(1,5)],									% a list of agents in the form (start,goal)
    Avoid = new_array(6,1),							% if the agents need to avoid some other agent, here is the path to be avoided (path length, number of agents to avoid)
    Avoid[1,1] = 6,									% at timestep 1, agent 1 is present at location 6
    Avoid[2,1] = 4,
    Avoid[3,1] = 3,
    Avoid[4,1] = 2,
    Avoid[5,1] = 2,
    Avoid[6,1] = 2,
    Makespan = 6,									% restriction on makespan
    SumOfCosts = 5.									% restriction on sum of costs

    												% if no restrictions are present, the following is used instead
    Avoid = new_array(0,0),
    Makespan = -1,
    SumOfCosts = -1.

An example of output format:

agents | timesteps
2 5 												% number_of_agents number_of_timesteps
36 55 36 37 38										% Each line is a list of visited vertices. One line per agent.
37 36 35 35 34