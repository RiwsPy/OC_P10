from django.db import models
from catalogue.management.commands.enums import OFF_TO_DB,\
    OFF_TO_DB_NUTRIMENTS, URL_PRODUCT
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from typing import Any

# Produit
# Table d'association Produit / Catégorie


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


# Create your models here.
class Product(models.Model):
    # See:
    # https://github.com/django/django/blob/main/django/db/models/fields/__init__.py
    # Par défaut, null = False

    code = models.CharField(max_length=13, primary_key=True)
    product_name = models.CharField(max_length=100)
    nova_groups = models.PositiveSmallIntegerField()
    nutrition_grades = models.CharField(max_length=1)
    stores = models.CharField(max_length=100, null=True)
    categories = models.ManyToManyField(Category, related_name='category')
    picture_url = models.URLField()

    # ECO Score:
    # https://fr.openfoodfacts.org/eco-score-l-impact-environnemental-des-produits-alimentaires
    eco_score = models.CharField(max_length=1)

    # Nutrition 100g
    energy_value = models.FloatField(default=0)
    fat_value = models.FloatField(default=0)
    sugar_value = models.FloatField(default=0)
    fiber_value = models.FloatField(default=0)
    protein_value = models.FloatField(default=0)
    salt_value = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.product_name

    def is_clean(self) -> bool:
        for attr in OFF_TO_DB.values():
            if getattr(self, attr, None) is None:
                return False
        return 'a' <= self.eco_score.lower() <= 'e'

    def clean(self, data: dict) -> None:
        """
            Initialize item with data
        """
        for attr_OFF, attr_DB in OFF_TO_DB.items():
            setattr(self, attr_DB, data.get(attr_OFF))
        for attr_OFF, attr_DB in OFF_TO_DB_NUTRIMENTS.items():
            setattr(self, attr_DB, data['nutriments'].get(attr_OFF, 0))

        for category in data.get('categories', '').split(', '):
            # TODO: pourquoi pas .get ???!
            cat = Category.objects.filter(pk__iexact=category)
            if cat:
                self.categories.set(cat[0])

        try:
            picture_url = data['selected_images']['front']['display']['fr']
        except KeyError:
            picture_url = ''
        self.picture_url = picture_url

    def update_or_create(self) -> Any:
        """
            Search the object in database
            * if is already created, database is updated and
            object id is returned
            * if not, the object is added in database and his id
            is returned
        """
        product_attrs = self.__dict__
        del product_attrs['_state']
        return self.__class__.objects.update_or_create(**product_attrs)[0]

    @property
    def off_url(self) -> str:
        """
            Return the product OpenFoodFacts url
        """
        return URL_PRODUCT + f'/{self.code}'

    class Meta:
        verbose_name = "produit"
        ordering = ['code']


class Favorite_product(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='search_product')
    substitute = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='substitude_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['product', 'substitute', 'user'],
                name='favorite_unique')
        ]
