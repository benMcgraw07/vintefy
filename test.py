import requests
import json
from typing import Any

user_agent = {
    "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 14816.131.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

class VintedApi:

    def __init__(self, proxy=None) -> None:
        self.session = requests.Session()
        if proxy:
            self.session.proxies.update(proxy)
        self.session.get("https://vinted.co.uk", headers=user_agent)

    def getProduct(self, id: int) -> Any:
        params = {
            "localize": "true",
        }
        headers = {
            **user_agent,
            "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Add your access token here
        }
        get_product = self.session.get(f"https://www.vinted.fr/api/v2/items/{id}", 
                                       headers=headers, params=params)
        if get_product.ok:
            json_product = json.loads(get_product.text)
            if json_product["code"] == 0:
                return json_product["item"]
            else:
                return json_product["message_code"]
        elif get_product.status_code == 429:
            return "Rate limited"
        else:
            return get_product
# Example usage
if __name__ == "__main__":
    vinted = VintedApi()
    product_info = vinted.getProduct(6060873469)  # Replace with a valid product ID
    print(product_info)
