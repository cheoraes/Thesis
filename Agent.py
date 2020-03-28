from names import get_full_name
class Agent:
    def __init__(self, gender, SMV):
        self.gender = gender
        self.SMV = SMV
        self.name = get_full_name(gender=self.gender)
        print("CREATION Agent:", "\t| SMV:", self.SMV, "\t| gender:", self.gender, "\t|name:", self.name)