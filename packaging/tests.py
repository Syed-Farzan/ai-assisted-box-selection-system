from decimal import Decimal

from django.test import TestCase

from .models import Box, Product
from .services import product_fits_in_box


class ProductFitsInBoxTests(TestCase):
    def create_product(self, length, width, height, weight=1):
        return Product.objects.create(
            name="Test Product",
            length=Decimal(str(length)),
            width=Decimal(str(width)),
            height=Decimal(str(height)),
            weight=Decimal(str(weight)),
        )

    def create_box(self, length, width, height, max_weight=10, cost=10):
        return Box.objects.create(
            name="Test Box",
            length=Decimal(str(length)),
            width=Decimal(str(width)),
            height=Decimal(str(height)),
            max_weight=Decimal(str(max_weight)),
            cost=Decimal(str(cost)),
        )

    def test_product_fits_normally(self):
        product = self.create_product(5, 5, 5)
        box = self.create_box(10, 10, 10)

        result = product_fits_in_box(product, box)

        self.assertTrue(result)

    def test_product_fits_after_rotation(self):
        product = self.create_product(20, 10, 5)
        box = self.create_box(10, 20, 10)

        result = product_fits_in_box(product, box)

        self.assertTrue(result)

    def test_product_does_not_fit_dimensionally(self):
        product = self.create_product(15, 15, 15)
        box = self.create_box(10, 10, 10)

        result = product_fits_in_box(product, box)

        self.assertFalse(result)
