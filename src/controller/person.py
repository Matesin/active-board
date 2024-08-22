# ----------------------CLASS----------------------
class Person:

    def __init__(self, age, gender, proximity: float, coords: tuple):
        """
        Person class
        :param age: Age of the person
        :param gender: Gender of the person
        :param proximity: Proximity to the camera
        """
        self.age = age
        self.gender = gender
        self.proximity = proximity
        self.coords = coords

    def __str__(self):
        return f'{self.gender} of age: {self.age}'

    def __repr__(self):
        return f'Person({self.gender}, {self.age}, {self.proximity}, {self.coords})'
