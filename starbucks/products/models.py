from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'menus'


class Category(models.Model):
    name = models.CharField(max_length=50)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)

    class Meta:
        db_table = 'categories'


class Product(models.Model):
    korean_name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    is_new = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'


class Image(models.Model):
    image_url = models.URLField(max_length=2000)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'


class Allergy(models.Model):
    name = models.CharField(max_length=30)
    products = models.ManyToManyField('Product', through='AllergyProduct')

    class Meta:
        db_table = 'allergies'


class AllergyProduct(models.Model):
    allergy = models.ForeignKey('Allergy', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'allergies_products'


class Nutrition(models.Model):
    one_serving_kcal = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    sodium_mg = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    saturated_fat_g = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    sugars_g = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    protein_g = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    caffeine_mg = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    size = models.CharField(max_length=30)
    product = models.OneToOneField('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'nutritions'