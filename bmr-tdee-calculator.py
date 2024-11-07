###import from modules
from enum import Enum
from typing import Literal, Union, Optional
from dataclasses import dataclass

### setting up class structures for the subsequent 'User' Class 
class Sex(Enum):
    M = "Male"
    F = "Female"
@dataclass
class Height:
    value: float
    unit: Literal["cm", "in"]

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Height must be positive")
@dataclass
class Weight:
    value: float
    unit: Literal["kg", "lbs"]

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Weight must be positive")
class ActivityLevel(Enum):
    sedentary = {
        "multiplier": 1.2,
        "description": "Little or no exercise, desk job (0 - 2 workouts/week)"
    }
    light = {
        "multiplier": 1.375,
        "description": "Light exercise/sports 1-3 days/week"
    }
    moderate = {
        "multiplier": 1.55,
        "description": "Moderate exercise/sports 3-5 days/week"
    }
    very = {
        "multiplier": 1.725,
        "description": "Hard exercise/sports 6-7 days/week"
    }
    extremely = {
        "multiplier": 1.9,
        "description": "Hard daily exercise/sports & physical job or training twice per day"
    }

    @property
    def multiplier(self) -> float:
        return self.value["multiplier"]
    
    @property
    def description(self) -> str:
        return self.value["description"]

class User:
    def __init__(
            self, 
            name: str, 
            age: int, 
            sex: Sex, 
            height: Height, 
            weight: Weight, 
            activity_level: Optional[ActivityLevel] = None,
            BMR = None, 
            TDEE_estimate = None
            ):
        
        #check if activity_level is provided and ensure it is an instance of Activitylevel enum
        if activity_level is not None and not isinstance(activity_level, ActivityLevel):
            raise ValueError(f"activity_level must be an ActivityLevel enum value or None, got {type(activity_level)}")
        
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height
        self.weight = weight
        self.activity_level = activity_level
        self.BMR = BMR
        self.TDEE_estimate = TDEE_estimate

    # calculate BMR & update User.BMR
    def calculate_BMR(self):
        if self.sex == Sex.M:
            BMR = 10 * self.weight.value + (6.25 * self.height.value) - (5 * self.age) + 5
        else: 
            BMR = 10 * self.weight.value + (6.25 * self.height.value) - (5 * self.age) - 161
        self.BMR = BMR
        return print(f"\n BMR for {self.name}: {self.BMR} Kcal\n")
    
    #
    def calculate_TDEE(self):
        ### TDEE = BMR + NEAT + EAT + TEF 
        # BMR = Basal Metabolic Rate (energy expenditure for cell division, protein synthesis etc.)
        # NEAT = Non-Exercise Activity Thermogenesis (energy expenditure for walking, talking etc.)
        # EAT = Exercise Activity Thermogenesis (energy expenditure for deliberate exercise)
        # TEF  = Thermic Effect of food (energy expenditure to digest food)
        pass
    
    def estimate_TDEE(self):
        if self.BMR is None:
            raise ValueError("BMR not yet defined")
        if self.activity_level is None:
            raise ValueError("Activity level must be set before estimating TDEE")
        else:
            self.TDEE_estimate = self.BMR * self.activity_level.multiplier
            return print(f"\nEstimated TDEE for {self.name}: {self.TDEE_estimate} Kcal\n")

### TESTING
Seb = User("Seb", 27, Sex.M, Height(171, "cm"), Weight(74, "kg"), ActivityLevel.sedentary)
Seb.calculate_BMR()
Seb.estimate_TDEE()