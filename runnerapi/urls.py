from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import RunViewSet, MyAdditionalView, MyNewAdditionalView, MyFilteredData, MySummaryViewset

router = DefaultRouter()
router.register('runs', RunViewSet, basename='runs')
router.register('all_runs', MyNewAdditionalView, basename='another')
router.register('final', MySummaryViewset, basename='final')

urlpatterns = [
    path('average_data', MyAdditionalView.as_view()),
    path('filtered', MyFilteredData.as_view()),
    path('filtered/<int:pk>', MyFilteredData.as_view(),)
]
urlpatterns += router.urls

