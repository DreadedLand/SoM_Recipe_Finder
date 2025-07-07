from urllib.parse import urlparse

from .allrecipes import parse_allrecipes
from .bonappetit import parse_bonappetit
from .epicurious import parse_epicurious
from .foodcom import parse_foodcom
from .foodnetwork import parse_foodnetwork

def get_recipe_data(response):
    domain = urlparse(response.url).netloc.lower()

    if "allrecipes.com" in domain:
        return parse_allrecipes(response)
    elif "bonappetit.com" in domain:
        return parse_bonappetit(response)
    elif "epicurious.com" in domain:
        return parse_epicurious(response)
    elif "food.com" in domain:
        return parse_foodcom(response)
    elif "foodnetwork.com" in domain:
        return parse_foodnetwork(response)
    else:
        return None