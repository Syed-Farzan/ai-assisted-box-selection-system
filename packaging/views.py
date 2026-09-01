from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Order
from .services import recommend_box


def recommend_box_view(request, order_id):
    get_object_or_404(Order, id=order_id)

    box = recommend_box(order_id)

    if box is None:
        return JsonResponse({"message": "No suitable box found"})

    return JsonResponse(
        {
            "recommended_box": {
                "id": box.id,
                "name": box.name,
                "cost": str(box.cost),
            }
        }
    )
