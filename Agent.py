import random
import json
import numpy as np
from names import get_first_name

from termcolor import colored, cprint


class Agent:
    prey = None
    hunters = []

    def __init__(self, gender, SMV, population):
        self.population = population
        self.population_observation = None
        self.gender = gender
        self.SMV = SMV
        self.name = get_first_name(gender=self.gender)
        # print(json.dumps(self.male_population_description, indent=4))
        print(colored("Creation:", 'green'), self.personalData(self))

    def personalData(self, agent):
        color = 'blue' if agent.gender == "male" else 'magenta'
        attributes = []
        return colored(agent.name + " " + agent.gender + " " + str(agent.SMV), color, attrs=attributes)

    def getPopulationObservation(self):
        # population observation
        print(colored("getPopulationObservation:", 'grey'), self.personalData(self))
        step_size = 0.25
        ratio_step_size = 0.1
        males = list(filter(lambda obj: obj.gender == 'male', self.population))
        females = list(filter(lambda obj: obj.gender == 'female', self.population))

        male_ratio = len(males) / len(self.population)
        female_ratio = len(females) / len(self.population)

        male_mean = np.mean([a.SMV for a in males])
        female_mean = np.mean([a.SMV for a in females])

        male_std = np.std([a.SMV for a in males])
        female_std = np.std([a.SMV for a in females])

        male_median = np.median([a.SMV for a in males])
        female_median = np.median([a.SMV for a in females])
        male_mode = 0
        # print("male MEAN", male_mean, "STD", male_std," ratio", male_ratio, "median",male_median)
        # print("female MEAN", female_mean, "STD", female_std, " ratio", female_ratio, "median",female_median)
        self.population_observation = {
            "ratio": [int(male_ratio / ratio_step_size), int(female_ratio / ratio_step_size)],
            "mean": [int(male_mean / step_size), int(female_mean / step_size)],
            "std": [int(male_std / step_size), int(female_std / step_size)],
            "median": [int(male_median / step_size), int(female_median / step_size)],
        }

        print(json.dumps(self.population_observation, indent=4))

    # ACTIONS
    def pickAction(self, action, target=None):
        if action == 'explore':
            self.explore()
        if action == 'offerSex':
            self.offerSex()
        if action == 'acceptBestSexOffer':
            self.acceptBestSexOffer()
        if action == 'getPopulationObservation':
            self.getPopulationObservation()

    def explore(self):
        color = 'grey'
        attributes = ['bold']
        candidates = list(filter(lambda obj: obj.gender != self.gender, self.population))
        self.prey = random.choice(candidates)
        print(self.personalData(self), colored("runs investigation on Prey:", color, attrs=attributes),
              self.personalData(self.prey))

    def offerSex(self):
        color = 'yellow'
        attributes = ['bold']
        if self.prey is not None:
            self.prey.getSexOffer(self);
            print(self.personalData(self), colored("offers sex to ", color, attrs=attributes),
                  self.personalData(self.prey))

    def getSexOffer(self, agent):
        color = 'cyan'
        attributes = ['bold']
        self.hunters.append(agent)
        print(self.personalData(self), colored("gets Sex Offer from ", color, attrs=attributes),
              self.personalData(agent))
        print("\thunter list")
        for hunter in self.hunters:
            print("\t\t" + self.personalData(hunter))

    def acceptBestSexOffer(self):
        color = 'green'
        attributes = ['bold']
        if len(self.hunters) > 0:
            self.hunters.sort(key=lambda obj: obj.SMV, reverse=True)
            sexpartner = self.hunters.pop(0)
            print(self.personalData(self), colored("accept Best Sex Offer with ", color, attrs=attributes),
                  self.personalData(sexpartner))
            self.hunters = []
            print("\thunter list empty")
