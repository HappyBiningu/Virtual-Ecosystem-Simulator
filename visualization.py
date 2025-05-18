import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import networkx as nx
from matplotlib.patches import ConnectionPatch
import matplotlib.cm as cm

def plot_population_trends(times, results, events=None, plot_type='matplotlib'):
    """
    Plot the population trends over time.
    
    Args:
        times (array): Time points
        results (array): Population values for prey and predator
        events (list): List of environmental change events
        plot_type (str): Type of plot ('matplotlib' or 'plotly')
        
    Returns:
        matplotlib.figure.Figure or plotly.graph_objects.Figure: Plot object
    """
    prey_pop = results[:, 0]
    predator_pop = results[:, 1]
    
    if plot_type == 'matplotlib':
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot populations
        ax.plot(times, prey_pop, 'b-', label='Prey')
        ax.plot(times, predator_pop, 'r-', label='Predator')
        
        # Add event markers if provided
        if events:
            for event in events:
                ax.axvline(x=event['time'], color='green', linestyle='--', alpha=0.6)
                ax.text(event['time'], max(np.max(prey_pop), np.max(predator_pop)) * 0.9, 
                        event['description'], rotation=90, verticalalignment='top')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Population')
        ax.set_title('Predator-Prey Population Dynamics')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    elif plot_type == 'plotly':
        fig = go.Figure()
        
        # Add population traces
        fig.add_trace(go.Scatter(
            x=times, y=prey_pop,
            name='Prey',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=times, y=predator_pop,
            name='Predator',
            line=dict(color='red', width=2)
        ))
        
        # Add event markers if provided
        if events:
            for event in events:
                fig.add_vline(
                    x=event['time'], 
                    line_dash="dash", 
                    line_color="green",
                    annotation_text=event['description'],
                    annotation_position="top right"
                )
        
        # Update layout
        fig.update_layout(
            title='Predator-Prey Population Dynamics',
            xaxis_title='Time',
            yaxis_title='Population',
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig

def plot_phase_space(results):
    """
    Plot the phase space diagram (predator vs prey).
    
    Args:
        results (array): Population values for prey and predator
        
    Returns:
        matplotlib.figure.Figure: Plot object
    """
    prey_pop = results[:, 0]
    predator_pop = results[:, 1]
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot the phase space trajectory
    ax.plot(prey_pop, predator_pop, 'g-', alpha=0.6)
    ax.plot(prey_pop[0], predator_pop[0], 'go', markersize=8, label='Start')
    ax.plot(prey_pop[-1], predator_pop[-1], 'ro', markersize=8, label='End')
    
    # Add direction arrows at regular intervals
    num_arrows = 10
    indices = np.linspace(0, len(prey_pop)-2, num_arrows, dtype=int)
    
    for i in indices:
        ax.annotate('', 
                   xy=(prey_pop[i+1], predator_pop[i+1]),
                   xytext=(prey_pop[i], predator_pop[i]),
                   arrowprops=dict(arrowstyle='->', color='blue', lw=1.5),
                   )
    
    ax.set_xlabel('Prey Population')
    ax.set_ylabel('Predator Population')
    ax.set_title('Phase Space Diagram')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

def plot_ecological_network(network_data):
    """
    Create a network visualization of the ecosystem.
    
    Args:
        network_data (dict): Data about the ecological relationships
        
    Returns:
        matplotlib.figure.Figure: Network visualization
    """
    # Create graph
    G = nx.DiGraph()
    
    # Add nodes
    prey_pop = network_data.get('prey_pop', 100)
    predator_pop = network_data.get('predator_pop', 50)
    
    # Scale node sizes
    max_pop = max(prey_pop, predator_pop)
    prey_size = 2000 * (prey_pop / max_pop)
    predator_size = 2000 * (predator_pop / max_pop)
    
    # Add nodes
    G.add_node("Sun", pos=(0, 3), node_type="resource")
    G.add_node("Vegetation", pos=(0, 2), node_type="resource")
    G.add_node("Prey", pos=(0, 1), node_type="species", population=prey_pop)
    G.add_node("Predator", pos=(0, 0), node_type="species", population=predator_pop)
    G.add_node("Decomposers", pos=(1, 1.5), node_type="resource")
    
    # Add edges with weights
    prey_growth = network_data.get('prey_growth_rate', 1.0)
    prey_death = network_data.get('prey_death_rate', 0.1)
    predator_growth = network_data.get('predator_growth_rate', 0.1)
    predator_death = network_data.get('predator_death_rate', 0.3)
    
    G.add_edge("Sun", "Vegetation", weight=5.0)
    G.add_edge("Vegetation", "Prey", weight=prey_growth * 10)
    G.add_edge("Prey", "Predator", weight=predator_growth * 10)
    G.add_edge("Predator", "Decomposers", weight=predator_death * 10)
    G.add_edge("Prey", "Decomposers", weight=prey_death * 5)
    G.add_edge("Decomposers", "Vegetation", weight=3.0)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Set positions
    pos = {
        "Sun": (-1, 4),
        "Vegetation": (0, 3),
        "Prey": (0, 1),
        "Predator": (0, -1),
        "Decomposers": (2, 1)
    }
    
    # Node colors and sizes
    node_color = {
        "Sun": "yellow",
        "Vegetation": "green",
        "Prey": "blue",
        "Predator": "red",
        "Decomposers": "brown"
    }
    
    node_size = {
        "Sun": 1500,
        "Vegetation": 1000,
        "Prey": prey_size,
        "Predator": predator_size,
        "Decomposers": 800
    }
    
    # Draw nodes
    for node in G.nodes():
        nx.draw_networkx_nodes(
            G, pos, 
            nodelist=[node],
            node_color=node_color[node],
            node_size=node_size[node],
            alpha=0.8,
            ax=ax
        )
    
    # Draw node labels
    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_family="sans-serif",
        ax=ax
    )
    
    # Draw edges with varying widths based on weight
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        width = weight / 2.0  # Scale the width
        nx.draw_networkx_edges(
            G, pos,
            edgelist=[(u, v)],
            width=width,
            alpha=0.7,
            edge_color="gray",
            arrows=True,
            arrowsize=20,
            connectionstyle='arc3,rad=0.1',
            ax=ax
        )
    
    # Add annotations
    ax.text(-1, 5, "Energy Flow Diagram", fontsize=18, fontweight='bold')
    ax.text(3, 4, "Legend:", fontsize=14)
    ax.text(3, 3.7, "● Energy Source", color="yellow", fontsize=12)
    ax.text(3, 3.4, "● Producer", color="green", fontsize=12)
    ax.text(3, 3.1, "● Herbivore", color="blue", fontsize=12)
    ax.text(3, 2.8, "● Carnivore", color="red", fontsize=12)
    ax.text(3, 2.5, "● Decomposer", color="brown", fontsize=12)
    
    # Add information about arrow thickness
    ax.text(3, 2.0, "Arrow thickness represents", fontsize=12)
    ax.text(3, 1.7, "strength of interaction", fontsize=12)
    
    # Remove axis
    ax.axis('off')
    
    return fig
