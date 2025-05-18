import numpy as np
from scipy.integrate import solve_ivp

def lotka_volterra_system(t, y, params):
    """
    Basic Lotka-Volterra predator-prey equations.
    
    Args:
        t: Time point
        y: Current populations [prey, predator]
        params: Dictionary containing model parameters
            - alpha: prey growth rate
            - beta: prey death rate due to predation
            - gamma: predator death rate
            - delta: predator growth rate from predation
    
    Returns:
        List of derivatives [dPrey/dt, dPredator/dt]
    """
    prey, predator = y
    alpha = params['alpha']
    beta = params['beta']
    gamma = params['gamma']
    delta = params['delta']
    
    dPrey_dt = alpha * prey - beta * prey * predator
    dPredator_dt = delta * prey * predator - gamma * predator
    
    return [dPrey_dt, dPredator_dt]

def run_lotka_volterra(prey_growth_rate, prey_death_rate, predator_death_rate, 
                      predator_growth_rate, initial_prey, initial_predator, time_span):
    """
    Run a basic Lotka-Volterra simulation.
    
    Args:
        prey_growth_rate (float): Prey reproduction rate (alpha)
        prey_death_rate (float): Prey death rate due to predation (beta)
        predator_death_rate (float): Predator death rate (gamma)
        predator_growth_rate (float): Predator growth rate from predation (delta)
        initial_prey (float): Initial prey population
        initial_predator (float): Initial predator population
        time_span (int): Duration of simulation
        
    Returns:
        tuple: (times, results) where times is an array of time points and
              results is an array of population values for prey and predator
    """
    # Set up parameters
    params = {
        'alpha': prey_growth_rate,
        'beta': prey_death_rate,
        'gamma': predator_death_rate,
        'delta': predator_growth_rate
    }
    
    # Initial conditions
    y0 = [initial_prey, initial_predator]
    
    # Time points
    t_span = (0, time_span)
    t_eval = np.linspace(0, time_span, 1000)
    
    # Solve the ODE system
    solution = solve_ivp(
        lambda t, y: lotka_volterra_system(t, y, params),
        t_span,
        y0,
        method='RK45',
        t_eval=t_eval
    )
    
    return solution.t, solution.y.T

def apply_environmental_change(base_params, env_type, intensity, affected_species):
    """
    Modify parameters based on environmental change.
    
    Args:
        base_params (dict): Original model parameters
        env_type (str): Type of environmental change
        intensity (float): Intensity of change (0-100%)
        affected_species (str): Which species is affected ('prey', 'predator', or 'both')
        
    Returns:
        dict: Modified parameters
    """
    # Make a copy of the original parameters
    params = base_params.copy()
    
    # Scale factor based on intensity (0-100%)
    scale = intensity / 100.0
    
    if env_type == "Temperature Increase":
        if affected_species in ["prey", "both"]:
            # Higher temperatures can increase metabolic rates but also stress
            params['alpha'] = base_params['alpha'] * (1 - scale * 0.3)  # Reduced reproduction
            params['beta'] = base_params['beta'] * (1 + scale * 0.2)    # Increased vulnerability
            
        if affected_species in ["predator", "both"]:
            params['gamma'] = base_params['gamma'] * (1 + scale * 0.4)  # Increased death rate
            params['delta'] = base_params['delta'] * (1 - scale * 0.1)  # Less efficient hunting
            
    elif env_type == "Habitat Loss":
        if affected_species in ["prey", "both"]:
            params['alpha'] = base_params['alpha'] * (1 - scale * 0.5)  # Less resources for reproduction
            params['beta'] = base_params['beta'] * (1 + scale * 0.3)    # Easier to catch (less hiding places)
            
        if affected_species in ["predator", "both"]:
            params['gamma'] = base_params['gamma'] * (1 + scale * 0.2)  # Increased competition
            # Hunting efficiency might go up initially as prey has fewer hiding places
            if scale < 0.5:
                params['delta'] = base_params['delta'] * (1 + scale * 0.2)
            else:
                params['delta'] = base_params['delta'] * (1 - (scale-0.5) * 0.4)  # But eventually decline
            
    elif env_type == "Resource Depletion":
        if affected_species in ["prey", "both"]:
            params['alpha'] = base_params['alpha'] * (1 - scale * 0.7)  # Substantially reduced reproduction
            
        if affected_species in ["predator", "both"]:
            # Secondary effect on predators as prey becomes scarcer
            params['delta'] = base_params['delta'] * (1 - scale * 0.3)  # Less energy from prey
            
    elif env_type == "Disease":
        if affected_species == "prey":
            params['alpha'] = base_params['alpha'] * (1 - scale * 0.4)  # Reduced reproduction
            # Add a direct mortality factor to prey
            params['direct_mortality'] = base_params.get('direct_mortality', 0) + scale * 0.05
            
        elif affected_species == "predator":
            params['gamma'] = base_params['gamma'] * (1 + scale * 0.6)  # Increased death rate
            
        elif affected_species == "both":
            params['alpha'] = base_params['alpha'] * (1 - scale * 0.3)
            params['gamma'] = base_params['gamma'] * (1 + scale * 0.4)
            params['direct_mortality'] = base_params.get('direct_mortality', 0) + scale * 0.03
    
    return params

def lotka_volterra_with_env_change(t, y, base_params, env_changes):
    """
    Extended Lotka-Volterra system with environmental changes.
    
    Args:
        t: Time point
        y: Current populations [prey, predator]
        base_params: Dictionary with baseline parameters
        env_changes: List of environmental change events
        
    Returns:
        List of derivatives [dPrey/dt, dPredator/dt]
    """
    prey, predator = y
    
    # Start with baseline parameters
    current_params = base_params.copy()
    
    # Apply all active environmental changes
    for change in env_changes:
        if t >= change['start_time']:
            # Calculate how far into the change we are (for gradual changes)
            if 'duration' in change and change['duration'] > 0:
                progress = min(1.0, (t - change['start_time']) / change['duration'])
                effective_intensity = change['intensity'] * progress
            else:
                effective_intensity = change['intensity']
                
            # Apply the change to parameters
            current_params = apply_environmental_change(
                current_params, 
                change['type'], 
                effective_intensity, 
                change['affected_species']
            )
    
    # Standard Lotka-Volterra equations
    alpha = current_params['alpha']
    beta = current_params['beta']
    gamma = current_params['gamma']
    delta = current_params['delta']
    
    dPrey_dt = alpha * prey - beta * prey * predator
    dPredator_dt = delta * prey * predator - gamma * predator
    
    # Add any direct mortality from disease or other factors
    if 'direct_mortality' in current_params:
        dPrey_dt -= current_params['direct_mortality'] * prey
        dPredator_dt -= current_params['direct_mortality'] * predator
        
    return [dPrey_dt, dPredator_dt]

def run_habitat_change_simulation(prey_growth_rate, prey_death_rate, predator_death_rate, 
                                 predator_growth_rate, initial_prey, initial_predator, 
                                 time_span, env_change_type, env_change_start, env_change_intensity):
    """
    Run a Lotka-Volterra simulation with environmental changes.
    
    Args:
        prey_growth_rate (float): Prey reproduction rate (alpha)
        prey_death_rate (float): Prey death rate due to predation (beta)
        predator_death_rate (float): Predator death rate (gamma)
        predator_growth_rate (float): Predator growth rate from predation (delta)
        initial_prey (float): Initial prey population
        initial_predator (float): Initial predator population
        time_span (int): Duration of simulation
        env_change_type (str): Type of environmental change
        env_change_start (int): When the change begins
        env_change_intensity (float): Severity of change (0-100%)
        
    Returns:
        tuple: (times, results, events) - times, population results, and significant events
    """
    # Set up baseline parameters
    base_params = {
        'alpha': prey_growth_rate,
        'beta': prey_death_rate,
        'gamma': predator_death_rate,
        'delta': predator_growth_rate
    }
    
    # Define environmental change
    affected_species = "both"  # Default to affecting both
    
    # Customize which species are affected based on the change type
    if env_change_type == "Disease":
        # Randomly choose which species is affected
        import random
        affected_options = ["prey", "predator", "both"]
        affected_species = random.choice(affected_options)
    
    env_changes = [{
        'type': env_change_type,
        'start_time': env_change_start,
        'intensity': env_change_intensity,
        'affected_species': affected_species,
        'duration': 10  # Gradual change over 10 time units
    }]
    
    # Initial conditions
    y0 = [initial_prey, initial_predator]
    
    # Time points
    t_span = (0, time_span)
    t_eval = np.linspace(0, time_span, 1000)
    
    # Solve the ODE system
    solution = solve_ivp(
        lambda t, y: lotka_volterra_with_env_change(t, y, base_params, env_changes),
        t_span,
        y0,
        method='RK45',
        t_eval=t_eval
    )
    
    # Create events list for plotting
    events = [{
        'time': env_change_start,
        'description': f"{env_change_type} begins",
        'type': env_change_type,
        'intensity': env_change_intensity,
        'affected': affected_species
    }]
    
    return solution.t, solution.y.T, events
