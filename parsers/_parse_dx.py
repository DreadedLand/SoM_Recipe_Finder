from .allrecipes import parse_allrecipes
from .bonappetit import parse_bonappetit
from .epicurious import parse_epicurious
from .foodcom import parse_foodcom
from .foodnetwork import parse_foodnetwork

''' '^' forces code to follow exactly the pattern

# we use blog regex to crawl more and find more recipes

# DOMAINS: {function, recipe regex, blog regex}
'''

DOMAINS = {
    "allrecipes.com": [parse_allrecipes, r"^(recipe/\d+/[^/]+/?|[^/]+-recipe-\d{7,9}/?)$", r"-\d{7,8}"],  # checks 4+ amt of digits and that there is only one path segment after recipe
    "bonappetit.com": [parse_bonappetit, r"^recipe/[^/]+$", r"gallery/[^/]+$"],  # end after 1 subset past /recipes/
    "epicurious.com": [parse_epicurious, r"^recipes/food/views/[^/]+-?$", r"recipes-menus/[^/]"],  # checks digits at end, with no subsets of url past digits
    # "food.com": [parse_foodcom,],
    "foodnetwork.com": [parse_foodnetwork, r"^recipes/.+-\d+/?$", r"/recipes/photos/[^/]"]  # /recipes/ then ignore rest of string, check end of string for digits
}

def get_recipe_data(response):
    # we do not need the regex strings for this, so we use '_'
    for domain, (func, _, _) in DOMAINS.items():
        if domain in response.url:
            return func(response)
    print(f"No parser for: {response.url}")
    return None