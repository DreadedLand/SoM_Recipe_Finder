from .allrecipes import parse_allrecipes
from .bonappetit import parse_bonappetit
from .epicurious import parse_epicurious
from .foodcom import parse_foodcom
from .foodnetwork import parse_foodnetwork

DOMAINS = {
    "allrecipes.com": [parse_allrecipes, r"/recipe/\d+/"],
    "bonappetit.com": [parse_bonappetit, r"/recipe/"],
    "epicurious.com": [parse_epicurious, r"/recipes/food/views/"],
    # "food.com": [parse_foodcom,],
    "foodnetwork.com": [parse_foodnetwork, r"-recipe-\d+/"]
}

def get_recipe_data(response):
    for domain, (func, _) in DOMAINS.items():
        if domain in response.url:
            return func[0](response)
    return None