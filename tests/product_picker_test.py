from ..model.product_picker import deserialize_products, pick_products, serialize_products

# We test the product picker module
# test
if __name__ == "__main__":

    products = deserialize_products("../tests/test_files/products_sample.json")
    evaluated_products = pick_products(3, products)
    for item in evaluated_products:
        print(item)
    serialize_products(evaluated_products, "../tests/test_files/picked_products_sample.json")
