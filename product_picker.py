import json
from typing import Dict, Any


class ProductProperties:
    """
    Class that holds the properties of a product
    """

    def __init__(self, category, gender, age):
        self.category = category
        self.gender = gender
        self.age = age

    def __str__(self):
        return (f"Product falls under category: {self.category}, "
                f"is supposed to be used by the gender {self.gender},"
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


def deserialize_products(filename: str) -> list:
    """
    Deserializes products from a given file
    :param filename: Name of the file to deserialize
    :return: List of products
    """
    # Open a file with products and their respective heuristics (probably json TODO: asses other possibilities)
    products = []
    with open(filename, "r") as file:
        products_data = json.load(file)
        for product_data in products_data:
            properties = ProductProperties(category=product_data["properties"]["category"],
                                           gender=product_data["properties"]["gender"],
                                           age=product_data["properties"]["age"])
            product = Product(name=product_data["name"], properties=properties)
            products.append(product)
    return products


def pick_products(products_threshold: int, products) -> dict[Any, int]:
    """
    Picks products based on given parameters
    :param products_threshold: Number of products to pick
    :param products: List of products
    :return: Given number of products that are the most attractive
    """
    evaluated_products = {} # Dictionary of picked products and their attractiveness
    for product in products:
        attractiveness = 1
        # Add some heuristics here
        evaluated_products[product] = attractiveness
    evaluated_products.sort(key=lambda x: x[1], reverse=True)
    return evaluated_products[:products_threshold]

# test
if __name__ == "__main__":
    products = pick_products(5, "products_sample.json")
    for product in products:
        print(product)