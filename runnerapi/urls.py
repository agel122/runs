from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import AverageData, AllData

router = DefaultRouter()
router.register('all_runs', AllData, basename='all_runs')

urlpatterns = [
    path('average_data', AverageData.as_view()),
]
urlpatterns += router.urls

