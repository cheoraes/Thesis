import sys
import ast
import os
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

male_population_description = {
    "population": config.initial_male_population_SMVs,
    "count": len(config.initial_male_population_SMVs),
    "min": min(config.initial_male_population_SMVs),
    "max": max(config.initial_male_population_SMVs),
    "ratio": len(config.initial_male_population_SMVs) / (
            len(config.initial_female_population_SMVs) + len(config.initial_male_population_SMVs)),
    "mean": statistics.mean(config.initial_male_population_SMVs),
    "hmean": statistics.harmonic_mean(config.initial_male_population_SMVs),
    "gmean": statistics.geometric_mean(config.initial_male_population_SMVs),
}

female_population_description = {
    "population": config.initial_female_population_SMVs,
    "count": len(config.initial_female_population_SMVs),
    "min": min(config.initial_female_population_SMVs),
    "max": max(config.initial_female_population_SMVs),
    "ratio": len(config.initial_female_population_SMVs) / (
            len(config.initial_female_population_SMVs) + len(config.initial_male_population_SMVs)),
    "mean": statistics.mean(config.initial_female_population_SMVs),
    "hmean": statistics.harmonic_mean(config.initial_female_population_SMVs),
    "gmean": statistics.geometric_mean(config.initial_female_population_SMVs),
}

# print("\nPopulation Description")
# print("Males")
# print(json.dumps(male_population_description, indent=4))
# print("Female")
# print(json.dumps(female_population_description, indent=4))

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
main_log = []
id = 0
for i in config.initial_male_population_SMVs:
    Agents.append(Agent(SMV=i, id=id, population=Agents, config=config.male, DNAPolicy={}, main_log=main_log))
    Agents[-1].render()
    id += 1
for i in config.initial_female_population_SMVs:
    Agents.append(Agent(SMV=i, id=id, population=Agents, config=config.female, DNAPolicy={}, main_log=main_log))
    Agents[-1].render()
    id += 1

any_alive = True
while any_alive:
    any_alive = False
    for agent in Agents:
        agent.actionSpaceSample()
        agent.render()
    for agent in Agents:
        agent.toAge()
        agent.render()
        if agent.alive == True:
            any_alive = True


# print(json.dumps(main_log, indent=4))
'''    
# print("GENERATION")
#     print("GENERATION", generation)
# newAgents = getNewGeneration()
#     for i in range(config.male["life expectancy"]):
#         print("\n--Episode ", i, "------------------------------\n")
#         for agent in Agents:
#             agent.actionSpaceSample()
#         for agent in Agents:
#             agent.toAge()



#print(json.dumps(main_log, indent=4))




def getNextGeneration():
    def pickPartner(partners):
        lottery_correction = sum(partners[-1].rewards)-1
        if lottery_correction > -1:
            lottery_correction = -1

        #print("lottery_correction", lottery_correction)

        total_lottery_tickets = 0
        for candidate in partners:
            #print("corrected rewards", sum(candidate.rewards) - lottery_correction )
            total_lottery_tickets += (sum(candidate.rewards) - lottery_correction)
        #print(total_lottery_tickets)
        selector = np.random.randint(total_lottery_tickets)
        for candidate in partners:
            score = sum(candidate.rewards) - lottery_correction
            #print(candidate.personalData(candidate),score)
            if score >= selector:
                return candidate
            else:
                selector -= score
        return partners[0]

    def combineDNA(partnerA, partnerB):
        newDNA = partnerA.DNAPolicy
        for gen, phen in partnerB.DNAPolicy.items():
            if gen in newDNA:
                # print("gen", gen, "is present in both")
                if np.random.rand() > 0.5:
                    newDNA[gen] = phen
            else:
                newDNA[gen] = phen
            # print(gen, phen)

        return newDNA

    print('get Next Generation')
    male_agents = list(filter(lambda obj: obj.gender == "male", Agents))
    male_agents.sort(key=lambda obj: sum(obj.rewards), reverse=True)
    female_agents = list(filter(lambda obj: obj.gender == "female", Agents))
    female_agents.sort(key=lambda obj: sum(obj.rewards), reverse=True)

    # FATHERS
    for agent in male_agents:
        print(agent.personalData(agent), sum(agent.rewards))

    # MOTHERS
    for agent in female_agents:
        print(agent.personalData(agent), sum(agent.rewards))

    nextGeneration = []
    print("----MALE GENERATION")
    for i in config.initial_male_population_SMVs:
        male = pickPartner(male_agents)
        print("partnerA", male.personalData(male))
        female = pickPartner(female_agents)
        print("partnerB", female.personalData(female))
        newDNA = combineDNA(male, female)
        nextGeneration.append(Agent(SMV=i, population=Agents, config=config.male, DNAPolicy=newDNA))
    print("----FEMALE GENERATION")
    for i in config.initial_female_population_SMVs:
        male = pickPartner(male_agents)
        print("partnerA", male.personalData(male))
        female = pickPartner(female_agents)
        print("partnerB", female.personalData(female))
        newDNA = combineDNA(male, female)
        nextGeneration.append(Agent(SMV=i, population=Agents, config=config.female, DNAPolicy=newDNA))



    return nextGeneration


generations = 50
for iGen in range(generations):
    print("\n---Generation", iGen)
    for i in range(config.male["life expectancy"]):
        print("\n--Episode ", i, "------------------------------\n")
        for agent in Agents:
            agent.actionSpaceSample()
        for agent in Agents:
            agent.toAge()
    print("\n-------END GENERATION", iGen)
    Agents = getNextGeneration()

for gen, phen in Agents[0].DNAPolicy.items():
    print(gen,phen)
# Agents[0].pickAction("explore")
# Agents[1].pickAction("explore")
# Agents[0].pickAction("offerSex")
# Agents[1].pickAction("offerSex")
# Agents[2].pickAction("acceptBestSexOffer")

'''
# for i in range(config.male["life expectancy"]):
#     print("\n--Episode ", i, "------------------------------\n")
#     for agent in Agents:
#         agent.actionSpaceSample()
#     for agent in Agents:
#         agent.toAge()

print("\n--END OF SEASON ", i, "------------------------------\n")


def getNewGeneration():
    print("GET NEXT GENERATION")

    def lottery(Agents, male_lottery_range, min):
        selector = np.random.randint(male_lottery_range)
        for agent in Agents:
            score = sum(agent.rewards) - min
            if score >= selector:
                return agent
            else:
                selector -= score

    def combineDNA(male, female):
        newDNA = male.DNAPolicy
        # for gen, phen in male.DNAPolicy.items():
        # print(gen, phen)
        # print("----------")
        for gen, phen in female.DNAPolicy.items():
            if gen in newDNA:
                # print("gen", gen, "is present in both")
                if np.random.rand() > 0.5:
                    newDNA[gen] = phen
            else:
                newDNA[gen] = phen
            # print(gen, phen)

        return newDNA

    print("\nPARTNER DNA SELECTION ", "------------------------------\n")
    # print("\n--males ",  "------------------------------\n")
    # male filtering
    male_agents = list(filter(lambda obj: obj.gender == "male", Agents))
    male_agents.sort(key=lambda obj: sum(obj.rewards), reverse=True)

    female_agents = list(filter(lambda obj: obj.gender == "female", Agents))
    female_agents.sort(key=lambda obj: sum(obj.rewards), reverse=True)

    for agent in male_agents:
        print(agent.personalData(agent), sum(agent.rewards))

    for agent in female_agents:
        print(agent.personalData(agent), sum(agent.rewards))

    male_minimun_reward = sum(male_agents[-1].rewards)
    female_minimun_reward = sum(female_agents[-1].rewards)
    # print("min",male_minimun_reward)
    male_lottery_range = 0
    female_lottery_range = 0
    # for agent in male_agents:
    #     male_lottery_range += sum(agent.rewards)-male_minimun_reward
    # for agent in female_agents:
    #     female_lottery_range += sum(agent.rewards)-female_minimun_reward
    # print ("male_lottery_range",male_lottery_range)
    # for agent in male_agents:
    # print(agent.personalData(agent), sum(agent.rewards)-male_minimun_reward)

    NewAgents = []

    for i in config.initial_male_population_SMVs:
        male_partner = lottery(male_agents, male_lottery_range, male_minimun_reward)
        # print("pick a male_partner",male_partner.personalData(male_partner),sum(male_partner.rewards))
        female_partner = lottery(female_agents, female_lottery_range, female_minimun_reward)
        # print("pick a female_partner",female_partner.personalData(female_partner),sum(female_partner.rewards))
        newDNA = combineDNA(male_partner, female_partner)

        NewAgents.append(Agent(SMV=i, population=Agents, config=config.male, DNAPolicy=newDNA))
        # print("----------")
    for i in config.initial_female_population_SMVs:
        male_partner = lottery(male_agents, male_lottery_range, male_minimun_reward)
        # print("pick a male_partner",male_partner.personalData(male_partner),sum(male_partner.rewards))
        female_partner = lottery(female_agents, female_lottery_range, female_minimun_reward)
        # print("pick a female_partner",female_partner.personalData(female_partner),sum(female_partner.rewards))
        newDNA = combineDNA(male_partner, female_partner)

        NewAgents.append(Agent(SMV=i, population=Agents, config=config.female, DNAPolicy=newDNA))
        print("----------")

    return NewAgents

    # total = sum(A.values())
    # # print("total",total)
    # selector = random.uniform(0, total)
    #
    # for action, score in options.items():
    #     # print(action,score,selector)
    #     if selector < score:
    #         return action
    #     else:
    #         selector -= score
    # return "explore"


# for agent in Agents:
#     print(agent.personalData(agent), sum(agent.rewards))

generations = 10
# for generation in range(generations):
# print("GENERATION")
#     print("GENERATION", generation)
# newAgents = getNewGeneration()
#     for i in range(config.male["life expectancy"]):
#         print("\n--Episode ", i, "------------------------------\n")
#         for agent in Agents:
#             agent.actionSpaceSample()
#         for agent in Agents:
#             agent.toAge()


'''
def execute(cmd):
    command = cmd.split(' ')
    if command[0] == 'clear':
        print (command[0])
        os.system('cls' if os.name == 'nt' else 'clear')
    if command[0] in (
            'explore',
            'offerSex',
            'acceptBestSexOffer',
            'increaseSelfAppraisal',
            'decreaseSelfAppraisal',
            'showObservation',
            'setPopulationObservation',
    ):
        Agents[int(command[1])].pickAction(command[0])
while True:
    print('Input command (use ? for help)')
    command = input()
    execute(command)
'''
