import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

EMPTY = 0
SUSCEPTIBLE = 1
INFECTED_SYM = 2
INFECTED_ASYM = 3
RECOVERED = 4

class City():

    def __init__(self, size, duration, density, initialInfected, probInfection, probRecovery, probSymptomatic, probMoveSym, probMoveAsym, moveRadius):

        # PARAMETERS
        self.size = size                            # Size of 2D space
        self.duration = duration                    # Duration of the simulation
        self.density = density                      # Probability of an empty cell
        self.initial_infected = initialInfected     # Number of individuals infected at start of simulation
        self.probInfection = probInfection          # Probability of infection upon immediate proximity
        self.probRecovery = probRecovery            # Probability of an infected individual recovering each day
        self.probSymptomatic = probSymptomatic      # v2.0 Proability of becoming symptomatic
        self.probMoveSymptomatic = probMoveSym      # v2.1 Probability of movement from a symptomatic individual
        self.probMoveAsymptomatic = probMoveAsym    # v2.1 Probability of movement from an asymptomatic individual
        self.moveRadius = moveRadius                # v2.1 Radius of movement

        # VARIABLES
        self.state = np.zeros((size,size))          # State of each cell in the 2D space
        self.stats = np.zeros((duration+1,4))
        self.proportionInfected = np.zeros(duration+1)
        self.proportionRecovered = np.zeros(duration+1)
        self.day = 0

    def populate(self):
        """ Populate city at random """
        for i in range(self.size):
            for j in range(self.size):
                # Flip a coin to see if the cell is empty or not
                if random.random() < self.density:
                    self.state[i][j] = SUSCEPTIBLE
                else:
                    self.state[i][j] = EMPTY

    def randomIndividual(self):
        """ Pick a random individual (i.e. non-empty cell) """
        found = False
        while not found:
            i = random.randint(0,self.size-1)
            j = random.randint(0,self.size-1)
            if self.state[i][j] != EMPTY: # and self.pop[i][j] != DEAD:
                found = True
        return i,j

    def infect(self):
        """ Infect n randomly chosen individuals with the virus """
        for k in range(self.initial_infected):
            i,j=self.randomIndividual()
            self.state[i][j] = INFECTED_ASYM

    def gatherStats(self):
        """ Keep statistics """
        self.totalIndividuals = np.count_nonzero(self.state)
        self.proportionInfected[self.day] = (np.count_nonzero(self.state==INFECTED_ASYM) + np.count_nonzero(self.state==INFECTED_SYM)) / self.totalIndividuals
        self.proportionRecovered[self.day] = np.count_nonzero(self.state==RECOVERED) / self.totalIndividuals
        self.stats[self.day]=np.array([np.count_nonzero(self.state==SUSCEPTIBLE),np.count_nonzero(self.state==INFECTED_ASYM),np.count_nonzero(self.state==INFECTED_SYM),np.count_nonzero(self.state==RECOVERED)])/self.totalIndividuals

    def neighborsInfected(self, i, j):
        """ Count the number of immediate neighbors who are infected """
        number_infected = 0
        for x in range(i-1,i+2):
            ni = x%self.size
            for y in range(j-1,j+2):
                nj = y%self.size
                if self.state[ni][nj] == INFECTED_ASYM or self.state[ni][nj] == INFECTED_SYM:
                    number_infected += 1
        return number_infected

    def stepHealth(self):
        """ Update the health state of the city """
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == INFECTED_SYM:
                    if random.random() < self.probRecovery:
                        self.state[i][j] = RECOVERED
                elif self.state[i][j] == INFECTED_ASYM:
                    if random.random() < self.probRecovery:
                        self.state[i][j] = RECOVERED
                    if random.random() < self.probSymptomatic:
                        self.state[i][j] = INFECTED_SYM
                elif self.state[i][j] == SUSCEPTIBLE:
                    if self.neighborsInfected(i,j) > 0:
                        if random.random() < self.probInfection:
                            self.state[i][j] = INFECTED_ASYM
                else:
                    pass

    def stepMove(self):
        """ Update the locations of individuals in the city """
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == INFECTED_SYM:
                    if random.random() < self.probMoveSymptomatic:
                        self.move(i,j)
                elif self.state[i][j] == INFECTED_SYM or self.state[i][j] == SUSCEPTIBLE or self.state[i][j] == RECOVERED:
                    if random.random() < self.probMoveAsymptomatic:
                        self.move(i,j)
                else:
                    pass

    def move(self, i, j):
        """ Move the individual in cell i,j to an empty cell """
        newi,newj = self.randomNewSpace(i,j)
        self.state[newi][newj] = self.state[i][j]
        self.state[i][j] = EMPTY

    def randomNewSpace(self,i,j):
        """ Pick a random new empty cell in the city """
        found = False
        tries = 0
        while not found and tries < 50:
            new_i = (i+int(np.random.normal(0.0,self.moveRadius)))%self.size
            new_j = (j+int(np.random.normal(0.0,self.moveRadius)))%self.size
            if self.state[new_i][new_j] == EMPTY:
                found = True
            tries += 1
        if tries == 50:
            print("Empty cell not found.")
            return i,j
        else:
            return new_i, new_j

    def show(self,title):
        plt.clf()
        prop_cycle = plt.rcParams['axes.prop_cycle']
        cols = prop_cycle.by_key()['color']
        cmap = colors.ListedColormap(["white", cols[0], cols[1], cols[1], cols[2]])
        bounds=[-0.5,0.5,1.5,2.5,3.5]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        plt.imshow(self.state, interpolation="nearest", cmap=cmap, norm=norm)
        plt.xticks([])
        plt.yticks([])
        plt.title(title)
        plt.savefig(title+".png")
        #plt.show()
