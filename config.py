import sys
import ast

# Population Distribution


initial_male_population_SMVs = (2,3,)
initial_female_population_SMVs = (1,2,3 )

generations = 1


# Data Resolution
resolution = {
    "ratio": 0.1,
    "std": 0.2,
    "mean": 0.2,
    "median": 0.2,
    "age": 1,
    "rewards memory buffer": 3,
    "reward": 5,
}

action_space = [
    "explore",
    "offerSex",
    "acceptBestSexOffer",
    #"increaseSelfAppraisal",
    #"decreaseSelfAppraisal",
    "setPopulationObservation",
]


observation_filter = {
    "population": {
        "ratio": {
            "active": False,
            "resolution": 0.1,
        },
        "mean": {
            "active": False,
            "resolution": 0.25,
        },
        "std": {
            "active": False,
            "resolution": 0.1,
        },
        "median": {
            "active": False,
            "resolution": 0.1,
        },
    },
    "inner": {
        "age": {
            "active": False,
            "resolution": 3,
        },
        "SMV": {
            "active": True,
            "resolution": 1,
        },
        "self-appraisal": {
            "active": False,
            "resolution": 1,
        },
        "reward": {
            "episode rewards": {
                "active": False,
                "buffer": 3,
                "resolution": 2,
            },
        }
    },
    "focus": {
        "age": {
            "active": False,
            "resolution": 0.1,
        },
        "SMV": {
            "active": True,
            "resolution": 1,
        },
    },
    "bestOffer": {
        "SMV": {
            "active": True,
            "resolution": 1,
        },
    }
}

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
    "life expectancy": 10,
    "self-appraisal": 5,
    "resolution": resolution,
    "reward policy": reward_policy,
    "action space": action_space,
    "observation filter": observation_filter,
}

# Female Configuration
female = {
    "gender": "female",
    "life expectancy": 10,
    "self-appraisal": 5,
    "resolution": resolution,
    "reward policy": reward_policy,
    "action space": action_space,
    "observation filter": observation_filter,
}
