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



#Arguments
male_SMVs = ast.literal_eval(sys.argv[1])
female_SMVs = ast.literal_eval(sys.argv[2])



#Population Description
print("\nPopulation Description")
print("Males")
male_population_description = {
    "population":male_SMVs,
    "count":len(male_SMVs),
    "min":min(male_SMVs),
    "max":max(male_SMVs),
    "ratio":len(male_SMVs)/(len(female_SMVs)+len(male_SMVs)),
    "mean":statistics.mean(male_SMVs),
    "hmean":statistics.harmonic_mean(male_SMVs),
    "gmean":statistics.geometric_mean(male_SMVs),
}

print(json.dumps(male_population_description, indent=4))

print("Female")
female_population_description = {
    "population":female_SMVs,
    "count":len(female_SMVs),
    "min":min(female_SMVs),
    "max":max(female_SMVs),
    "ratio":len(female_SMVs)/(len(female_SMVs)+len(male_SMVs)),
    "mean":statistics.mean(female_SMVs),
    "hmean":statistics.harmonic_mean(female_SMVs),
    "gmean":statistics.geometric_mean(female_SMVs),
}
print(json.dumps(female_population_description, indent=4))



bins = np.arange(min(male_population_description["min"], female_population_description["min"]), max(male_population_description["max"], female_population_description["max"])+1, 0.5).tolist()
plt.hist([male_population_description["population"],
         female_population_description["population"]],
         bins=bins, color=['blue', 'pink'], edgecolor='black', rwidth=1.0,
         label=["Male ("+str(male_population_description["count"]) +
                ") ratio: " + str(round(male_population_description["ratio"], 2)),
                "Female ("+str(female_population_description["count"]) +
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
#plt.show()


#Agents creation
Agents = []
for i in male_SMVs:
    Agents.append(Agent(gender='male', SMV=i, population = [male_population_description,female_population_description]))
for i in female_SMVs:
    Agents.append(Agent(gender='female', SMV=i, population = [male_population_description,female_population_description]))


Agents[0].explore(Agents)
Agents[1].explore(Agents)
Agents[2].explore(Agents)
Agents[0].offerSex()
Agents[1].offerSex()
Agents[2].offerSex()
Agents[3].acceptBestSexOffer()