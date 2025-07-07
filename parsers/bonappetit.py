from bs4 import BeautifulSoup

def parse_bonappetit(response):
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", class_="post__title")
    if not title_tag:
        title_tag = soup.find("h1", {"data-testid": "ContentHeaderHed"})
    title = title_tag.get_text(strip=True) if title_tag else None

    ingredient_tags = soup.select("div.ingredient__text")
    if not ingredient_tags:
        ingredient_tags = soup.select("li[data-testid='IngredientListItem']")

    ingredients = [tag.get_text(strip=True) for tag in ingredient_tags if tag.get_text(strip=True)]

    return {
        "title": title,
        "ingredients": ingredients
    }
