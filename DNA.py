import config
import numpy as np
from Agent import Agent
def GeneticRecombination(Agents):



    def fitnessCalculation(tested_agents):
        tested_agents.sort(key=lambda obj: sum(obj.rewards), reverse=True)
        min_reward = sum(tested_agents[-1].rewards)
        for tested_agent in tested_agents:
            tested_agent.fitness = sum(tested_agent.rewards) + 1
            if min_reward < 0:
                tested_agent.fitness -= min_reward
            tested_agent.fitness = int(pow(tested_agent.fitness, config.fitnessPow))


    def geneticLottery(lottery_players):
        total_lottery_tickets = 0
        for player in lottery_players:
            total_lottery_tickets += player.fitness
        winner_ticket = np.random.randint(total_lottery_tickets)
        for player in lottery_players:
            if player.fitness >= winner_ticket:
                return player
            else:
                winner_ticket -= player.fitness



        print(total_lottery_tickets,winner_ticket)
        return "hola"
    male_agents= list(filter(lambda obj: obj.gender == "male", Agents))
    fitnessCalculation(male_agents)
    female_agents= list(filter(lambda obj: obj.gender == "female", Agents))
    fitnessCalculation(female_agents)

    print("GeneticRecombination")
    for agent in Agents:
        print(agent.personalData(agent),"fitness:", agent.fitness,)

    if config.DNACombineMethod == "best score":
        print("best score")
        for i in range(20):
            male = geneticLottery(male_agents)
            female = geneticLottery(female_agents)
            print("winner male:", male.personalData(male))
            print("winner female:", female.personalData(female))
            #female = pickAgent(female_agents)









    return Agents[-1].DNAPolicy