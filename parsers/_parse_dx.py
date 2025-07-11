from .allrecipes import parse_allrecipes
from .bonappetit import parse_bonappetit
from .epicurious import parse_epicurious
from .foodcom import parse_foodcom
from .foodnetwork import parse_foodnetwork

DOMAINS = {  # '^' forces code to follow exactly the pattern
    "allrecipes.com": [parse_allrecipes, r"^/recipe/\d{4,}/[^/]+/?$"],  # checks 4+ amt of digits and that there is only one path segment after recipe
    "bonappetit.com": [parse_bonappetit, r"^/recipe/[^/]+$"],  # end after 1 subset past /recipes/
    "epicurious.com": [parse_epicurious, r"^/recipes/food/views/[^/]+-\d+/?$"],  # checks digits at end, with no subsets of url past digits
    # "food.com": [parse_foodcom,],
    "foodnetwork.com": [parse_foodnetwork, r"^/recipes/.+-\d+/?$"]  # /recipes/ then ignore others, check end of string for digits
}

def get_recipe_data(response):
    for domain, (func, _) in DOMAINS.items():
        if domain in response.url:
            return func(response)
    return None