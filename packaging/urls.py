from django.urls import path

from .views import recommend_box_view

urlpatterns = [
    path(
        "orders/<int:order_id>/recommend-box/",
        recommend_box_view,
        name="recommend-box",
    ),
]
