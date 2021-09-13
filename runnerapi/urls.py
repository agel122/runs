from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AverageData, AllData, api_root, UserCreate, UserList, LoginView


router = DefaultRouter()
router.register('all_runs', AllData, basename='all_runs')


urlpatterns = [
    path('', api_root),
    path('average_data/', AverageData.as_view(), name='average_data'),
    path('user_create/', UserCreate.as_view(), name='user_create'),
    path('users', UserList.as_view(), name='user_list'),
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += router.urls

