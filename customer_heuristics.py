def evaluate_customers(faces: list) -> [int, str]:
    """
    Evaluates customers based on their age and gender, finds the potentially most profitable one
    :param faces: list of faces
    :return: list of evaluated customers
    """
    age = 0
    gender = None
    # Heuristic for customer evaluation
    # TODO: Apply some real heuristic shit
    for face in faces:
        current_age = face.age
        if age < current_age < 70:
            age = current_age
            gender = face.gender
        else:
            continue
    return age, gender
