from bs4 import BeautifulSoup

def parse_foodnetwork(response):
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("div", class_="assetTitle").find("section", class_="o-AssetTitle").find("h1", class_="o-AssetTitle__a-Headline").find("span", class_="o-AssetTitle__a-HeadlineText")
    title = title_tag.get_text(strip=True) if title_tag else None

    ingredients = []
    container = soup.find("div", class_="o-Ingredients__m-Body")
    if container:
        for p in container.find_all("p", class_="o-Ingredients__a-Ingredient"):
            # get rid of select all element
            if "o-Ingredients__a-Ingredient--SelectALl" in p.get("class", []):
                continue
            text = p.find("span", class_="o-Ingredients__a-Ingredient--CheckboxLabel").get_text(strip=True)
            if text:
                ingredients.append(text)

    rating_sr_only = soup.find("div", class_="sr-only").get_text(strip=True)
    rating = rating_sr_only.replace("rated", "").replace(" of ", "/").replace("stars", "").strip()
    return {
        "title": title,
        "ingredients": ingredients,
        "rating": rating
    }
