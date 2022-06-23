import city
import matplotlib.pyplot as plt
import numpy as np

def runSimNoShow():
    done = False
    c = city.City(size, duration, density, initialInfected, probInfection, probRecovery, probSymptomatic, probMoveSym, probMoveAsym, moveRadius)
    c.populate()
    c.infect()
    c.gatherStats()
    c.show("Start")
    for day in range(duration):
        c.day += 1
        c.stepHealth()
        c.stepMove()
        c.gatherStats()
    c.show("Final")
    return c

size = 100
duration = 1000
density = 0.2
initialInfected = 1
probInfection = 0.5
probRecovery = 0.01
probSymptomatic = 0.01
probMoveSym = 0.0
probMoveAsym = 1.0
moveRadius = 10

c=runSimNoShow()
plt.clf()
plt.plot(c.stats)
plt.xlabel("Days")
plt.ylabel("Proportion")
plt.legend(("Susecptible","Infected (Asymp)","Infected (Symp)","Recovered"))
# plt.savefig("individualrun.png")
plt.show()
