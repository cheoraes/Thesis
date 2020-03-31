import sys
import ast

# Population Distribution


initial_male_population_SMVs = (3, 4,)
initial_female_population_SMVs = (4, 2,)

# Data Resolution
resolution = {
    "ratio": 0.1,
    "std": 0.2,
    "mean": 0.2,
    "median": 0.2,
    "age": 1,
    "reward memory": 3,
    "reward": 5,
}

action_space = [
    "explore",
    "offerSex",
    "acceptBestSexOffer",
    "increaseSelfAppraisal",
    "decreaseSelfAppraisal",
    "setPopulationObservation",
]

# Reward Policy
reward_policy = {
    "explore": -1,
    "offerSex": -1,
    "acceptBestSexOffer": -1,
    "increaseSelfAppraisal": -1,
    "decreaseSelfAppraisal": -1,
    "setPopulationObservation": -3,
    "showObservation": 0,
    "sex": (0, 10, 20, 30, 40, 50)

}

# Male Cconfiguration
male = {
    "gender": "male",
    "life expectancy": 5,
    "self-appraisal": 5,
    "resolution": resolution,
    "reward policy": reward_policy,
    "action space": action_space,
}

# Female Configuration
female = {
    "gender": "female",
    "life expectancy": 5,
    "self-appraisal": 5,
    "resolution": resolution,
    "reward policy": reward_policy,
    "action space": action_space,
}
