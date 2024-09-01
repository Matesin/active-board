from controller.person import Person
import random

IDEAL_AGE = 35


def evaluate_faces(faces: list[Person]) -> Person:
    """
    Evaluates customers based on their age and gender, finds the potentially most profitable one
    :param faces: list of faces
    :return: list of evaluated customers
    """
    if faces is None or len(faces) == 0:
        return None
    # Heuristic for customer evaluation
    # TODO: Apply some real heuristic shit
    # picked_person = Person(0, "Unknown", 0, (0, 0))
    index = random.randint(0, len(faces) - 1)
    picked_person = faces[index]
    return picked_person


def average_customers(customers: list[Person]) -> Person:
    picked_customer = None
    if len(customers) > 10:
        picked_customer = most_frequent(customers)
    return picked_customer


def most_frequent(source: list[any]) -> any:
    sorted_dict = {}
    count, item = 0, ''
    for i in reversed(source):
        sorted_dict[item] = sorted_dict.get(i, 0) + 1
        if sorted_dict[item] >= count:
            count, item = sorted_dict[i], i
    return item




