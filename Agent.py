import random
from names import get_first_name

from termcolor import colored, cprint

class Agent:
    prey = None
    def __init__(self, gender, SMV):
        self.gender = gender
        self.SMV = SMV
        self.name = get_first_name(gender=self.gender)
        print(colored("Creation:", 'green'), self.personal_data(self))


    def personal_data(self,agent):
        color = 'blue' if agent.gender == "male" else 'magenta'
        attributes = []

        return colored( agent.name + " " + agent.gender + " " + str(agent.SMV), color, attrs = attributes)



    #ACTIONS

    def explore(self, population):
        color='grey'
        attributes=['reverse']
        candidates = list(filter(lambda obj: obj.gender != self.gender, population))
        self.prey = random.choice(candidates)
        print(self.personal_data(self), colored("runs investigation on Prey:",color, attrs = attributes), self.personal_data(self.prey))
        self.offerSex()

    def offerSex(self):
        color = 'yellow'
        attributes = ['bold']
        if self.prey != None :
            print(self.personal_data(self), colored("offers sex to ",color,attrs = attributes), self.personal_data(self.prey))