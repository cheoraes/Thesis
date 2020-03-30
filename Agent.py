import random
import json
import numpy as np
from names import get_first_name
import icons

from termcolor import colored, cprint


class Agent:

    def __init__(self, SMV, population, config):
        self.population = population
        self.config = config
        self.SMV = SMV
        self.focus = None
        self.sexOfferees = []
        self.observation = {
            "population": {},
            "inner": {},
            "focus": {},
            "bestOffer": {}
        }
        self.age = 0
        self.alive = True
        self.gender = self.config["gender"]
        self.selfAppraisal = self.config["self-appraisal"]
        self.lifeExpectancy = self.config["life expectancy"]
        self.name = get_first_name(gender=self.gender)
        self.episode_reward = 0
        self.total_reward = 0

        print(colored("Creation:", 'green'), self.personalData(self))

    def personalData(self, agent):
        gender_icon = icons.male if agent.gender == "male" else icons.female
        color = 'blue' if agent.gender == "male" else 'magenta'
        attributes = []

        return colored(agent.name + " ("+str(self.age)+") " + gender_icon + " " + str(agent.SMV), color, attrs=attributes)

    def showFocus(self):
        if self.focus is not None:
            print("\t\t\t", self.personalData(self), "focus on ", self.personalData(self.focus))
        else:
            print("\t\t\t", self.personalData(self), "No focus")

    def showSexOffereeList(self):
        print("\t\t\t", self.personalData(self), "Sex Offeree's list")
        if len(self.sexOfferees) > 0:
            self.sexOfferees.sort(key=lambda obj: obj.SMV, reverse=True)
            for sexOfferee in self.sexOfferees:
                print("\t\t\t\t ", icons.heart, self.personalData(sexOfferee))
        else:
            print("\t\t\t\t", icons.heart, "Empty")

    def getSexOffer(self, agent):
        color = 'cyan'
        attributes = ['bold']
        self.sexOfferees.append(agent)
        print("\t\t", self.personalData(self), colored("gets Sex Offer from ", color, attrs=attributes),
              self.personalData(agent))

    def toAge(self):

        self.age += 1
        self.total_reward += self.episode_reward
        print(icons.diamond,"toAge", self.personalData(self), "Episode Reward", self.episode_reward,"Total Reward", self.total_reward)
        self.episode_reward = 0


    # Observations
    def setPopulationObservation(self):
        # population observation
        print("*", colored("setPopulationObservation:", 'grey'), self.personalData(self))

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
        if len(self.sexOfferees) > 0:
            self.sexOfferees.sort(key=lambda obj: obj.SMV, reverse=True)
            self.observation["bestOffer"] = {
                "name": self.sexOfferees[0].name,
                "SMV": self.sexOfferees[0].SMV,
            }
        else:
            self.observation["bestOffer"] = {}

    def setObservation(self):
        self.setInnerObservation()
        self.setFocusObservation()
        self.setBestOfferObservation()
        attributes = ['bold']
        print(colored("\t\tPopulation ", "red", attrs=attributes), self.observation["population"])
        print(colored("\t\tInner ", "red", attrs=attributes), self.observation["inner"])
        print(colored("\t\tFocus ", "red", attrs=attributes), self.observation["focus"])
        print(colored("\t\tBest Offer ", "red", attrs=attributes), self.observation["bestOffer"])

    # ACTIONS
    def pickAction(self, action, target=None):
        print("\n*", self.personalData(self))
        print(colored("\tPre Action Observation", "grey", attrs=["concealed"]))
        self.setObservation()
        print(colored("\tAction ", "green", attrs=['bold']), action)

        self.episode_reward += int(self.config["reward_policy"][action])
        if action == 'showObservation':
            None
        if action == 'explore':
            self.explore()
        if action == 'offerSex':
            self.offerSex()
        if action == 'acceptBestSexOffer':
            self.acceptBestSexOffer()
        if action == 'setPopulationObservation':
            self.setPopulationObservation()
        if action == 'increaseSelfAppraisal':
            self.updateSelfAppraisal(1)
        if action == 'decreaseSelfAppraisal':
            self.updateSelfAppraisal(-1)
        self.showFocus()
        self.showSexOffereeList()

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
        print("\t\t", self.personalData(self), colored("runs investigation on:", color, attrs=attributes),
              self.personalData(self.focus))

    def offerSex(self):
        color = 'yellow'
        attributes = ['bold']
        if self.focus is not None:
            print("\t\t", self.personalData(self), colored("offers sex to", color, attrs=attributes),
                  self.personalData(self.focus))
            self.focus.getSexOffer(self);

    def acceptBestSexOffer(self):
        color = 'green'
        attributes = ['bold']
        if len(self.sexOfferees) > 0:
            self.sexOfferees.sort(key=lambda obj: obj.SMV, reverse=True)
            sexPartner = self.sexOfferees.pop(0)
            print("\t\t", self.personalData(self), colored("accept Best Sex Offer with ", color, attrs=attributes),
                  self.personalData(sexPartner))
            self.sexOfferees = []
