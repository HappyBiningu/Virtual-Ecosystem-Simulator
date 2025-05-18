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
            'description': "A desert ecosystem with limited resources. Features lower reproduction rates and higher mortality.",
            'region': "Southwest U.S. Desert",
            'prey_species': "Desert Cottontail Rabbit",
            'predator_species': "Coyote"
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
            'description': "A forest ecosystem with abundant resources. Features higher reproduction rates and generally stable populations.",
            'region': "Pacific Northwest Temperate Rainforest",
            'prey_species': "Snowshoe Hare",
            'predator_species': "Canadian Lynx"
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
            'description': "A marine ecosystem with high biodiversity. Features high prey reproduction but specialized predators.",
            'region': "Atlantic Coastal Waters",
            'prey_species': "Atlantic Herring",
            'predator_species': "Atlantic Cod"
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
            'description': "An ecosystem on the brink. Features extreme parameter values that lead to oscillatory behavior or population crashes.",
            'region': "Overgrazed Savanna",
            'prey_species': "Thomson's Gazelle",
            'predator_species': "African Lion"
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
            'description': "A cold environment with slow growth rates but strong resilience.",
            'region': "Arctic Tundra",
            'prey_species': "Arctic Hare",
            'predator_species': "Arctic Fox"
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
            'description': "An isolated ecosystem with specialized species and limited resources.",
            'region': "Galapagos Islands",
            'prey_species': "Marine Iguana",
            'predator_species': "Galapagos Hawk"
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
            'description': "An open ecosystem with abundant primary producers and visible predator-prey dynamics.",
            'region': "Serengeti Plains",
            'prey_species': "Wildebeest",
            'predator_species': "Spotted Hyena"
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
            'description': "A simulation of climate change impacts on a standard ecosystem.",
            'region': "Boreal Forest",
            'prey_species': "Moose",
            'predator_species': "Wolf",
            'research_notes': "Based on studies showing reduced prey reproduction and increased metabolic stress with rising temperatures."
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
            'description': "A simulation of progressive habitat destruction on ecosystem dynamics.",
            'region': "Amazon Rainforest",
            'prey_species': "Capybara",
            'predator_species': "Jaguar",
            'research_notes': "Based on deforestation patterns and their impacts on population carrying capacity and hunting efficiency."
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
            'description': "A simulation of disease outbreak affecting one or both species.",
            'region': "Wyoming-Montana Region",
            'prey_species': "Elk",
            'predator_species': "Gray Wolf",
            'research_notes': "Based on historical disease outbreaks like chronic wasting disease in cervids."
        },
        
        "Invasive Species Impact": {
            'prey_growth_rate': 1.0,
            'prey_death_rate': 0.1,
            'initial_prey': 120,
            'predator_death_rate': 0.2,
            'predator_growth_rate': 0.2, 
            'initial_predator': 5,
            'time_span': 300,
            'enable_env_change': True,
            'env_change_type': "Resource Depletion",
            'env_change_start': 100,
            'env_change_intensity': 50,
            'description': "Simulates the introduction of an invasive predator with high efficiency and low initial numbers.",
            'region': "Australian Outback",
            'prey_species': "Bilby",
            'predator_species': "Feral Cat (invasive)",
            'research_notes': "Demonstrates typical population dynamics when a non-native predator enters a new ecosystem with prey not adapted to its hunting strategies."
        },
        
        "Extreme Weather Events": {
            'prey_growth_rate': 1.2,
            'prey_death_rate': 0.08,
            'initial_prey': 150,
            'predator_death_rate': 0.25,
            'predator_growth_rate': 0.12,
            'initial_predator': 40,
            'time_span': 250,
            'enable_env_change': True,
            'env_change_type': "Habitat Loss",
            'env_change_start': 100,
            'env_change_intensity': 90,
            'description': "Models sudden catastrophic events like hurricanes or floods that drastically but temporarily alter habitat conditions.",
            'region': "Gulf Coast Wetlands",
            'prey_species': "Marsh Rabbit",
            'predator_species': "American Alligator",
            'research_notes': "The environmental change is severe but temporary, showing how resilience and recovery mechanisms function after disasters."
        },
        
        "Seasonal Migration Dynamics": {
            'prey_growth_rate': 1.4,
            'prey_death_rate': 0.15,
            'initial_prey': 200,
            'predator_death_rate': 0.3,
            'predator_growth_rate': 0.08,
            'initial_predator': 30,
            'time_span': 365,
            'enable_env_change': True,
            'env_change_type': "Temperature Increase",
            'env_change_start': 90,
            'env_change_intensity': 40,
            'description': "Simulates annual cycles with seasonal variations in predator-prey interactions due to migration patterns.",
            'region': "African Savanna",
            'prey_species': "Zebra",
            'predator_species': "Lion",
            'research_notes': "The environmental changes represent seasonal shifts that temporarily reduce interaction between species due to migration movements."
        },
        
        "Conservation Intervention": {
            'prey_growth_rate': 0.7,
            'prey_death_rate': 0.3,
            'initial_prey': 40,
            'predator_death_rate': 0.4,
            'predator_growth_rate': 0.15,
            'initial_predator': 25,
            'time_span': 300,
            'enable_env_change': True,
            'env_change_type': "Habitat Loss",
            'env_change_start': 50,
            'env_change_intensity': -50,  # Negative value represents improvement
            'description': "Models the impact of conservation efforts to improve habitat and species protection in a degraded ecosystem.",
            'region': "European Alpine Forest",
            'prey_species': "Alpine Ibex",
            'predator_species': "Eurasian Lynx",
            'research_notes': "The negative environmental change value represents habitat restoration and protected area establishment."
        }
    }
    
    return scenarios
