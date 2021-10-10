URL_OFF = "https://fr.openfoodfacts.org/"
URL_SEARCH = URL_OFF + "cgi/search.pl?"
URL_PRODUCT = URL_OFF + "product"
HEADERS = {"User-Agent": "P8_PurBeurre - Version 0.1"}


CATEGORIES = [
    "Petit-déjeuners",
    "Légumes et dérivés",
    "Céréales et pommes de terre",
    "Plats préparés",
    "Desserts",
    "Boissons",
    ]

PAYLOAD = {
    'action': 'process',
    'tagtype_0': 'categories',
    'tag_contains_0': 'contains',
    'tag_0': '',  # category
    'tagtype_1': 'countries',
    'tag_contains_1': 'contains',
    'tag_1': 'France',
    'tagtype_2': 'categories_lc',
    'tag_contains_2': 'contains',
    'tag_2': 'fr',
    'sort_by': 'unique_scans_n',  # sort by popularity
    'page_size': 50,  # possible choice : 20, 50, 100, 250, 500, 1000
    'page': 1,
    'json': True,
}

OFF_TO_DB = {
    "code": "code",
    "product_name_fr": "product_name",
    "nova_groups": "nova_groups",
    "nutrition_grades": "nutrition_grades",
    "stores": "stores",
    "ecoscore_grade": "eco_score",
}

OFF_TO_DB_NUTRIMENTS = {
    "energy-kcal_100g": "energy_value",
    "carbohydrates_100g": "sugar_value",
    "salt_100g": "salt_value",
    "fat_100g": "fat_value",
    "proteins_100g": "protein_value",
    "fiber_100g": "fiber_value",
}
