from django.urls import path
from . import views


urlpatterns = [
    path("blog/", views.BlogView.as_view()),
    path("blog/<str:pk>/", views.BlogView.as_view())
]
