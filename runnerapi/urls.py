from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from .views import AverageData, AllData, api_root, UserCreate, UserList, LoginView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="RUNS API",
      default_version='v1',
      description="Test description",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('all_runs', AllData, basename='all_runs')


urlpatterns = [
    path('', api_root),
    path('average_data/', AverageData.as_view(), name='average_data'),
    path('user_create/', UserCreate.as_view(), name='user_create'),
    path('users', UserList.as_view(), name='user_list'),
    path('login/', LoginView.as_view(), name='login'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += router.urls

