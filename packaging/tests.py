from decimal import Decimal

from django.test import TestCase

from .models import Box, Order, OrderItem, Product
from .services import product_fits_in_box, recommend_box


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


class RecommendBoxTests(TestCase):
    def create_box(
        self,
        name,
        length,
        width,
        height,
        max_weight,
        cost,
    ):
        return Box.objects.create(
            name=name,
            length=Decimal(str(length)),
            width=Decimal(str(width)),
            height=Decimal(str(height)),
            max_weight=Decimal(str(max_weight)),
            cost=Decimal(str(cost)),
        )

    def create_product(
        self,
        name,
        length,
        width,
        height,
        weight,
    ):
        return Product.objects.create(
            name=name,
            length=Decimal(str(length)),
            width=Decimal(str(width)),
            height=Decimal(str(height)),
            weight=Decimal(str(weight)),
        )

    def create_order_with_item(self, product, quantity=1):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
        )

        return order

    def test_box_rejected_when_weight_exceeds_capacity(self):
        box = self.create_box(
            "Test Box",
            20,
            20,
            20,
            5,
            10,
        )

        product = self.create_product(
            "Heavy Product",
            10,
            10,
            10,
            10,
        )

        order = self.create_order_with_item(product)

        result = recommend_box(order.id)

        self.assertIsNone(result)

    def test_box_rejected_when_total_volume_exceeds_box_volume(self):
        box = self.create_box(
            "Test Box",
            10,
            10,
            10,
            20,
            10,
        )

        product = self.create_product(
            "Product",
            10,
            10,
            6,
            1,
        )

        order = self.create_order_with_item(
            product,
            quantity=2,
        )

        result = recommend_box(order.id)

        self.assertIsNone(result)

    def test_lowest_cost_box_is_selected_when_multiple_boxes_fit(self):
        cheap_box = self.create_box(
            "Cheap Box",
            20,
            20,
            20,
            20,
            10,
        )

        self.create_box(
            "Expensive Box",
            20,
            20,
            20,
            20,
            20,
        )

        product = self.create_product(
            "Product",
            5,
            5,
            5,
            1,
        )

        order = self.create_order_with_item(product)

        result = recommend_box(order.id)

        self.assertEqual(result.id, cheap_box.id)

    def test_least_unused_volume_selected_when_cost_is_same(self):
        large_box = self.create_box(
            "Large Box",
            30,
            30,
            30,
            20,
            10,
        )

        smaller_box = self.create_box(
            "Smaller Box",
            20,
            20,
            20,
            20,
            10,
        )

        product = self.create_product(
            "Product",
            10,
            10,
            10,
            1,
        )

        order = self.create_order_with_item(product)

        result = recommend_box(order.id)

        self.assertEqual(result.id, smaller_box.id)

    def test_returns_none_when_no_suitable_box_exists(self):
        self.create_box(
            "Small Box",
            10,
            10,
            10,
            5,
            10,
        )

        product = self.create_product(
            "Too Large Product",
            20,
            20,
            20,
            10,
        )

        order = self.create_order_with_item(product)

        result = recommend_box(order.id)

        self.assertIsNone(result)
