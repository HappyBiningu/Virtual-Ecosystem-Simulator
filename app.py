import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import time
import base64
from ecosystem_model import run_lotka_volterra, run_habitat_change_simulation
from visualization import plot_population_trends, plot_ecological_network, plot_phase_space
from preset_scenarios import get_preset_scenarios
from utils import save_scenario, load_scenario, export_simulation_data, calculate_ecosystem_metrics

# Set page configuration
st.set_page_config(
    page_title="Virtual Ecosystem Simulator",
    page_icon="🌿",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None
if 'network_data' not in st.session_state:
    st.session_state.network_data = None
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = {}
if 'saved_scenarios' not in st.session_state:
    st.session_state.saved_scenarios = {}

# Title and Introduction
st.title("🌿 Virtual Ecosystem Simulator")
st.markdown("""
    Explore predator-prey dynamics and ecosystem stability with this interactive simulator.
    Adjust parameters, introduce environmental changes, and observe how species populations evolve over time.
""")

# Main layout with tabs
tab1, tab2, tab3 = st.tabs(["Simulator", "Ecological Network", "About"])

with tab1:
    # Sidebar for controls
    st.sidebar.header("Simulation Parameters")
    
    # Presets section
    st.sidebar.subheader("Ecosystem Presets")
    preset_scenarios = get_preset_scenarios()
    preset_option = st.sidebar.selectbox(
        "Select a preset ecosystem",
        ["Custom"] + list(preset_scenarios.keys())
    )
    
    # Load preset if selected
    if preset_option != "Custom" and preset_option != st.session_state.get('last_preset', None):
        st.session_state.current_scenario = preset_scenarios[preset_option].copy()
        st.session_state.last_preset = preset_option
    
    # Species Parameters Section
    st.sidebar.subheader("Species Parameters")
    
    with st.sidebar.expander("Prey Species", expanded=True):
        prey_growth_rate = st.slider(
            "Prey Growth Rate (α)", 0.01, 2.0, 
            st.session_state.current_scenario.get('prey_growth_rate', 1.0),
            help="The rate at which the prey population grows in the absence of predators"
        )
        
        prey_death_rate = st.slider(
            "Prey Death Rate due to Predation (β)", 0.01, 2.0, 
            st.session_state.current_scenario.get('prey_death_rate', 0.1),
            help="The rate at which prey are caught and consumed by predators"
        )
        
        initial_prey = st.slider(
            "Initial Prey Population", 1, 1000, 
            st.session_state.current_scenario.get('initial_prey', 100),
            help="Starting population size of the prey species"
        )
    
    with st.sidebar.expander("Predator Species", expanded=True):
        predator_death_rate = st.slider(
            "Predator Death Rate (γ)", 0.01, 2.0, 
            st.session_state.current_scenario.get('predator_death_rate', 0.3),
            help="The natural death rate of predators in the absence of prey"
        )
        
        predator_growth_rate = st.slider(
            "Predator Growth Rate from Predation (δ)", 0.01, 2.0, 
            st.session_state.current_scenario.get('predator_growth_rate', 0.1),
            help="The efficiency at which predators convert consumed prey into new predators"
        )
        
        initial_predator = st.slider(
            "Initial Predator Population", 1, 1000, 
            st.session_state.current_scenario.get('initial_predator', 50),
            help="Starting population size of the predator species"
        )
    
    # Environmental Parameters
    st.sidebar.subheader("Environmental Parameters")
    
    with st.sidebar.expander("Habitat & Climate", expanded=True):
        time_span = st.slider(
            "Simulation Time (t)", 10, 500, 
            st.session_state.current_scenario.get('time_span', 100),
            help="Duration of the simulation in time units"
        )
        
        st.markdown("##### Environmental Changes")
        enable_env_change = st.checkbox(
            "Enable Environmental Changes",
            st.session_state.current_scenario.get('enable_env_change', False),
            help="Simulate changes in habitat or climate that affect species parameters"
        )
        
        env_change_start = 0
        env_change_intensity = 0
        env_change_type = "None"
        
        if enable_env_change:
            env_change_type = st.selectbox(
                "Change Type",
                ["Temperature Increase", "Habitat Loss", "Resource Depletion", "Disease"],
                index=["None", "Temperature Increase", "Habitat Loss", "Resource Depletion", "Disease"].index(
                    st.session_state.current_scenario.get('env_change_type', "Temperature Increase")
                ) - 1 if st.session_state.current_scenario.get('env_change_type', "None") != "None" else 0,
                help="Type of environmental change to simulate"
            )
            
            env_change_start = st.slider(
                "Start Time", 1, time_span-5, 
                min(st.session_state.current_scenario.get('env_change_start', time_span//4), time_span-5),
                help="When the environmental change begins (time units)"
            )
            
            env_change_intensity = st.slider(
                "Intensity (%)", 0, 100, 
                st.session_state.current_scenario.get('env_change_intensity', 30),
                help="Severity of the environmental change"
            )
    
    # Save current parameters to session state
    st.session_state.current_scenario = {
        'prey_growth_rate': prey_growth_rate,
        'prey_death_rate': prey_death_rate,
        'initial_prey': initial_prey,
        'predator_death_rate': predator_death_rate,
        'predator_growth_rate': predator_growth_rate,
        'initial_predator': initial_predator,
        'time_span': time_span,
        'enable_env_change': enable_env_change,
        'env_change_type': env_change_type if enable_env_change else "None",
        'env_change_start': env_change_start if enable_env_change else 0,
        'env_change_intensity': env_change_intensity if enable_env_change else 0
    }
    
    # Save/Load scenario section
    st.sidebar.subheader("Save/Load Scenario")
    scenario_name = st.sidebar.text_input("Scenario Name", "My Scenario")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("💾 Save"):
            save_scenario(scenario_name, st.session_state.current_scenario)
            st.sidebar.success(f"Saved: {scenario_name}")
    
    with col2:
        saved_scenarios = list(st.session_state.saved_scenarios.keys())
        if saved_scenarios:
            load_option = st.selectbox("Load Scenario", ["Select..."] + saved_scenarios)
            if load_option != "Select..." and st.button("📂 Load"):
                st.session_state.current_scenario = load_scenario(load_option)
                st.sidebar.success(f"Loaded: {load_option}")
                st.rerun()
    
    # Run Simulation Button
    run_simulation = st.sidebar.button("🚀 Run Simulation", type="primary")
    
    # Main content area
    st.subheader("Population Dynamics")
    
    # Run simulation when button is clicked
    if run_simulation:
        with st.spinner("Simulating ecosystem..."):
            # If environmental changes are enabled, use habitat change simulation
            if enable_env_change:
                times, results, events = run_habitat_change_simulation(
                    prey_growth_rate, prey_death_rate, 
                    predator_death_rate, predator_growth_rate,
                    initial_prey, initial_predator, time_span,
                    env_change_type, env_change_start, env_change_intensity
                )
            else:
                # Run basic Lotka-Volterra model
                times, results = run_lotka_volterra(
                    prey_growth_rate, prey_death_rate, 
                    predator_death_rate, predator_growth_rate,
                    initial_prey, initial_predator, time_span
                )
                events = []
            
            # Store results in session state
            st.session_state.simulation_results = {
                'times': times,
                'results': results,
                'events': events
            }
            
            # Generate network data
            st.session_state.network_data = {
                'prey_growth_rate': prey_growth_rate,
                'prey_death_rate': prey_death_rate,
                'predator_death_rate': predator_death_rate,
                'predator_growth_rate': predator_growth_rate,
                'prey_pop': results[-1, 0],
                'predator_pop': results[-1, 1]
            }
    
    # Display simulation results if available
    if st.session_state.simulation_results is not None:
        plot_data = st.session_state.simulation_results
        
        # Create tabs for different visualization types
        view_tab1, view_tab2, view_tab3 = st.tabs(["Line Chart", "Interactive Plot", "Phase Space"])
        
        with view_tab1:
            fig_line = plot_population_trends(
                plot_data['times'], 
                plot_data['results'], 
                plot_data.get('events', []),
                plot_type='matplotlib'
            )
            st.pyplot(fig_line)
        
        with view_tab2:
            fig_plotly = plot_population_trends(
                plot_data['times'], 
                plot_data['results'], 
                plot_data.get('events', []),
                plot_type='plotly'
            )
            st.plotly_chart(fig_plotly, use_container_width=True)
            
        with view_tab3:
            fig_phase = plot_phase_space(plot_data['results'])
            st.pyplot(fig_phase)
            st.markdown("""
            **Phase Space Interpretation:** 
            
            This diagram shows predator population (y-axis) versus prey population (x-axis). 
            Each point represents the population state at a moment in time, with arrows showing the direction of change.
            
            - Circular patterns indicate cyclical population dynamics
            - Spirals inward suggest stability over time
            - Spirals outward suggest instability
            - The starting point is marked in green, and the ending point in red
            """)
        
        # Export functionality
        st.download_button(
            label="📊 Export Simulation Data (CSV)",
            data=pd.DataFrame({
                'Time': plot_data['times'],
                'Prey': plot_data['results'][:, 0],
                'Predator': plot_data['results'][:, 1]
            }).to_csv(index=False),
            file_name="ecosystem_simulation_data.csv",
            mime="text/csv",
        )
        
        # Display final population stats
        st.subheader("Final Population Statistics")
        col1, col2 = st.columns(2)
        with col1:
            final_prey = plot_data['results'][-1, 0]
            st.metric(
                "Prey Population", 
                f"{final_prey:.1f}",
                f"{final_prey - initial_prey:.1f}"
            )
        
        with col2:
            final_predator = plot_data['results'][-1, 1]
            st.metric(
                "Predator Population", 
                f"{final_predator:.1f}",
                f"{final_predator - initial_predator:.1f}"
            )
        
        # Display interpretation
        prey_change = ((final_prey - initial_prey) / initial_prey) * 100
        predator_change = ((final_predator - initial_predator) / initial_predator) * 100
        
        st.subheader("Ecological Interpretation")
        
        if abs(prey_change) < 10 and abs(predator_change) < 10:
            st.success("The ecosystem appears to be relatively stable, with population levels showing only minor fluctuations.")
        elif prey_change > 50 and predator_change < -30:
            st.warning("The prey population is growing rapidly while predators are declining, suggesting a potential imbalance in the ecosystem.")
        elif prey_change < -50 and predator_change > 0:
            st.error("The prey population has crashed significantly, which may eventually lead to predator decline due to food scarcity.")
        elif prey_change < -30 and predator_change < -30:
            st.error("Both populations are declining significantly, indicating a potentially endangered ecosystem.")
        else:
            st.info("The ecosystem shows typical predator-prey population cycles.")
        
        if enable_env_change:
            st.markdown(f"**Environmental Change Effects:** The {env_change_type.lower()} that occurred at time {env_change_start} with {env_change_intensity}% intensity has affected the population dynamics.")
            
        # Population Stability Metrics section
        st.subheader("Population Stability Metrics")
        metrics = calculate_ecosystem_metrics(plot_data['results'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ecosystem Stability Score", f"{metrics['ecosystem_stability']:.2f}", 
                     help="Higher values indicate a more stable ecosystem (lower coefficient of variation)")
            st.metric("Prey Oscillation Period", f"{metrics['prey_period']:.1f}" if metrics['prey_period'] > 0 else "N/A",
                     help="Average time between prey population peaks")
        
        with col2:
            st.metric("Prey Coefficient of Variation", f"{metrics['prey_cv']:.3f}",
                    help="Measure of prey population variability (lower is more stable)")
            st.metric("Prey Population Peaks", f"{metrics['prey_peaks_count']}",
                    help="Number of prey population peaks detected")
        
        with col3:
            st.metric("Predator Coefficient of Variation", f"{metrics['predator_cv']:.3f}",
                    help="Measure of predator population variability (lower is more stable)")
            st.metric("Phase Difference", f"{metrics['phase_difference']:.1f}" if metrics['phase_difference'] > 0 else "N/A",
                    help="Time lag between prey and predator peaks")
        
        # Expandable detailed statistics
        with st.expander("Detailed Statistics"):
            st.markdown("### Raw Population Statistics")
            stats_df = pd.DataFrame({
                "Metric": ["Mean", "Standard Deviation", "Minimum", "Maximum", "Final Value"],
                "Prey": [
                    f"{metrics['prey_mean']:.2f}", 
                    f"{metrics['prey_std']:.2f}", 
                    f"{metrics['prey_min']:.2f}", 
                    f"{metrics['prey_max']:.2f}",
                    f"{metrics['final_prey']:.2f}"
                ],
                "Predator": [
                    f"{metrics['predator_mean']:.2f}", 
                    f"{metrics['predator_std']:.2f}", 
                    f"{metrics['predator_min']:.2f}", 
                    f"{metrics['predator_max']:.2f}",
                    f"{metrics['final_predator']:.2f}"
                ]
            })
            st.table(stats_df)
    else:
        st.info("Click 'Run Simulation' to see the ecosystem dynamics.")

with tab2:
    st.subheader("Ecological Network Visualization")
    
    if st.session_state.network_data is not None:
        network_fig = plot_ecological_network(st.session_state.network_data)
        st.pyplot(network_fig)
        
        st.markdown("""
        **Network Interpretation:**
        
        This diagram represents the ecological relationships in the simulated ecosystem:
        - Arrows indicate the direction of energy/resource flow
        - Arrow thickness represents the strength of the interaction
        - Node size corresponds to population size
        
        The predator-prey relationship is the primary interaction shown, but the model also 
        implicitly represents other factors like resource availability and competition.
        """)
    else:
        st.info("Run a simulation first to visualize the ecological network.")

with tab3:
    st.subheader("About the Virtual Ecosystem Simulator")
    
    st.markdown("""
    ### The Lotka-Volterra Model
    
    This simulator is based on the Lotka-Volterra equations, also known as the predator-prey equations. These differential equations describe the dynamics of biological systems in which two species interact, one as a predator and the other as prey.
    
    The basic equations are:
    
    **Prey population:** $\\frac{dx}{dt} = \\alpha x - \\beta xy$
    
    **Predator population:** $\\frac{dy}{dt} = \\delta xy - \\gamma y$
    
    Where:
    - $x$ is the prey population
    - $y$ is the predator population
    - $\\alpha$ is the prey growth rate (reproduction)
    - $\\beta$ is the prey death rate due to predation
    - $\\gamma$ is the predator death rate
    - $\\delta$ is the predator growth rate from consuming prey
    
    ### Environmental Changes
    
    The simulator also allows for introducing environmental changes that modify these parameters:
    
    - **Temperature Increase**: Affects reproduction and death rates
    - **Habitat Loss**: Reduces carrying capacity and increases competition
    - **Resource Depletion**: Decreases prey growth rate
    - **Disease**: Increases death rates for affected species
    
    ### Limitations
    
    This is a simplified model that doesn't account for:
    - Multiple species interactions
    - Spatial heterogeneity
    - Age structure
    - Genetic diversity
    - Detailed behavioral mechanisms
    
    ### Applications
    
    Despite its simplicity, this model provides valuable insights into:
    - Population cycles
    - Ecosystem stability and resilience
    - Tipping points and critical thresholds
    - Impact of environmental changes on food webs
    """)
    
    st.subheader("Further Reading")
    st.markdown("""
    - [Understanding the Lotka-Volterra Model](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations)
    - [Ecological Networks and Food Webs](https://en.wikipedia.org/wiki/Food_web)
    - [Ecosystem Stability and Resilience](https://en.wikipedia.org/wiki/Ecological_resilience)
    """)
