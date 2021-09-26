from django.urls import path

from .views import AssetView, AssetRetrieveView, AssetStructureView, SpinsetView, __SpinsetView

urlpatterns = [
    path('<int:pk>', AssetRetrieveView.as_view(), name="retrieve"),
    path('structure/<int:pk>', AssetStructureView.as_view(), name="structure"),
    path('spinset/<int:pk>', SpinsetView.as_view(), name="spinset"),
    path('__spinset', __SpinsetView.as_view(), name="__spinset"),
    path('', AssetView.as_view(), name="asset"),
]