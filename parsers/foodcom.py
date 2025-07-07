from bs4 import BeautifulSoup

def parse_foodcom(response):
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", class_="recipe-title")
    title = title_tag.get_text(strip=True) if title_tag else None

    ingredient_tags = soup.select("li.ingredient")
    ingredients = [tag.get_text(strip=True) for tag in ingredient_tags if tag.get_text(strip=True)]

    return {
        "title": title,
        "ingredients": ingredients
    }
