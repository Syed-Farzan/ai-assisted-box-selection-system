from .models import Box, Order


def product_fits_in_box(product, box):
    product_dimensions = sorted(
        [
            product.length,
            product.width,
            product.height,
        ]
    )

    box_dimensions = sorted(
        [
            box.length,
            box.width,
            box.height,
        ]
    )

    return all(
        product_dimension <= box_dimension
        for product_dimension, box_dimension in zip(product_dimensions, box_dimensions)
    )


def recommend_box(order_id):
    order = Order.objects.prefetch_related("items__product").get(id=order_id)

    order_items = order.items.all()

    total_weight = sum(item.product.weight * item.quantity for item in order_items)

    total_volume = sum(
        item.product.length * item.product.width * item.product.height * item.quantity
        for item in order_items
    )

    suitable_boxes = []

    for box in Box.objects.all():

        all_products_fit = all(
            product_fits_in_box(item.product, box) for item in order_items
        )

        if not all_products_fit:
            continue

        if total_weight > box.max_weight:
            continue

        box_volume = box.length * box.width * box.height

        if total_volume > box_volume:
            continue

        unused_volume = box_volume - total_volume

        suitable_boxes.append(
            {
                "box": box,
                "unused_volume": unused_volume,
            }
        )

    if not suitable_boxes:
        return None

    suitable_boxes.sort(
        key=lambda item: (
            item["box"].cost,
            item["unused_volume"],
            item["box"].id,
        )
    )

    return suitable_boxes[0]["box"]
