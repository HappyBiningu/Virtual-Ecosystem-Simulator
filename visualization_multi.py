import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import networkx as nx
import matplotlib.cm as cm
from matplotlib.colors import to_rgba

def plot_multi_species(times, results, species_info):
    """
    Plot population trends for multiple interacting species.
    
    Args:
        times (array): Time points
        results (array): Population values for all species
        species_info (dict): Dictionary with species metadata
        
    Returns:
        matplotlib.figure.Figure: Plot object
    """
    num_species = results.shape[1]
    species_names = species_info.get('names', [f"Species {i+1}" for i in range(num_species)])
    
    # Use a simple color palette for each species
    color_palette = plt.cm.get_cmap('tab10', num_species)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot each species
    for i in range(num_species):
        ax.plot(times, results[:, i], label=species_names[i], 
                color=colors[i], linewidth=2)
    
    # Add labels and legend
    ax.set_xlabel('Time')
    ax.set_ylabel('Population')
    ax.set_title(f'Multi-Species Population Dynamics: {species_info.get("ecosystem_type", "Ecosystem")}')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    return fig

def plot_food_web(species_info):
    """
    Create a network visualization of a multi-species food web.
    
    Args:
        species_info (dict): Dictionary with species interaction data
        
    Returns:
        matplotlib.figure.Figure: Network visualization
    """
    species_names = species_info['names']
    interaction_matrix = species_info['interaction_matrix']
    num_species = len(species_names)
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes
    for i, name in enumerate(species_names):
        G.add_node(name, index=i)
    
    # Add edges based on interactions
    for i in range(num_species):
        for j in range(num_species):
            if i != j and interaction_matrix[i][j] != 0:
                # Negative interaction means i is eaten by j
                if interaction_matrix[i][j] < 0:
                    G.add_edge(species_names[i], species_names[j], 
                              weight=abs(interaction_matrix[i][j]),
                              interaction_type="predation")
                # Positive interaction means cooperation or benefit
                elif interaction_matrix[i][j] > 0:
                    G.add_edge(species_names[i], species_names[j], 
                              weight=interaction_matrix[i][j],
                              interaction_type="benefit")
    
    # Create positions - try to arrange in a food chain/web hierarchy
    try:
        # Try to use hierarchical layout
        pos = nx.spring_layout(G, seed=42)
    except:
        # Fall back to circular layout
        pos = nx.circular_layout(G)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Draw nodes with different colors for different species types
    node_colors = []
    for node in G.nodes():
        if "plant" in node.lower() or "phyto" in node.lower():
            node_colors.append("green")
        elif "herb" in node.lower() or "zoo" in node.lower():
            node_colors.append("blue")
        elif "carn" in node.lower() or "pred" in node.lower() or "shark" in node.lower():
            node_colors.append("red")
        elif "omni" in node.lower():
            node_colors.append("purple")
        elif "decomp" in node.lower():
            node_colors.append("brown")
        else:
            node_colors.append("grey")
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.8)
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    
    # Draw edges with different styles for predation vs. benefit
    predation_edges = [(u, v) for u, v, d in G.edges(data=True) if d['interaction_type'] == "predation"]
    benefit_edges = [(u, v) for u, v, d in G.edges(data=True) if d['interaction_type'] == "benefit"]
    
    # Edge weights for thickness
    predation_weights = [3 * G[u][v]['weight'] for u, v in predation_edges]
    benefit_weights = [3 * G[u][v]['weight'] for u, v in benefit_edges]
    
    # Draw predation edges (what eats what)
    nx.draw_networkx_edges(G, pos, edgelist=predation_edges, width=predation_weights,
                          edge_color='red', arrows=True, connectionstyle='arc3,rad=0.1')
    
    # Draw benefit edges (who benefits from whom)
    nx.draw_networkx_edges(G, pos, edgelist=benefit_edges, width=benefit_weights,
                          edge_color='green', style='dashed', arrows=True, 
                          connectionstyle='arc3,rad=-0.1')
    
    # Add legend elements
    ax.plot([], [], 'red-', linewidth=2, label='Predation')
    ax.plot([], [], 'green--', linewidth=2, label='Benefit')
    ax.plot([], [], 'o', color='green', markersize=10, label='Producers')
    ax.plot([], [], 'o', color='blue', markersize=10, label='Herbivores')
    ax.plot([], [], 'o', color='red', markersize=10, label='Carnivores')
    ax.plot([], [], 'o', color='purple', markersize=10, label='Omnivores')
    ax.plot([], [], 'o', color='brown', markersize=10, label='Decomposers')
    
    # Add title and legend
    plt.title(f"Food Web: {species_info.get('ecosystem_type', 'Ecosystem')}")
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.axis('off')
    
    return fig