import json
from typing import Dict, Any


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
                                           age=product_data["properties"]["age"],
                                           customer_disclaimer=product_data["properties"]["customer_disclaimer"],
                                           image=product_data["properties"]["image"])
            product = Product(name=product_data["name"], properties=properties)
            products.append(product)
    return products


def pick_products(products_threshold: int, products) -> list:
    """
    Picks products based on given parameters
    :param products_threshold: Number of products to pick
    :param products: List of products
    :return: Given number of products that are the most attractive
    """
    evaluated_products = {}  # Dictionary of picked products and their attractiveness
    for product in products:
        attractiveness = 1
        # Add some heuristics here
        evaluated_products[product] = attractiveness
    # Sort the products by their attractiveness
    evaluated_products_list = [product for product, _ in
                               sorted(evaluated_products.items(), key=lambda item: item[1], reverse=True)]
    return evaluated_products_list[:products_threshold]


def serialize_products(products: list, filename: str) -> None:
    """
    Serializes products to a given file
    :param products: List of products to serialize
    :param filename: Name of the file to serialize
    :return: None
    """
    products_data = []
    for product in products:
        products_data = {"name": product.name,
                         "properties":
                             {"category": product.properties.category,
                              "customer_disclaimer": product.properties.disclaimer,
                              "image": product.properties.image}}
    with open(filename, "w") as file:
        try:  # Try to serialize the products
            json.dump(products_data, file)
        except json.JSONDecodeError as e:
            print(f"Error while serializing products: {e}")


# test
if __name__ == "__main__":

    products = deserialize_products("../tests/test_files/products_sample.json")
    evaluated_products = pick_products(3, products)
    for item in evaluated_products:
        print(item)
    serialize_products(evaluated_products, "../tests/test_files/picked_products_sample.json")
