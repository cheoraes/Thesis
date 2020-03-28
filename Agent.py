import random
import json
from names import get_first_name

from termcolor import colored, cprint

class Agent:
    prey = None
    hunters = []
    def __init__(self, gender, SMV, population):
        self.male_population_description = population[0]
        self.female_population_description = population[1]
        self.gender = gender
        self.SMV = SMV
        self.name = get_first_name(gender=self.gender)
        #print(json.dumps(self.male_population_description, indent=4))
        print(colored("Creation:", 'green'), self.personal_data(self))


    def personal_data(self, agent):
        color = 'blue' if agent.gender == "male" else 'magenta'
        attributes = []
        return colored(agent.name + " " + agent.gender + " " + str(agent.SMV), color, attrs=attributes)



    #ACTIONS

    def explore(self, population):
        color='grey'
        attributes=['bold']
        candidates = list(filter(lambda obj: obj.gender != self.gender, population))
        self.prey = random.choice(candidates)
        print(self.personal_data(self), colored("runs investigation on Prey:",color, attrs=attributes), self.personal_data(self.prey))


    def offerSex(self):
        color = 'yellow'
        attributes = ['bold']
        if self.prey is not None:
            self.prey.getSexOffer(self);
            print(self.personal_data(self), colored("offers sex to ",color,attrs=attributes), self.personal_data(self.prey))

    def getSexOffer(self,agent):
        color = 'cyan'
        attributes = ['bold']
        self.hunters.append(agent)
        print(self.personal_data(self), colored("gets Sex Offer from ", color, attrs=attributes),
              self.personal_data(agent))
        print("\thunter list")
        for hunter in self.hunters:
            print("\t\t" + self.personal_data(hunter))

    def acceptBestSexOffer(self):
        color = 'green'
        attributes = ['bold']
        if len(self.hunters) > 0:
            self.hunters.sort(key=lambda obj: obj.SMV, reverse=True)
            sexpartner = self.hunters.pop(0)
            print(self.personal_data(self),colored("accept Best Sex Offer with ",color,attrs=attributes), self.personal_data(sexpartner) )
            self.hunters = []
            print("\thunter list empty")



