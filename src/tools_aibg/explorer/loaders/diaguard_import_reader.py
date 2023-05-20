import re
import pandas as pd
from typing import TextIO


class DiaguardImportReader():
    """Reads Diaguard CSV backup file into a dataframe for Explorer objects"""
    def __init__(self, f: TextIO):
        """Reads a diaguard backup csv file and creates the entry dataframe"""
        self.lines = [line.strip() for line in f.readlines()]
        self.foods = {}  # format: `food: carbs (g) per 100g`
        self.entries = []
        self.process_backup()
        self.df = pd.DataFrame(self.entries)
        self.df['date'] = pd.to_datetime(self.df['date'])

    def format_line(self, line):
        """Remove double quotes and semicolons and convert to list"""
        def clear_chars(s): return re.sub(r"^\"|\"$", "", s)
        line = list(map(clear_chars, line.split(';')))
        return line[0], line[1:]

    def process_food(self, food_info):
        """Format food name and save it into foods dictionary"""
        food_name = food_info[0].lower()
        self.foods[food_name] = float(food_info[-1])

    def process_entry(self, content, i):
        """Process a single entry starting at given index"""
        date, comments = content[:2]
        glucose, activity, hba1c = None, 0, None
        insulin = (0,)*3  # bolus, correction, basal
        meal = {}  # food: grams of carbs
        tags = []
        while i < len(self.lines):
            field, values = self.format_line(self.lines[i])
            if field == "measurement":
                category = values[0]
                if category == "bloodsugar":
                    glucose = int(float(values[1]))
                elif category == "insulin":
                    insulin = tuple(map(lambda x: int(float(x)), values[1:4]))
                elif category == "meal":
                    meal["carbs"] = float(values[1])
                elif category == "activity":
                    activity = float(values[1])
                elif category == "hba1c":
                    hba1c = float(values[1])
            elif field == "foodEaten":
                food_eaten = values[0].lower()
                food_weight = float(values[1])
                carb_ratio = self.foods[food_eaten]/100
                meal[food_eaten] = food_weight * carb_ratio
            elif field == "entryTag":
                tags.append(values[0])
            else:
                break
            i += 1
        self.entries.append({
            "date": date,
            "glucose": glucose,
            "bolus_insulin": insulin[0],
            "correction_insulin": insulin[1],
            "fast_insulin": sum(insulin[:2]),
            "basal_insulin": insulin[2],
            "total_insulin": sum(insulin),
            "activity": activity,
            "hba1c": hba1c,
            "meal": meal,
            "carbs": sum(meal.values()),
            "tags": tags,
            "comments": comments,
        })
        return i

    def process_backup(self):
        """Process the whole CSV backup file"""
        i = 0
        while i < len(self.lines):
            name, content = self.format_line(self.lines[i])
            if name == "food":
                self.process_food(content)
                i = i+1
            elif name == "entry":
                i = self.process_entry(content, i+1)
            else:
                i = i+1
