from urllib.parse import urlparse

from .allrecipes import parse_allrecipes
from .bonappetit import parse_bonappetit
from .epicurious import parse_epicurious
from .foodcom import parse_foodcom
from .foodnetwork import parse_foodnetwork

DOMAINS = {
    "allrecipes.com": parse_allrecipes,
    "bonappetit.com": parse_bonappetit,
    "epicurious.com": parse_epicurious,
    "food.com": parse_foodcom,
    "foodnetwork.com": parse_foodnetwork
}

def get_recipe_data(response):
    for domain, func in DOMAINS.items():
        if domain in response.url:
            return func(response)
    return None