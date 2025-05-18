def get_preset_scenarios():
    """
    Get a dictionary of preset ecosystem scenarios.
    
    Returns:
        dict: Dictionary of preset scenarios
    """
    scenarios = {
        "Desert Ecosystem": {
            'prey_growth_rate': 0.6,
            'prey_death_rate': 0.2,
            'initial_prey': 70,
            'predator_death_rate': 0.4,
            'predator_growth_rate': 0.08,
            'initial_predator': 30,
            'time_span': 150,
            'enable_env_change': False,
            'env_change_type': "None",
            'env_change_start': 0,
            'env_change_intensity': 0,
            'description': "A desert ecosystem with limited resources. Features lower reproduction rates and higher mortality."
        },
        
        "Forest Ecosystem": {
            'prey_growth_rate': 1.2,
            'prey_death_rate': 0.15,
            'initial_prey': 120,
            'predator_death_rate': 0.3,
            'predator_growth_rate': 0.12,
            'initial_predator': 40,
            'time_span': 150,
            'enable_env_change': False,
            'env_change_type': "None",
            'env_change_start': 0,
            'env_change_intensity': 0,
            'description': "A forest ecosystem with abundant resources. Features higher reproduction rates and generally stable populations."
        },
        
        "Marine Ecosystem": {
            'prey_growth_rate': 1.5,
            'prey_death_rate': 0.1,
            'initial_prey': 200,
            'predator_death_rate': 0.25,
            'predator_growth_rate': 0.08,
            'initial_predator': 30,
            'time_span': 150,
            'enable_env_change': False,
            'env_change_type': "None",
            'env_change_start': 0,
            'env_change_intensity': 0,
            'description': "A marine ecosystem with high biodiversity. Features high prey reproduction but specialized predators."
        },
        
        "Unstable Ecosystem": {
            'prey_growth_rate': 1.8,
            'prey_death_rate': 0.3,
            'initial_prey': 50,
            'predator_death_rate': 0.2,
            'predator_growth_rate': 0.2,
            'initial_predator': 40,
            'time_span': 150,
            'enable_env_change': False,
            'env_change_type': "None",
            'env_change_start': 0,
            'env_change_intensity': 0,
            'description': "An ecosystem on the brink. Features extreme parameter values that lead to oscillatory behavior or population crashes."
        },
        
        "Arctic Ecosystem": {
            'prey_growth_rate': 0.5,
            'prey_death_rate': 0.05,
            'initial_prey': 150,
            'predator_death_rate': 0.3,
            'predator_growth_rate': 0.1,
            'initial_predator': 20,
            'time_span': 150,
            'enable_env_change': False,
            'env_change_type': "None",
            'env_change_start': 0,
            'env_change_intensity': 0,
            'description': "A cold environment with slow growth rates but strong resilience."
        },
        
        "Island Ecosystem": {
            'prey_growth_rate': 1.0,
            'prey_death_rate': 0.2,
            'initial_prey': 80,
            'predator_death_rate': 0.35,
            'predator_growth_rate': 0.15,
            'initial_predator': 15,
            'time_span': 150,
            'enable_env_change': False,
            'env_change_type': "None",
            'env_change_start': 0,
            'env_change_intensity': 0,
            'description': "An isolated ecosystem with specialized species and limited resources."
        },
        
        "Grassland Ecosystem": {
            'prey_growth_rate': 1.3,
            'prey_death_rate': 0.12,
            'initial_prey': 180,
            'predator_death_rate': 0.28,
            'predator_growth_rate': 0.09,
            'initial_predator': 35,
            'time_span': 150,
            'enable_env_change': False,
            'env_change_type': "None",
            'env_change_start': 0,
            'env_change_intensity': 0,
            'description': "An open ecosystem with abundant primary producers and visible predator-prey dynamics."
        },
        
        "Climate Change Scenario": {
            'prey_growth_rate': 1.1,
            'prey_death_rate': 0.1,
            'initial_prey': 100,
            'predator_death_rate': 0.3,
            'predator_growth_rate': 0.1,
            'initial_predator': 50,
            'time_span': 200,
            'enable_env_change': True,
            'env_change_type': "Temperature Increase",
            'env_change_start': 50,
            'env_change_intensity': 60,
            'description': "A simulation of climate change impacts on a standard ecosystem."
        },
        
        "Habitat Loss Scenario": {
            'prey_growth_rate': 1.1,
            'prey_death_rate': 0.1,
            'initial_prey': 100,
            'predator_death_rate': 0.3,
            'predator_growth_rate': 0.1,
            'initial_predator': 50,
            'time_span': 200,
            'enable_env_change': True,
            'env_change_type': "Habitat Loss",
            'env_change_start': 50,
            'env_change_intensity': 70,
            'description': "A simulation of progressive habitat destruction on ecosystem dynamics."
        },
        
        "Epidemic Scenario": {
            'prey_growth_rate': 1.1,
            'prey_death_rate': 0.1,
            'initial_prey': 100,
            'predator_death_rate': 0.3,
            'predator_growth_rate': 0.1,
            'initial_predator': 50,
            'time_span': 200,
            'enable_env_change': True,
            'env_change_type': "Disease",
            'env_change_start': 50,
            'env_change_intensity': 80,
            'description': "A simulation of disease outbreak affecting one or both species."
        }
    }
    
    return scenarios
