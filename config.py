import sys
import ast

# Population Distribution


intial_male_population_SMVs = (3, 4)
initial_female_population_SMVs = (4,)

# Data Resolution
resolution = {
    "ratio": 0.1,
    "std": 0.2,
    "mean": 0.2,
    "median": 0.2,
    "age": 5,
}

# Reward Policy
reward_policy = {
    "explore": -1,
    "offerSex": -1,
    "acceptBestSexOffer": 0,
    "increaseSelfAppraisal": 0,
    "decreaseSelfAppraisal": 0,
    "setPopulationObservation": -3,
}

# Male Cconfiguration
male = {
    "gender": "male",
    "life expectancy": 100,
    "self-appraisal": 5,
    "resolution": resolution,
    "reward_policy": reward_policy,
    "parental_care": 2
}

# Female Configuration
female = {
    "gender": "female",
    "life expectancy": 100,
    "self-appraisal": 5,
    "resolution": resolution,
    "reward_policy": reward_policy,
    "parental_care": 6
}
