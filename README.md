
# 🌿 Virtual Ecosystem Simulator

An interactive web application that simulates predator-prey dynamics and ecosystem stability using the Lotka-Volterra model.

## Features

- **Interactive Simulation**: Adjust parameters like growth rates, death rates, and initial populations
- **Environmental Changes**: Simulate impacts of climate change, habitat loss, disease outbreaks
- **Real-world Scenarios**: Pre-configured ecosystems based on actual ecological research
- **Advanced Visualization**: Population trends, phase space diagrams, and ecological networks
- **Data Analysis**: Statistical metrics, stability analysis, and population cycle detection

## Getting Started

1. Click the "Run" button to start the Streamlit application
2. Access the simulator through the provided URL
3. Select a preset scenario or customize your own parameters
4. Run simulations and analyze the results

## Simulator Tabs

1. **Simulator**: Main simulation interface with parameter controls
2. **Ecological Network**: Visual representation of species interactions
3. **Data Analysis**: Detailed statistical analysis and insights
4. **Scenario Research**: Information about real-world ecosystem scenarios
5. **About**: Technical details about the Lotka-Volterra model

## Components

- `app.py`: Main Streamlit application
- `ecosystem_model.py`: Core simulation logic
- `multispecies.py`: Extended model for multiple species
- `preset_scenarios.py`: Pre-configured ecosystem scenarios
- `visualization.py`: Population and network plotting functions
- `utils.py`: Helper functions and metrics calculation

## Model Description

The simulator uses the Lotka-Volterra equations:
- Prey population: dx/dt = αx - βxy
- Predator population: dy/dt = δxy - γy

Where:
- x: prey population
- y: predator population
- α: prey growth rate
- β: prey death rate due to predation
- γ: predator death rate
- δ: predator growth rate from consuming prey

## Built With

- Python
- Streamlit
- NumPy
- SciPy
- Matplotlib
- Plotly
- NetworkX

## Usage Example

1. Select a preset ecosystem (e.g., "Forest Ecosystem")
2. Adjust parameters if desired
3. Enable environmental changes to simulate disturbances
4. Click "Run Simulation" to see the results
5. Analyze population dynamics and ecosystem stability

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
