import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def multi_species_system(t, y, params):
    """
    Extended ecosystem model with multiple interacting species.
    
    Args:
        t: Time point
        y: Array of current population values for each species
        params: Dictionary containing model parameters
            - growth_rates: List of intrinsic growth rates for each species
            - interaction_matrix: Matrix of interaction coefficients
    
    Returns:
        List of derivatives for each species population
    """
    num_species = len(y)
    derivatives = np.zeros(num_species)
    
    # Get parameters
    growth_rates = params['growth_rates']
    interaction_matrix = params['interaction_matrix']
    carrying_capacities = params.get('carrying_capacities', [float('inf')] * num_species)
    
    # Calculate derivative for each species
    for i in range(num_species):
        # Intrinsic growth term (includes carrying capacity)
        derivatives[i] = growth_rates[i] * y[i] * (1 - y[i] / carrying_capacities[i])
        
        # Interaction terms with other species
        for j in range(num_species):
            if i != j:  # Skip self-interaction 
                derivatives[i] += interaction_matrix[i][j] * y[i] * y[j]
    
    return derivatives

def run_multi_species_simulation(species_names, growth_rates, interaction_matrix, 
                                initial_populations, carrying_capacities=None, time_span=100):
    """
    Run a simulation with multiple interacting species.
    
    Args:
        species_names (list): Names of each species in the ecosystem
        growth_rates (list): Intrinsic growth rates for each species
        interaction_matrix (list): Matrix of interaction coefficients
        initial_populations (list): Initial population for each species
        carrying_capacities (list, optional): Maximum sustainable population for each species
        time_span (int): Duration of simulation
        
    Returns:
        tuple: (times, results) where times is an array of time points and
               results is an array of population values for all species
    """
    num_species = len(species_names)
    
    # Validate inputs
    if len(growth_rates) != num_species:
        raise ValueError("Growth rates list must match number of species")
    if len(interaction_matrix) != num_species or any(len(row) != num_species for row in interaction_matrix):
        raise ValueError("Interaction matrix must be square with dimensions matching number of species")
    if len(initial_populations) != num_species:
        raise ValueError("Initial populations list must match number of species")
    
    # Set default carrying capacities if not provided
    if carrying_capacities is None:
        carrying_capacities = [1000] * num_species
    elif len(carrying_capacities) != num_species:
        raise ValueError("Carrying capacities list must match number of species")
    
    # Setup parameters
    params = {
        'growth_rates': growth_rates,
        'interaction_matrix': interaction_matrix,
        'carrying_capacities': carrying_capacities
    }
    
    # Initial conditions
    y0 = initial_populations
    
    # Time points
    t_span = (0, time_span)
    t_eval = np.linspace(0, time_span, 1000)
    
    # Solve the ODE system
    solution = solve_ivp(
        lambda t, y: multi_species_system(t, y, params),
        t_span,
        y0,
        method='RK45',
        t_eval=t_eval
    )
    
    return solution.t, solution.y.T

def create_food_web_example(ecosystem_type="forest", num_species=3, time_span=100):
    """
    Create an example food web with interactions between multiple species.
    
    Args:
        ecosystem_type (str): Type of ecosystem (forest, marine, etc.)
        num_species (int): Number of species in the food web (3-5 recommended)
        time_span (int): Duration of simulation
        
    Returns:
        tuple: (times, results, species_info) containing simulation results and metadata
    """
    if num_species < 3:
        num_species = 3  # Minimum for interesting food web
    if num_species > 5:
        num_species = 5  # Maximum for clarity
    
    # Define species based on ecosystem type
    if ecosystem_type == "forest":
        species_names = ["Plants", "Herbivores", "Carnivores", "Omnivores", "Decomposers"][:num_species]
        
        # Default growth rates (positive for producers, negative for consumers)
        growth_rates = [0.5, -0.2, -0.3, -0.25, 0.1][:num_species]
        
        # Initial populations
        initial_populations = [500, 100, 30, 50, 200][:num_species]
        
        # Carrying capacities
        carrying_capacities = [1000, 300, 100, 150, 500][:num_species]
        
        # Create interaction matrix (positive: benefits, negative: harms)
        interaction_matrix = np.zeros((num_species, num_species))
        
        # Plants are eaten by herbivores and omnivores
        if num_species >= 2:
            interaction_matrix[0][1] = -0.01  # Plants eaten by herbivores
            interaction_matrix[1][0] = 0.02   # Herbivores benefit from plants
        
        if num_species >= 3:
            interaction_matrix[1][2] = -0.02  # Herbivores eaten by carnivores
            interaction_matrix[2][1] = 0.01   # Carnivores benefit from herbivores
        
        if num_species >= 4:
            interaction_matrix[0][3] = -0.005  # Plants eaten by omnivores
            interaction_matrix[3][0] = 0.01    # Omnivores benefit from plants
            interaction_matrix[1][3] = -0.01   # Herbivores compete with omnivores
            interaction_matrix[3][1] = -0.01   # Omnivores compete with herbivores
        
        if num_species >= 5:
            # Decomposers benefit from dead organisms
            interaction_matrix[4][0] = 0.005
            interaction_matrix[4][1] = 0.005
            interaction_matrix[4][2] = 0.005
            interaction_matrix[4][3] = 0.005
    
    elif ecosystem_type == "marine":
        species_names = ["Phytoplankton", "Zooplankton", "Small Fish", "Large Fish", "Sharks"][:num_species]
        
        # Default growth rates
        growth_rates = [0.8, -0.1, -0.2, -0.3, -0.4][:num_species]
        
        # Initial populations
        initial_populations = [800, 200, 100, 50, 20][:num_species]
        
        # Carrying capacities
        carrying_capacities = [2000, 500, 300, 150, 60][:num_species]
        
        # Create interaction matrix
        interaction_matrix = np.zeros((num_species, num_species))
        
        # Basic food chain
        if num_species >= 2:
            interaction_matrix[0][1] = -0.01  # Phytoplankton eaten by zooplankton
            interaction_matrix[1][0] = 0.02   # Zooplankton benefit from phytoplankton
        
        if num_species >= 3:
            interaction_matrix[1][2] = -0.02  # Zooplankton eaten by small fish
            interaction_matrix[2][1] = 0.01   # Small fish benefit from zooplankton
        
        if num_species >= 4:
            interaction_matrix[2][3] = -0.03  # Small fish eaten by large fish
            interaction_matrix[3][2] = 0.02   # Large fish benefit from small fish
        
        if num_species >= 5:
            interaction_matrix[3][4] = -0.04  # Large fish eaten by sharks
            interaction_matrix[4][3] = 0.02   # Sharks benefit from large fish
    
    else:  # Generic ecosystem
        species_names = [f"Species {i+1}" for i in range(num_species)]
        growth_rates = [0.5] + [-0.2] * (num_species - 1)
        initial_populations = [100 * (num_species - i) for i in range(num_species)]
        carrying_capacities = [200 * (num_species - i) for i in range(num_species)]
        
        # Simple food chain for generic ecosystem
        interaction_matrix = np.zeros((num_species, num_species))
        for i in range(num_species - 1):
            interaction_matrix[i][i+1] = -0.02  # Species i is eaten by species i+1
            interaction_matrix[i+1][i] = 0.01   # Species i+1 benefits from eating species i
    
    # Run the simulation
    times, results = run_multi_species_simulation(
        species_names,
        growth_rates,
        interaction_matrix,
        initial_populations,
        carrying_capacities,
        time_span
    )
    
    # Create species info for visualization
    species_info = {
        'names': species_names,
        'growth_rates': growth_rates,
        'interaction_matrix': interaction_matrix,
        'carrying_capacities': carrying_capacities,
        'ecosystem_type': ecosystem_type
    }
    
    return times, results, species_info