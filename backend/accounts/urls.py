from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.MyTokenObtainPairView.as_view(), name='login'),
    path("register/", views.register_user, name="register"),
    path("profile/", views.user_profile, name="profile"),
    path("logout/", views.logout_request, name="logout"),


    path("users/", views.get_users, name="all_users"),
    path("user/<str:id>/update/", views.update_user, name="update_user"),
    path("user/<str:id>/delete/", views.delete_user, name="remove_user")
]
