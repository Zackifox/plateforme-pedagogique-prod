from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    LogoutView,
    MeView,
    InscriptionView,
    LoginEmailOuUsernameView,
    GoogleLoginView,
)

urlpatterns = [
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('login/', LoginEmailOuUsernameView.as_view(), name='login'),
    path('login-admin/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-google/', GoogleLoginView.as_view(), name='login_google'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
]