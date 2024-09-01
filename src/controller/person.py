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
        self.product_threshold = None # Threshold for the number of products to be picked, based on the age group
        self.resolve_product_threshold()

    def __str__(self):
        return f'{self.gender} of age: {self.age}'

    def __repr__(self):
        return f'Person({self.gender}, {self.age}, {self.proximity}, {self.coords})'

    def resolve_product_threshold(self):
        if self.age < '(0-2)':
            self.product_threshold = 1
        elif self.age < '(4-6)':
            self.product_threshold = 2
        elif self.age < '(8-12)' or '(15-20)' or '(25-32)':
            self.product_threshold = 3
        else:
            self.product_threshold = 4
        return self.product_threshold
