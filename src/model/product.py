class ProductProperties:
    """
    Class that holds the properties of a product
    """

    def __init__(self, category, gender, age, customer_disclaimer: str, image: str):
        self.category = category
        self.gender = gender
        self.age = age
        self.disclaimer = customer_disclaimer
        self.image = image

    def __str__(self):
        return (f"Product falls under category {self.category}, "
                f"is supposed to be used by the gender {self.gender}, "
                f"of age {self.age}")


class Product:
    """
    Class that represents the product entity, separated from properties for future GUI implementation
    """

    def __init__(self, name, properties: ProductProperties):
        self.name = name
        self.properties = properties

    def __str__(self):
        return f"{self.name}\n\t{self.properties}"
