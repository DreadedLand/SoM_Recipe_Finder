from bs4 import BeautifulSoup

def parse_epicurious(response):
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", itemprop="name")
    title = title_tag.get_text(strip=True) if title_tag else None

    ingredient_tags = soup.select("li.ingredient")
    if not ingredient_tags:
        ingredient_tags = soup.select("div.ingredient-group li")

    ingredients = [tag.get_text(strip=True) for tag in ingredient_tags if tag.get_text(strip=True)]

    return {
        "title": title,
        "ingredients": ingredients
    }
