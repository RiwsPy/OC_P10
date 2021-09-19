from django.core.management.base import BaseCommand, CommandError
from .enums import HEADERS, PAYLOAD, CATEGORIES, URL_SEARCH
import requests
from catalogue.models import Product, Category
import json

class Command(BaseCommand):
    help = 'Update database with OpenFoodFacts API'

    def handle(self, *args, **options) -> None:
        self.call_api()
        self.stdout.write(self.style.SUCCESS('Mise à jour de la base de données réussie.'))
        #self.stdout.write(self.style.ERROR('Error')

    def call_api(self) -> None:
        """
            Request Open Food Facts API
            Save the results in the database
        """

        code_set = set()
        print("Mise à jour de la base de données...")
        params = PAYLOAD.copy()
        Category.objects.all().delete()
        Product.objects.all().delete()

        for category in CATEGORIES:
            params["tag_0"] = category
            req = requests.get(URL_SEARCH, params=params, headers=HEADERS)
            if req.status_code == 200:
                results_json = req.json()

                cat = self.save_category(category)

                for product_data in results_json["products"]:
                    if not product_data["code"] in code_set:
                        code_set.add(product_data["code"])
                        self.save_product(product_data, cat)

    def save_category(self, category_name: str) -> Category:
        cat = Category()
        cat.name = category_name[:200]
        cat.save()
        return cat

    def save_product(self, product_data: dict, cat: Category) -> None:
        pro = Product()
        pro.clean(product_data)
        if pro.is_clean():
            pro.save()
            pro.categories.add(cat)
            pro.save()
