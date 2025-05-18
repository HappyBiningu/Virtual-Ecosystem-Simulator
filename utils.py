import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

def save_scenario(name, scenario_data):
    """
    Save the current scenario to session state.
    
    Args:
        name (str): Name of the scenario
        scenario_data (dict): Dictionary containing scenario parameters
    """
    # If saved_scenarios doesn't exist in session state, create it
    if 'saved_scenarios' not in st.session_state:
        st.session_state.saved_scenarios = {}
    
    # Add timestamp to scenario data
    scenario_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to session state
    st.session_state.saved_scenarios[name] = scenario_data

def load_scenario(name):
    """
    Load a scenario from session state.
    
    Args:
        name (str): Name of the scenario to load
        
    Returns:
        dict: Dictionary containing scenario parameters
    """
    if 'saved_scenarios' in st.session_state and name in st.session_state.saved_scenarios:
        return st.session_state.saved_scenarios[name].copy()
    else:
        # Return default values if scenario not found
        return {
            'prey_growth_rate': 1.0,
            'prey_death_rate': 0.1,
            'initial_prey': 100,
            'predator_death_rate': 0.3,
            'predator_growth_rate': 0.1,
            'initial_predator': 50,
            'time_span': 100,
            'enable_env_change': False,
            'env_change_type': "None",
            'env_change_start': 0,
            'env_change_intensity': 0
        }

def export_simulation_data(times, results, filename='simulation_data.csv'):
    """
    Export simulation results to a CSV file.
    
    Args:
        times (array): Time points
        results (array): Population values
        filename (str): Name of output file
        
    Returns:
        str: Path to saved file or error message
    """
    try:
        df = pd.DataFrame({
            'Time': times,
            'Prey': results[:, 0],
            'Predator': results[:, 1]
        })
        
        df.to_csv(filename, index=False)
        return f"Data exported successfully to {filename}"
    except Exception as e:
        return f"Error exporting data: {str(e)}"

def calculate_ecosystem_metrics(results):
    """
    Calculate various ecological metrics from simulation results.
    
    Args:
        results (array): Population values for prey and predator
        
    Returns:
        dict: Dictionary of ecological metrics
    """
    prey_pop = results[:, 0]
    predator_pop = results[:, 1]
    
    # Basic statistics
    prey_mean = prey_pop.mean()
    prey_std = prey_pop.std()
    prey_min = prey_pop.min()
    prey_max = prey_pop.max()
    
    predator_mean = predator_pop.mean()
    predator_std = predator_pop.std()
    predator_min = predator_pop.min()
    predator_max = predator_pop.max()
    
    # Population stability (coefficient of variation)
    prey_cv = prey_std / prey_mean if prey_mean > 0 else 0
    predator_cv = predator_std / predator_mean if predator_mean > 0 else 0
    
    # Ecosystem stability (combined metric)
    ecosystem_stability = 1 / (prey_cv + predator_cv) if (prey_cv + predator_cv) > 0 else float('inf')
    
    # Final state
    final_prey = prey_pop[-1]
    final_predator = predator_pop[-1]
    
    # Oscillation analysis
    prey_peaks = []
    predator_peaks = []
    
    for i in range(1, len(prey_pop)-1):
        if prey_pop[i] > prey_pop[i-1] and prey_pop[i] > prey_pop[i+1]:
            prey_peaks.append((i, prey_pop[i]))
        if predator_pop[i] > predator_pop[i-1] and predator_pop[i] > predator_pop[i+1]:
            predator_peaks.append((i, predator_pop[i]))
    
    # Estimate average cycle period if there are enough peaks
    prey_period = 0
    predator_period = 0
    
    if len(prey_peaks) >= 2:
        peak_indices = [p[0] for p in prey_peaks]
        avg_interval = sum(peak_indices[i+1] - peak_indices[i] for i in range(len(peak_indices)-1)) / (len(peak_indices)-1)
        prey_period = avg_interval
    
    if len(predator_peaks) >= 2:
        peak_indices = [p[0] for p in predator_peaks]
        avg_interval = sum(peak_indices[i+1] - peak_indices[i] for i in range(len(peak_indices)-1)) / (len(peak_indices)-1)
        predator_period = avg_interval
    
    # Phase difference (time lag between prey and predator peaks)
    phase_diff = 0
    if len(prey_peaks) >= 1 and len(predator_peaks) >= 1:
        # Find the nearest predator peak after the first prey peak
        prey_peak_idx = prey_peaks[0][0]
        next_predator_peaks = [(i, p) for i, p in enumerate(predator_peaks) if p[0] > prey_peak_idx]
        if next_predator_peaks:
            next_predator_peak_idx = next_predator_peaks[0][1][0]
            phase_diff = next_predator_peak_idx - prey_peak_idx
    
    return {
        'prey_mean': prey_mean,
        'prey_std': prey_std,
        'prey_min': prey_min,
        'prey_max': prey_max,
        'prey_cv': prey_cv,
        'predator_mean': predator_mean,
        'predator_std': predator_std,
        'predator_min': predator_min,
        'predator_max': predator_max,
        'predator_cv': predator_cv,
        'ecosystem_stability': ecosystem_stability,
        'final_prey': final_prey,
        'final_predator': final_predator,
        'prey_period': prey_period,
        'predator_period': predator_period,
        'phase_difference': phase_diff,
        'prey_peaks_count': len(prey_peaks),
        'predator_peaks_count': len(predator_peaks)
    }
