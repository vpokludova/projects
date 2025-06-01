import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def update_edge_dict(path, diction):
    for i in range(len(path) - 1):
        edge = (path[i], path[i+1])
        if edge in diction:
            diction[edge] += 1
        else:
            diction[edge] = 1
    return diction 

def animate_paths(initial_agents, final_agents, max_length, map_size, map_data):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Colors for agents
    colors = plt.cm.get_cmap('tab20')(np.linspace(0, 1, max(len(initial_agents), len(final_agents))))
    
    def get_intermediate_position(pos1, pos2):
        return ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)
    
    def update(frame):
        for ax, agents, title in [(ax1, initial_agents, 'Initial Agent Paths'), 
                          (ax2, final_agents, 'Conflict-Resolved Paths')]:
            ax.clear()
            ax.set_xlim(0, map_size[0])
            ax.set_ylim(0, map_size[1])
            ax.set_title(f'{title}\nTime step: {frame/2:.1f}', fontsize=12, fontweight='bold')

            # Draw obstacles
            for y in range(map_size[1]):
                for x in range(map_size[0]):
                    if map_data[y][x] == '@':
                        ax.add_patch(plt.Rectangle((x-0.5, y-0.5), 1, 1, color='black'))
            
            vertex_conflicts = {}
            edge_conflicts = {}
            
            for i, agent in enumerate(agents):
                if int(frame/2) < len(agent.path):
                    current_pos = agent.path[int(frame/2)]
                    
                    if frame % 2 == 0:  # Full step
                        x, y = current_pos
                        if (x, y) in vertex_conflicts:
                            vertex_conflicts[(x, y)].append(agent.index)
                        else:
                            vertex_conflicts[(x, y)] = [agent.index]
                        ax.plot(x, y, 'o', markersize=10, color=colors[i], alpha=0.7)
                        ax.text(x, y, f'A{agent.index}', ha='center', va='center', fontweight='bold')
                    else:  # Half step
                        if int(frame/2) + 1 < len(agent.path):
                            next_pos = agent.path[int(frame/2) + 1]
                            x, y = get_intermediate_position(current_pos, next_pos)
                            edge = (current_pos, next_pos)
                            if edge in edge_conflicts:
                                edge_conflicts[edge].append(agent.index)
                            else:
                                edge_conflicts[edge] = [agent.index]
                            ax.plot(x, y, 'o', markersize=10, color=colors[i], alpha=0.7)
                            ax.text(x, y, f'A{agent.index}', ha='center', va='center', fontweight='bold')
            
            # Highlight vertex conflicts
            for (x, y), conflicting_agents in vertex_conflicts.items():
                if len(conflicting_agents) > 1:
                    ax.add_patch(plt.Circle((x, y), 0.5, color='red', fill=False, linewidth=2))
                    ax.text(x, y+0.7, f"Vertex Conflict: {', '.join(map(str, conflicting_agents))}", 
                            ha='center', va='bottom', color='red', fontweight='bold')
            
            # Highlight edge conflicts
            for (pos1, pos2), conflicting_agents in edge_conflicts.items():
                if len(conflicting_agents) > 1:
                    mid_x, mid_y = get_intermediate_position(pos1, pos2)
                    ax.add_patch(plt.Rectangle((mid_x-0.4, mid_y-0.4), 0.8, 0.8, color='orange', fill=False, linewidth=2))
                    ax.text(mid_x, mid_y+0.7, f"Edge Conflict: {', '.join(map(str, conflicting_agents))}", 
                            ha='center', va='bottom', color='orange', fontweight='bold')
        
        return ax1, ax2
    
    # Create the animation with twice as many frames to include half-steps
    anim = animation.FuncAnimation(fig, update, frames=max_length*2, interval=400, blit=False, repeat=False)
    
    # Save the animation as a gif or show it interactively
    anim.save('path_animation.gif', writer='pillow', dpi=100)
    plt.show()  # Show the animation interactively