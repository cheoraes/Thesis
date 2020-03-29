import sys
import ast


#population distribution
#With arguments
if len(sys.argv)>1:
    intial_male_population_SMVs = ast.literal_eval(sys.argv[1])
    initial_female_population_SMVs = ast.literal_eval(sys.argv[2])
#with no arguments
else:
    intial_male_population_SMVs = (4,3,5)
    initial_female_population_SMVs = (4,1)

# Data resolution
resolution = {
    "ratio":0.1,
    "std":0.2,
    "mean":0.2,
    "median":0.2,
    "age":5,
}
#male configuration
male = {
    "gender": "male",
    "life expectancy":100,
    "self-appraisal":5,
    "resolution" : resolution,
}
#female configuration
female = {
    "gender": "female",
    "life expectancy": 100,
    "self-appraisal": 5,
    "resolution" : resolution,
}
