from woocommerce import API

def publish_product(shop_url: str, woo_key: str, woo_secret: str, product_name: str, product_price: str, product_description: str, short_description: str, category: int, image_url: str):    
    wcapi = API(
        url=shop_url,
        consumer_key=woo_key,
        consumer_secret=woo_secret,
        version="wc/v3"
    )

    data = {
        "name": product_name,
        "type": "simple",
        "regular_price": product_price,
        "description": product_description,
        "short_description": short_description,
        "categories": [
            {
                "id": category
            }
        ],
        "images": [
            {
                "src": image_url
            }
        ]
    }

    print(wcapi.post("products", data).json())