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
        self.selected_action = None
        self.episode_reward = 0
        self.rewards = []

        print(colored("Creation:", 'green'), self.personalData(self))

    def personalData(self, agent):
        gender_icon = icons.male if agent.gender == "male" else icons.female
        color = 'blue' if agent.gender == "male" else 'magenta'
        attributes = []

        return colored(agent.name + " (" + str(self.age) + ") " + gender_icon + str(agent.SMV), color,
                       attrs=attributes)

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
        self.rewards.append(self.episode_reward)
        print("\t", icons.diamond, "toAge", self.personalData(self), "Episode Reward", self.episode_reward,
              "Total Reward",
              sum(self.rewards))
        self.episode_reward = 0
        self.age += 1
        if self.age >= self.lifeExpectancy:
            self.alive = False
            print("\t\t", icons.cross, self.personalData(self), "is Dead", icons.cross)
            self.setObservation()

    # Observations
    def setPopulationObservation(self):
        # population observation

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
            "ratio": [male_ratio, female_ratio],
            "mean": [male_mean, female_mean],
            "std": [male_std, female_std],
            "median": [male_median, female_median],
        }

        print("\t\t", colored("setPopulationObservation:", 'grey'), self.personalData(self))
        print("\t\t\t", self.observation["population"])

    def setInnerObservation(self):
        self.observation["inner"] = {
            "age": self.age,
            "SMV": self.SMV,
            "self-appraisal": self.selfAppraisal,
            "reward": {
                "episode rewards": self.rewards,
            }
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

        print(colored("\t\tPopulation ", "red", attrs=['bold']), self.observation["population"])
        print(colored("\t\tInner ", "red", attrs=['bold']), self.observation["inner"])
        print(colored("\t\tFocus ", "red", attrs=['bold']), self.observation["focus"])
        print(colored("\t\tBest Offer ", "red", attrs=['bold']), self.observation["bestOffer"])
        self.filteredObservation()

    def filteredObservation(self):
        print("\t", icons.fisheye, colored("Filtered Observation", "grey", attrs=["concealed"]))
        header=[]
        obs = []

        def filterField(field, config, val, color="cyan"):
            obs = int(val / config["resolution"])
            print(colored("\t\t" + field, color, attrs=['bold']), "obs", obs, "| val", val, "| res",
                  config["resolution"])
            return obs

        #POPULATION
        #MALE FEMALE RATIO
        if self.config["observation filter"]["population"]["ratio"]["active"]:
            header.append("Male/female ratio")
            if "ratio" in self.observation["population"]:
                obs.append(filterField("Male ratio", self.config["observation filter"]["population"]["ratio"],
                                       self.observation["population"]["ratio"][0]))
            else:
                obs.append(None)
        #MALE FEMALE MEANS
        if self.config["observation filter"]["population"]["mean"]["active"]:
            header.append("Male mean")
            header.append("Female mean")

            if "mean" in self.observation["population"]:
                obs.append(filterField("Male mean", self.config["observation filter"]["population"]["mean"],
                                       self.observation["population"]["mean"][0]))
                obs.append(filterField("Female mean", self.config["observation filter"]["population"]["mean"],
                                       self.observation["population"]["mean"][1]))
            else:
                obs.append(None)
                obs.append(None)
        # MALE FEMALE STANDARD DEVIATION
        if self.config["observation filter"]["population"]["std"]["active"]:
            header.append("Male Std")
            header.append("Female Std")
            if "std" in self.observation["population"]:
                obs.append(filterField("Male std", self.config["observation filter"]["population"]["std"],
                                       self.observation["population"]["std"][0]))
                obs.append(filterField("Female std", self.config["observation filter"]["population"]["std"],
                                       self.observation["population"]["std"][1]))
            else:
                obs.append(None)
                obs.append(None)

        #INNER
        #SELF AGE
        if self.config["observation filter"]["inner"]["age"]["active"]:
            header.append("Self-Age")
            obs.append(filterField("Self Age", self.config["observation filter"]["inner"]["age"],
                                   self.observation["inner"]["age"], "magenta"))
        #SELF SMV
        if self.config["observation filter"]["inner"]["SMV"]["active"]:
            header.append("Self SMV")
            obs.append(filterField("Self SMV", self.config["observation filter"]["inner"]["SMV"],
                                   self.observation["inner"]["SMV"], "magenta"))
        #SELF-APPRAISAL
        if self.config["observation filter"]["inner"]["self-appraisal"]["active"]:
            header.append("Self-Appraisal")
            obs.append(filterField("self-appraisal", self.config["observation filter"]["inner"]["self-appraisal"],
                                   self.observation["inner"]["self-appraisal"], "magenta"))
        #REWARDS
        if self.config["observation filter"]["inner"]["reward"]["episode rewards"]["active"]:
            header.append("episode rewards")
            buffer = self.config["observation filter"]["inner"]["reward"]["episode rewards"]["buffer"]
            resolution = self.config["observation filter"]["inner"]["reward"]["episode rewards"]["resolution"]
            if len(self.rewards)>0:
                ep_rew_buffer_sum = sum(self.observation["inner"]["reward"]["episode rewards"][-buffer:])
                ep_rew_buffer_sum_low_resolution = ep_rew_buffer_sum/resolution
                obs.append(ep_rew_buffer_sum_low_resolution)
            else:
                obs.append(0)
        #FOCUS
        #FOCUS AGE
        if self.config["observation filter"]["focus"]["age"]["active"]:
            header.append("Focus Age")
            if "age" in self.observation["focus"]:
                obs.append(filterField("Focus Age", self.config["observation filter"]["focus"]["age"],
                                       self.observation["focus"]["age"], "magenta"))
            else:
                obs.append(None)
        #FOCUS SMV
        if self.config["observation filter"]["focus"]["SMV"]["active"]:
            header.append("Focus SMV")
            if "SMV" in self.observation["focus"]:
                obs.append(filterField("Focus SMV", self.config["observation filter"]["focus"]["SMV"],
                                       self.observation["focus"]["SMV"], "magenta"))
            else:
                obs.append(None)

        #BEST OFFER
        if self.config["observation filter"]["bestOffer"]["SMV"]["active"]:
            header.append("Best offer SMV")
            if "SMV" in self.observation["bestOffer"]:
                obs.append(filterField("bestOffer SMV", self.config["observation filter"]["bestOffer"]["SMV"],
                                       self.observation["bestOffer"]["SMV"], "yellow"))
            else:
                obs.append(None)
        #
        print("\n")
        print("Header", header)
        print("\n")
        print("OBS", obs)


        # #FILTER INNER OBSERVATION
        # if self.config["observation filter"]["inner"]["age"]["active"]:
        #     field = "Age"
        #     val = self.observation["inner"]["age"]
        #     res = self.config["observation filter"]["inner"]["age"]["resolution"]
        #     obs = int(val/res)
        #     print(colored("\t\t"+ field, "cyan", attrs=['bold']),"obs", obs, "| val", val, "| res" ,res)
        #
        # if self.config["observation filter"]["inner"]["SMV"]["active"]:
        #     field = "SMV"
        #     val = self.observation["inner"]["SMV"]
        #     res = self.config["observation filter"]["inner"]["SMV"]["resolution"]
        #     obs = int(val / res)
        #     print(colored("\t\t" + field, "cyan", attrs=['bold']), "obs", obs, "| val", val, "| res", res)

        # if self.config["observation filter"]["inner"]["SMV"][0]:
        #     SMV_observation = int(self.observation["inner"]["SMV"]/self.config["observation filter"]["inner"]["SMV"][1])
        #     print(colored("\t\tSMV observation:", "cyan", attrs=['bold']), SMV_observation,
        #           ", SMV:", self.observation["inner"]["SMV"],
        #           ", resolution:", self.config["observation filter"]["inner"]["SMV"][1],
        #           )
        # if self.config["observation filter"]["inner"]["self-appraisal"][0]:
        #     selfAppraisal_observation = int(self.observation["inner"]["self-appraisal"]/self.config["observation filter"]["inner"]["self-appraisal"][1])
        #     print(colored("\t\tSelf-appraisal obs:", "cyan", attrs=['bold']), selfAppraisal_observation,
        #           ", Self-appraisal:", self.observation["inner"]["self-appraisal"],
        #           ", resolution:", self.config["observation filter"]["inner"]["self-appraisal"][1],
        #           )
        # if self.config["observation filter"]["inner"]["reward"]["episode rewards"][0]:
        #     buffer = self.config["observation filter"]["inner"]["reward"]["episode rewards"][1]
        #     resolution =
        #     ep_rew_buffer_sum = sum(self.observation["inner"]["reward"]["episode rewards"][-buffer:])
        #     ep_rew_buffer_sum_low_res =
        #     episode_rewards_observation_buffer_sum = sum(self.observation["inner"]["reward"]["episode rewards"][-buffer:])
        #
        #
        #     episode_rewards_observation_buffer_sum_low_resolution = int(episode_rewards_observation_buffer_sum_obs/self.config["observation filter"]["inner"]["reward"]["episode rewards"][2])
        #     print(colored("\t\tEpisode rewards buffer sum observation:", "cyan", attrs=['bold']), episode_rewards_observation_buffer_sum_obs,
        #           ", Buffer:", self.observation["inner"]["self-appraisal"],
        #           ", resolution:", self.config["observation filter"]["inner"]["self-appraisal"][1],
        #
        #           )

    # ACTIONS
    def actionSpaceSample(self):
        if self.alive:
            self.selected_action = np.random.choice(self.config["action space"])
            self.pickAction(self.selected_action)

    def pickAction(self, action, target=None):
        print("\n", icons.man, self.personalData(self))
        print("\t", icons.fisheye, colored("Pre Action Observation", "grey", attrs=["concealed"]))
        self.setObservation()

        action_cost = int(self.config["reward policy"][action])
        self.episode_reward += action_cost
        print("\t", icons.spade, colored(action, "green", attrs=['bold']), "reward:", action_cost)
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
        print("\t\t", self.personalData(self), colored("update Self-appraisal", color, attrs=attributes),
              "(" + str(val) + ") ",
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
            reward_to_sexPartner = sexPartner.config["reward policy"]["sex"][self.SMV]
            reward_to_me = self.config["reward policy"]["sex"][sexPartner.SMV]
            sexPartner.episode_reward += reward_to_sexPartner
            self.episode_reward += reward_to_me
            print("\t\t", self.personalData(self), "reward:", reward_to_me,
                  colored("accept Best Sex Offer with ", color, attrs=attributes),
                  self.personalData(sexPartner), "reward", reward_to_sexPartner)
            self.sexOfferees = []
