import matplotlib
matplotlib.use("pygame")
import matplotlib.pyplot as plt
import os, sys, subprocess
from random import random
import pygame
import math

#debug helper
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit

# Particle and ParticleList classes
class ParticleList(list):
    def __init__(self, particles=[]):
        super().__init__(particles)
        self.R_vals, self.I_and_R_vals = [0], [0]
        self.x_vals = [0.0]

    def add(self, particle):
        self.append(particle)

    def move_all(self, step_len):
        for p in self:
            p.move(step_len)

    def step(self, recovery_rate, step_len):  #Modify to prevent escaping from box (see shell in editor for how)
        # move all particles
        self.move_all(step_len)

        # collect lists for speed
        susceptibles = [p for p in self if p.state == 0]
        infected = [p for p in self if p.state == 1]

        # Infecting people
        for s in susceptibles:
            for i in infected:
                if random() < distance_const/((s.position[0] - i.position[0])**2 + (s.position[1] - i.position[1])**2)**2:
                    s.state = 1
                    break

        for i in infected:
            if random() < isol_probability and particle_list.x_vals[-1] >= isol_start_time:   #isolation
                i.isolated = 1
                i.destination = [isol_X_offset + random()*isol_W, isol_Y_offset + random()*isol_H]
                i.d_vector = [(i.destination[0] - i.position[0])*step_len, (i.destination[1] - i.position[1])*step_len]
            if random() < recovery_rate:    # recoveries
                i.state = 2

    def update_graph(self):
        self.R_vals.append(sum(1 for p in self if p.state == 2))
        self.I_and_R_vals.append(sum(1 for p in self if p.state != 0))
        self.x_vals.append(self.x_vals[-1] + step_len)
        axes.cla()
        axes.set_xlabel("Time (days)", color="white", loc='right', labelpad = 9.0)
        axes.set_ylabel("Population", color="white", loc='top', labelpad = 18.0)
        plt.xlim(0, self.x_vals[-1])
        plt.ylim(0, population)
        axes.fill_between(self.x_vals, 0, self.R_vals, color="#676767", alpha=1, label='Removed')
        axes.fill_between(self.x_vals, self.R_vals, self.I_and_R_vals, color="#ED5151", alpha=1, label='Infected')
        axes.fill_between(self.x_vals, self.I_and_R_vals, population, color="#4C88F7", alpha=1, label='Susceptible')
        pygame.draw.rect(screen, (255, 255, 255), (W_offset, H_offset, W_sim, H_sim), 2)
        pygame.draw.rect(screen, (255, 255, 255), (W_offset + isol_X_offset, H_offset + isol_Y_offset, isol_W, isol_H), 2)
        screen.blit(fig, (0, -50))  #type: ignore
        R_value = round((self.I_and_R_vals[-1] - self.I_and_R_vals[-2])/(self.I_and_R_vals[-2] - self.R_vals[-2])/recovery_rate, 2) if self.I_and_R_vals[-2] > self.R_vals[-2] else 0
        screen.blit(font.render(f'R: {R_value}', True, (255, 255, 255)), (W_offset + 10, H_offset + H_sim + 10)) # type: ignore
    
    def main_loop(self):
        """
        Run the Pygame-based main simulation loop.
        Returns:
                None
        """
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False

            clock.tick(120)
            screen.fill((0, 0, 0))

            # advance simulation each frame
            self.step(recovery_rate, step_len)

            # draw particles from this list
            for p in self:
                pygame.draw.circle(screen, p.state_color(), (int(p.position[0]+W_offset), int(p.position[1]+H_offset)), circle_radius)
            self.update_graph()
            fig.canvas.draw()
            pygame.display.flip()

class Particle:
    def __init__(self, position, velocity_dir, acceleration_dir, state):
        self.position = position
        self.velocity_dir = velocity_dir
        self.acceleration_dir = acceleration_dir
        self.state = state  # 0: Susceptible, 1: Infected, 2: Removed
        self.isolated = 0   # 0: not isolated, 1: moving to isolation, 2: isolated
        self.destination = [0, 0]
        self.d_vector = [0, 0] # direction vector towards destination
        self.isol_steps = 1//step_len

    def move(self, step_len):
        # velocity_dir and acceleration_dir are treated as scalar angles (radians)
        fps = clock.get_fps() if clock.get_fps() > 0 else 60
        if self.isolated == 1:
            #if (self.position[0] + self.d_vector[0] >= self.destination[0] or self.d_vector[0] == 0) and (self.position[1] + self.d_vector[1] >= self.destination[1] or self.d_vector[1] == 0):
            if self.isol_steps <= 0:
                self.isolated = 2
            else:
                self.position[0] += self.d_vector[0]
                self.position[1] += self.d_vector[1]
                self.isol_steps -= 1
        elif self.isolated == 0:
            if (self.position[0] < circle_radius and math.cos(self.velocity_dir) < 0) or (self.position[0] > W_sim - circle_radius and math.cos(self.velocity_dir) > 0):
                self.velocity_dir -= 1.5*math.pi
            elif (self.position[1] < circle_radius and math.sin(self.velocity_dir) < 0) or (self.position[1] > H_sim - circle_radius and math.sin(self.velocity_dir) > 0):
                self.velocity_dir -= 0.5*math.pi
            else:
                self.velocity_dir += self.acceleration_dir * step_len
                self.velocity_dir = self.velocity_dir % (2 * math.pi)
            self.position[0] = (self.position[0] + math.cos(self.velocity_dir) * step_len * 90 / fps) % W_sim
            self.position[1] = (self.position[1] + math.sin(self.velocity_dir) * step_len * 90 / fps) % H_sim
            # randomize angular acceleration a bit
            if random() < 0.2:
                self.acceleration_dir = round(random() * math.pi / 25, 2)
        else:
            if (self.position[0] - isol_X_offset < circle_radius and math.cos(self.velocity_dir) < 0) or (self.position[0] - isol_X_offset > isol_W - circle_radius and math.cos(self.velocity_dir) > 0):
                self.velocity_dir -= 1.5*math.pi
            elif (self.position[1] - isol_Y_offset < circle_radius and math.sin(self.velocity_dir) < 0) or (self.position[1] - isol_Y_offset > isol_H - circle_radius and math.sin(self.velocity_dir) > 0):
                self.velocity_dir -= 0.5*math.pi
            else:
                self.velocity_dir += self.acceleration_dir * step_len
                self.velocity_dir = self.velocity_dir % (2 * math.pi)
            self.position[0] = ((self.position[0] + math.cos(self.velocity_dir) * step_len * 90 / fps) - isol_X_offset) % isol_W + isol_X_offset
            self.position[1] = ((self.position[1] + math.sin(self.velocity_dir) * step_len * 90 / fps) - isol_Y_offset) % isol_H + isol_Y_offset
            # randomize angular acceleration a bit
            if random() < 0.2:
                self.acceleration_dir = round(random() * math.pi / 25, 2)
    
    def state_color(self):
        return colour_dict[self.state]


#Setup initial conditions and particles
W, H = 1400, 900
W_sim, H_sim = 600, 600
W_offset, H_offset = 750, 25
circle_radius = 3
colour_dict = {0: "#4C88F7", 1: "#ED5151", 2: "#676767"}

#Parameters for SIR model
S, I, R = 992.0, 8.0, 0.0
population = S + I + R
step_len, duration = 0.1, 200       #both in days, step_len is how much time each frame represents
recovery_rate = 1/10 * step_len     #10 days on average to recover
distance_const = 1e-4 * (W_sim**2 + H_sim**2)

#Parameters for isolation (only edit the first and last of these to change behaviour of isolation, middle two are for visualisation)
isol_start_time = 20.0  #days
isol_W, isol_H = 200, 200
isol_X_offset, isol_Y_offset = 0, 650     #Relative to top-left of simulation box
isol_probability = 0.9 * step_len * 2/7   #Isolation twice a week

#Particle setup
particles = []
for _ in range(int(S)):
    particles.append(Particle(position=[round(random()*(W_sim-2*circle_radius))+circle_radius, round(random()*(H_sim-2*circle_radius)+circle_radius)], acceleration_dir=round(random()*math.pi/5, 2), velocity_dir=round(random()*2*math.pi, 2), state=0))
for _ in range(int(I)):
    particles.append(Particle(position=[round(random()*(W_sim-2*circle_radius))+circle_radius, round(random()*(H_sim-2*circle_radius)+circle_radius)], acceleration_dir=round(random()*math.pi/5, 2), velocity_dir=round(random()*2*math.pi, 2), state=1))

particle_list = ParticleList(particles)

# Pygame setup
if os.environ.get("RUN_PYGAME_SUBPROCESS") != "1":
    env = os.environ.copy()
    env["RUN_PYGAME_SUBPROCESS"] = "1"
    if sys.platform == "win32":
        subprocess.Popen([sys.executable] + sys.argv, creationflags=subprocess.CREATE_NEW_CONSOLE, env=env)
        sys.exit(0)
    else:
        os.execv(sys.executable, [sys.executable] + sys.argv)

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("SIR Model Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

#Matplotlib setup
graph_width, graph_height = 750, 550
plt.rcParams['figure.figsize'] = [graph_width/100, graph_height/100]
fig, axes = plt.subplots(1,1)
fig.patch.set_facecolor((0,0,0)); axes.patch.set_facecolor((0,0,0))
axes.spines['bottom'].set_color('white'); axes.spines['left'].set_color('white')
axes.tick_params(axis='x', colors='white'); axes.tick_params(axis='y', colors='white')
axes.set_xlabel("Time (days)", color="white", loc='right')
axes.set_ylabel("Population", color="white", loc='top')
plt.xlim(0, particle_list.x_vals[-1])
plt.ylim(0, population)
fig.canvas.draw()
screen.blit(fig, (50, 50))  #type: ignore 
axes.fill_between(particle_list.x_vals, 0, particle_list.R_vals, color="#ED5151", alpha=1, label='Infected')
axes.fill_between(particle_list.x_vals, particle_list.R_vals, particle_list.I_and_R_vals, color="#4C88F7", alpha=1, label='Susceptible')
axes.fill_between(particle_list.x_vals, particle_list.I_and_R_vals, population, color="#676767", alpha=1, label='Removed')
pygame.display.update() 

# Run the main simulation loop
particle_list.main_loop()
pygame.quit()
sys.exit(0)

