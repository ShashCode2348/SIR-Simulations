# SIR-Simulations

## About

4 simulations based on the SIR Model, which model the scenarios:
- No restrictions
- Isolation (testing twice a week)
- Social distancing
- Vaccination

For the situations with interventions, the interventions are after 20 days, and with 90% compliance, arguably higher than real life, but this can be modified.
The system of infection is not based on an infection radius; rather, probability is inversely proportional to the fourth power of distance between the particles. The constant of proportinality for this is distance_const, so feel free to change it if you wish.

## Requirements

- Python 3
- Matplotlib (with matplotlib-pygame addition)
- Pygame

## Usage

Download the Python file of your choice, and simply run it. You can also change the parameters to experiment with how the impacts change with 80% compliance compared to 90% compliance instead, by scrolling down to where the 'Parameters' comment is, and editing the values of your choice. Each restriction has its own individual set of parameters - follow the guidelines of comments as to what certain variables represent, and which ones you can/cannot change.

