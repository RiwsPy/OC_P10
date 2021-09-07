from django.test import TestCase
from django.urls.base import reverse
from catalogue.models import Product, Category
from catalogue.management.commands.enums import OFF_TO_DB, OFF_TO_DB_NUTRIMENTS

# Create your tests here.

class ModelsTest(TestCase):
    # ran before each test.
    def setUp(self):
        category_01 = Category.objects.create(
            name="Plat léger"
        )
        product_01 = Product.objects.create(
            code="32",
            product_name="Fromage à raclette",
            nova_groups=4,
            nutrition_grades="D",
            stores="",
            picture_url="https://fr.openfoodfacts.org/images/products/317/658/201/6252/front_fr.59.400.jpg",
            eco_score="C",
            energy_value=10.0,
            fat_value=12.2,
            sugar_value=324.1,
            fiber_value=73.1,
            protein_value=22.2,
            salt_value=924.2)

        product_01.categories.set([category_01])

    def test_url_product(self):
        pro = Product.objects.get(pk='32')
        
        self.assertEqual(pro.off_url, "https://fr.openfoodfacts.org/product/32")

    def test_clean(self):
        data_test= {
            'code':"355",
            'product_name_fr':"Cordon bleu père Dodu",
            'nova_groups':4,
            'nutrition_grades':"B",
            'stores':"",
            'picture_url':"https://fr.openfoodfacts.org/images/products/359/669/013/6046/front_fr.39.400.jpg",
            'ecoscore_grade':"D",
            'nutriments': {
                'energy-kcal_100g':32.0,
                'fat_100g':42.2,
                'carbohydrates_100g':12.1,
                'fiber_100g':72.1,
                'proteins_100g':14.2,
                'salt_100g':9.2}}
        new_pro = Product()
        new_pro.clean(data_test)

        for attr_OFF, attr_DB in OFF_TO_DB.items():
            self.assertEqual(getattr(new_pro, attr_DB), data_test.get(attr_OFF))
        for attr_OFF, attr_DB in OFF_TO_DB_NUTRIMENTS.items():
            self.assertEqual(getattr(new_pro, attr_DB), data_test['nutriments'].get(attr_OFF))

        self.assertEqual(new_pro.is_clean(), True)
