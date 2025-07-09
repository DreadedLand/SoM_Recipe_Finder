import json

from bs4 import BeautifulSoup

# basically same logic as epicurious yipee
def parse_bonappetit(response):
    try:
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("h1", class_="post__title")
        if not title_tag:
            title_tag = soup.find("h1", {"data-testid": "ContentHeaderHed"})
        title = title_tag.get_text(strip=True) if title_tag else None

        contentScript = soup.find_all("script", type="application/ld+json")

        for tag in contentScript:
            try:
                data = json.loads(tag.string)

                if isinstance(data, list):
                    for item in data:
                        if item.get("@type") == "Recipe":
                            data = item
                            break

                if data.get("@data") != "Recipe":
                    continue

                ingredients = data.get("recipeIngredient", [])
                rating = str(data.get("AggregateRating", {}).get("RatingValue", "N/A"))

                if ingredients:
                    return {
                        "title": title.strip(),
                        "ingredients": [i.ingredients for i in ingredients],
                        "rating": rating.strip()
                    }
            except Exception:
                continue
    except Exception:
        pass

    return None
