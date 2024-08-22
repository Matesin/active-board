from controller.person import Person
import random

IDEAL_AGE = 35


def evaluate_faces(faces: list[Person]) -> [int, str]:
    """
    Evaluates customers based on their age and gender, finds the potentially most profitable one
    :param faces: list of faces
    :return: list of evaluated customers
    """

    # Heuristic for customer evaluation
    # TODO: Apply some real heuristic shit
    # picked_person = Person(0, "Unknown", 0, (0, 0))
    index = random.randint(0, len(faces) - 1)
    picked_person = faces[index]
    return picked_person.age, picked_person.gender


