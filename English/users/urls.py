from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from .views import AccountViewSet
from .routers import AccountRouter


router = AccountRouter()
router.register("accounts", AccountViewSet, basename='accounts')


urlpatterns = [
    path("", include(
        [
            path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
            path("token/verify/", TokenVerifyView.as_view(), name='token_verify')
        ]
    )),

]

urlpatterns += router.urls
