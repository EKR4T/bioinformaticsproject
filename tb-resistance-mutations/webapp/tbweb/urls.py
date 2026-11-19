from django.urls import path

from predictor import views

urlpatterns = [
    path("", views.index, name="index"),
    path("model/", views.model_card, name="model"),
    path("api/predict", views.api_predict, name="api_predict"),
    path("api/features", views.api_features, name="api_features"),
]
