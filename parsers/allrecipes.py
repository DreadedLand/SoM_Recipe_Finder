from bs4 import BeautifulSoup

def parse_allrecipes(response):
    soup = BeautifulSoup(response.text, "html.parser")
    title = None
    rating = None
    ingredients = []

    try:
        title_tag = soup.find("h1", class_="article-heading text-headline-400")
        if title_tag and title_tag.get_text(strip=True):
            title = title_tag.get_text(strip=True)
        else:
            title = None
    except Exception as errAttr:
        print(f"Failed getting title: {errAttr}")

    for li in soup.select("li"):
        quantity = li.find("span", attrs={"data-ingredient-quantity": "true"})
        unit = li.find("span", attrs={"data-ingredient-unit": "true"})
        name = li.find("span", attrs={"data-ingredient-name": "true"})

        parts = []
        try:
            if quantity:
                parts.append(quantity.get_text(strip=True))
            if unit:
                parts.append(unit.get_text(strip=True))
            if name:
                parts.append(name.get_text(strip=True))
        except Exception as basic:
            print(f"Failed getting stuff: {basic}")

        if parts:
            ingredients.append(" ".join(parts))

    try:
        if soup.find("div", class_="mm-recipes-review-bar__comment") and \
           soup.find("div", class_="mm-recipes-review-bar__comment").get_text(strip=True) == "Be the first to rate & review!":
            rating = "No rating yet"
        else:
            review_tag = soup.find("div", class_="comp mm-recipes-review-bar__rating mntl-text-block text-label-300")
            rating = review_tag.get_text(strip=True) + "/5" if review_tag else None
    except Exception as rating_err:
        print(f"Failed getting rating: {rating_err}")

    return {
        "title": title,
        "ingredients": ingredients,
        "rating": rating
    }
