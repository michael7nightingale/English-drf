from django.urls import path, include

from .routers import CategoryRouter
from .views import CategoryViewSet


router = CategoryRouter()
router.register("", CategoryViewSet, "categories")

urlpatterns = [
    path("", include(router.urls)),

]
