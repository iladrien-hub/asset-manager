from django.urls import path

from .views import RelationView, GeneratorView

urlpatterns = [
    path('', RelationView.as_view(), name="relations"),
    path('generate', GeneratorView.as_view(), name="generate"),
]