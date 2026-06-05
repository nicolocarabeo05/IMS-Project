from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.index, name="dashboard-index"),
    path("staff/", views.staff, name="dashboard-staff"),
    path("staff/details/<int:pk>/", views.staff_details, name="dashboard-staff-details"),
    path("product/", views.product, name="dashboard-product"),
    path("product/delete/<int:pk>/", views.product_delete, name="dashboard-product-delete"),
    path("product/update/<int:pk>/", views.product_update, name="dashboard-product-update"),
    path("order/", views.order, name="dashboard-order"),
    path("cancel-order/<int:pk>/", views.cancel_order, name="dashboard-cancel-order"),
    path("update-order-status/<int:pk>/<str:status>/", views.update_order_status, name="dashboard-update-order-status"),
    path('staff/cancel-order/<int:pk>/', views.staff_cancel_order, name='staff-cancel-order'),
]