
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("razorpay/", include("razorpay_backend.api.urls"))
]
