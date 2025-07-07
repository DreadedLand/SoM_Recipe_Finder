from bs4 import BeautifulSoup

def parse_allrecipes(response):
    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("h1", class_="article-heading text-headline-400")
    title = title_tag.get_text(strip=True) if title_tag else None
    ingredients = []

    for li in soup.select("li"):
        quantity = li.find("span", attrs={"data-ingredient-quantity": "true"})
        unit = li.find("span", attrs={"data-ingredient-unit": "true"})
        name = li.find("span", attrs={"data-ingredient-name": "true"})

        parts = []
        if quantity:
            parts.append(quantity.get_text(strip=True))
        if unit:
            parts.append(unit.get_text(strip=True))
        if name:
            parts.append(name.get_text(strip=True))

        if parts:
            ingredients.append(" ".join(parts))

    review_tag = soup.find("div", class_="comp mm-recipes-review-bar__rating mntl-text-block text-label-300")
    rating = review_tag.get_text(strip=True) + "/5"
    return {
        "title": title,
        "ingredients": ingredients,
        "rating": rating
    }