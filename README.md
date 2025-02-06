# Digital Twin Signal Propagation Simulation Project

## Project Description

This project aims to simulate wireless signal propagation in an urban environment using a digital twin, created through the integration of **Unreal Engine 5.3** and **Nvidia Sionna**. The developed software allows modeling, calculating, and visualizing signal coverage in a complex urban scenario.

### Technologies Used
- **Unreal Engine 5.3**: Real-time 3D simulation engine.
- **Blender 4.1**: Used for creating 3D models of urban buildings.
- **Nvidia Sionna**: Library for simulating wireless signal propagation.
- **Python & TensorFlow**: Languages and libraries for automation and simulation data analysis.

## Objectives

The objective of the project is to provide a tool that:
1. Accurately simulates signal propagation in a complex urban environment.
2. Visualizes signal paths and coverage maps through a realistic digital twin.
3. Allows comparison between simulated data and real data to validate the model's accuracy.

## Main Features

1. **3D Model Creation**: Using **Blender** and **OpenStreetMap** data, a 3D model of the urban area is generated.
2. **Signal Propagation Simulation**: Thanks to **Nvidia Sionna** and differentiable **ray tracing**, the propagation of the signal between transmitters (TX) and receivers (RX) is simulated.
3. **Signal Path Visualization**: In **Unreal Engine**, the signal paths are traced and visualized using `Blueprints` that draw debug lines between TX and RX.
4. **Coverage Map Generation**: A high-resolution coverage map is generated, representing the signal strength in decibels for each point in the urban area.

## Project Structure

The project is divided into four main phases:
1. **Importing the Urban Model**: Geographical data is imported from OpenStreetMap and converted into 3D models using Blender.
2. **Propagation Simulation**: Nvidia Sionna is used to calculate the signal paths and generate the coverage map.
3. **Visualization**: The simulation results are imported into Unreal Engine for interactive visualization.
4. **Model Validation**: The simulation results are compared with real field data to validate the model.

## How to Run the Project

### Prerequisites
- **Unreal Engine 5.3**
- **Blender 4.1**
- **Nvidia Sionna**
- **Python 3.8+** with **TensorFlow**

### Instructions

1. **Data Import**:
   - Open **Blender** and use the `Blosm` add-on to import data from **OpenStreetMap**.
   - Export the 3D model as an `.obj` file and `.xml` for Unreal Engine and Nvidia Sionna respectively.

2. **Simulation**:
   - Run the Python script to launch Nvidia Sionna and calculate the signal paths and coverage map.
   - Export the results in CSV and image format.

3. **Visualization**:
   - Import the exported data into **Unreal Engine**.
   - Use the provided `Blueprints` to visualize the signal paths and coverage map.

## Results

The project has enabled the creation of a detailed digital twin of an urban environment, calculating complex signal paths and generating a high-resolution coverage map. The results were compared with real data to verify accuracy.

## Future Developments

- Improvement of the model to include dynamic obstacles (e.g., vehicles and people).
- Integration with machine learning models for real-time network optimization.

## Authors

- **Carlo Zamuner** - Graduate student in Computer, Communications and Electronics Engineering at the University of Trento.
