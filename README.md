# SIR-Simulations

## About

4 simulations based on the SIR Model, which model the scenarios:
- No restrictions
- Isolation (testing twice a week)
- Social distancing
- Vaccination

For the situations with interventions, the interventions are after 20 days, and with 90% compliance, arguably higher than real life, but this can be modified.

## What is an SIR Model?

An SIR Model is a type of model used to model the spread of a pathogen. It splits people into 3 groups: Susceptible, who haven't been infected; Infected, who are currently infected; and removed, who were infected, but have since recovered or passed away. It is primarily determined by 2 values: transmission rate, the number of susceptible people becoming infected per infected person (or how many people an infected person infects per frame); and recovery rate, the number of infected people becoming removed per infected person (or the probability that an infected person recovers in a given frame).

Rather than basing infection rate off an infection radius (having a certain fixed probability of becoming infected if you are within a certain radius of an infected person, else you won't be infected), I opted for a system in which probability is inversely proportional to the fourth power of distance between the particles. The constant of proportinality for this is distance_const, so feel free to change it if you wish.

## Requirements

- Python 3
- Matplotlib (with matplotlib-pygame addition)
- Pygame

## Usage

Download the Python file of your choice, and simply run it. You can also change the parameters to experiment with how the impacts change with 80% compliance compared to 90% compliance instead, by scrolling down to where the 'Parameters' comment is, and editing the values of your choice. Each restriction has its own individual set of parameters - follow the guidelines of comments as to what certain variables represent, and which ones you can/cannot change.

There is also a file called 'Infection Radius Based.py' - this is a bonus file of sorts, operating on the basis of infection radius instead of the aforementioned system. Feel free to use it, and compare it to the other models.

![View Counter](https://view-counter.tobyhagan.com/?user=ShashCode2348/SIR-Simulations)
