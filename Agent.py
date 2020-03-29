import random
import json
import numpy as np
from names import get_first_name

from termcolor import colored, cprint


class Agent:
    focus = None
    sexOfferors = []
    observation = {
        "population": {},
        "inner": {},
        "focus": {},
        "bestOffer": {}
    }
    age = 0

    alive = True

    def __init__(self, SMV, population, config):
        self.population = population
        self.config = config

        self.SMV = SMV
        self.gender = config["gender"]
        self.selfAppraisal = config["self-appraisal"]
        self.lifeExpectancy = config["life expectancy"]

        self.name = get_first_name(gender=self.gender)
        # print(json.dumps(self.male_population_description, indent=4))
        print(colored("Creation:", 'green'), self.personalData(self))

    def personalData(self, agent):
        color = 'blue' if agent.gender == "male" else 'magenta'
        attributes = []
        return colored(agent.name + " " + agent.gender + " " + str(agent.SMV), color, attrs=attributes)

    def setPopulationObservation(self):
        # population observation
        print(colored("getPopulationObservation:", 'grey'), self.personalData(self))

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
        self.observation["population"] = {
            "ratio": [int(male_ratio / self.config["resolution"]["ratio"]),
                      int(female_ratio / self.config["resolution"]["ratio"])],
            "mean": [int(male_mean / self.config["resolution"]["mean"]),
                     int(female_mean / self.config["resolution"]["mean"])],
            "std": [int(male_std / self.config["resolution"]["std"]),
                    int(female_std / self.config["resolution"]["std"])],
            "median": [int(male_median / self.config["resolution"]["median"]),
                       int(female_median / self.config["resolution"]["median"])],
        }

        # print( self.population_observation )
        # print(json.dumps(self.population_observation, indent=4))

    def setInnerObservation(self):
        self.observation["inner"] = {
            "age": int(self.age / self.config["resolution"]["age"]),
            "self-appraisal": self.selfAppraisal
        }

    def setFocusObservation(self):
        if self.focus is not None:
            self.observation["focus"] = {
                "age": int(self.focus.age / self.focus.config["resolution"]["age"]),
                "SMV": self.focus.SMV
            }
        else:
            self.observation["focus"] = {}

    def setBestOfferObservation(self):
        if len(self.sexOfferors) > 0:
            self.sexOfferors.sort(key=lambda obj: obj.SMV, reverse=True)
            self.observation["bestOffer"] = self.sexOfferors[0].SMV
        else:
            self.observation["bestOffer"] = {}

    def setObservation(self):
        self.setInnerObservation()
        self.setFocusObservation()
        self.setBestOfferObservation()
        print(colored("Observation", "white", attrs=['reverse']), self.personalData(self))
        attributes = ['bold']
        print(colored("\tPopulation ", "red", attrs=attributes), self.observation["population"])
        print(colored("\tInner ", "blue", attrs=attributes), self.observation["inner"])
        print(colored("\tFocus ", "green", attrs=attributes), self.observation["focus"])
        print(colored("\tBest Offer ", "yellow", attrs=attributes), self.observation["bestOffer"])
        # print(json.dumps(self.observation, indent=2))

    # ACTIONS
    def pickAction(self, action, target=None):
        self.setObservation()
        if action == 'showObservation':
            None
        if action == 'explore':
            self.explore()
        if action == 'offerSex':
            self.offerSex()
        if action == 'acceptBestSexOffer':
            self.acceptBestSexOffer()
        if action == 'getPopulationObservation':
            self.setPopulationObservation()
        if action == 'increaseSelfAppraisal':
            self.updateSelfAppraisal(1)
        if action == 'decreaseSelfAppraisal':
            self.updateSelfAppraisal(-1)

    def updateSelfAppraisal(self, val):
        color = 'grey'
        attributes = ['bold']
        old = self.selfAppraisal
        self.selfAppraisal += val
        if self.selfAppraisal < 0: self.selfAppraisal = 0
        print(self.personalData(self), colored("update Self-appraisal", color, attrs=attributes), "(" + str(val) + ") ",
              old, "-->", self.selfAppraisal)

    def explore(self):
        color = 'grey'
        attributes = ['bold']
        candidates = list(filter(lambda obj: obj.gender != self.gender, self.population))
        self.focus = random.choice(candidates)
        print("*", self.personalData(self), colored("runs investigation on:", color, attrs=attributes),
              self.personalData(self.focus))

    def offerSex(self):
        color = 'yellow'
        attributes = ['bold']
        if self.focus is not None:
            print("*", self.personalData(self), colored("offers sex to", color, attrs=attributes),
                  self.personalData(self.focus))
            self.focus.getSexOffer(self);

    def getSexOffer(self, agent):
        color = 'cyan'
        attributes = ['bold']
        self.sexOfferors.append(agent)
        print(self.personalData(self), colored("gets Sex Offer from ", color, attrs=attributes),
              self.personalData(agent))
        print("\tSex Offerors' list")
        for hunter in self.sexOfferors:
            print("\t\t" + self.personalData(hunter))

    def acceptBestSexOffer(self):
        color = 'green'
        attributes = ['bold']
        if len(self.sexOfferors) > 0:
            self.sexOfferors.sort(key=lambda obj: obj.SMV, reverse=True)
            sexPartner = self.sexOfferors.pop(0)
            print(self.personalData(self), colored("accept Best Sex Offer with ", color, attrs=attributes),
                  self.personalData(sexPartner))
            self.sexOfferors = []
            print("\tSex Offerors' list empty")
