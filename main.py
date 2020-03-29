import sys
import ast
import json
import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd
import random
from matplotlib import pyplot as plt

from Agent import Agent
import config

# Population Description
print("\nPopulation Description")
print("Males")
male_population_description = {
    "population": config.male_SMVs,
    "count": len(config.male_SMVs),
    "min": min(config.male_SMVs),
    "max": max(config.male_SMVs),
    "ratio": len(config.male_SMVs) / (len(config.female_SMVs) + len(config.male_SMVs)),
    "mean": statistics.mean(config.male_SMVs),
    "hmean": statistics.harmonic_mean(config.male_SMVs),
    "gmean": statistics.geometric_mean(config.male_SMVs),
}

print(json.dumps(male_population_description, indent=4))

print("Female")
female_population_description = {
    "population": config.female_SMVs,
    "count": len(config.female_SMVs),
    "min": min(config.female_SMVs),
    "max": max(config.female_SMVs),
    "ratio": len(config.female_SMVs) / (len(config.female_SMVs) + len(config.male_SMVs)),
    "mean": statistics.mean(config.female_SMVs),
    "hmean": statistics.harmonic_mean(config.female_SMVs),
    "gmean": statistics.geometric_mean(config.female_SMVs),
}
print(json.dumps(female_population_description, indent=4))

bins = np.arange(min(male_population_description["min"], female_population_description["min"]),
                 max(male_population_description["max"], female_population_description["max"]) + 1, 0.5).tolist()
plt.hist([male_population_description["population"],
          female_population_description["population"]],
         bins=bins, color=['blue', 'pink'], edgecolor='black', rwidth=1.0,
         label=["Male (" + str(male_population_description["count"]) +
                ") ratio: " + str(round(male_population_description["ratio"], 2)),
                "Female (" + str(female_population_description["count"]) +
                ") ratio: " + str(round(female_population_description["ratio"], 2))])

plt.axvline(female_population_description["mean"], color='red', label='F Mean')
plt.axvline(female_population_description["hmean"], color='yellow', label='F Harm Mean')
plt.axvline(female_population_description["gmean"], color='orange', label='F Geo Mean')
plt.axvline(male_population_description["mean"], color='blue', label='M Mean')
plt.axvline(male_population_description["hmean"], color='green', label='M Harm Mean')
plt.axvline(male_population_description["gmean"], color='purple', label='M Geo Mean')
plt.legend()
plt.title('Population Description')
plt.xlabel('SMV')
plt.ylabel('#Agents')
# plt.show()


# Agents creation
Agents = []
for i in config.male_SMVs:
    Agents.append(Agent(gender='male', SMV=i, population=Agents))
for i in config.female_SMVs:
    Agents.append(Agent(gender='female', SMV=i, population=Agents))

for agent in Agents:
    agent.getPopulationObservation()

Agents[0].pickAction("explore")
Agents[1].pickAction("explore")
Agents[2].pickAction("explore")
Agents[0].pickAction("offerSex")
Agents[1].pickAction("offerSex")
Agents[2].pickAction("offerSex")
Agents[3].pickAction("acceptBestSexOffer")
