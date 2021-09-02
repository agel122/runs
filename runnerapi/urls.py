from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from .views import AverageData, AllData

router = DefaultRouter()
router.register('all_runs', AllData, basename='all_runs')

urlpatterns = [
    path('average_data/', AverageData.as_view(), name='average_data'),
]

urlpatterns += router.urls


"""runs_list = AllData.as_view({
    'get': 'list',
    'post': 'create'
})
runs_detail = AllData.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('average_data/', AverageData.as_view(), name='average_data'),
    path('all_runs/', runs_list, name='all_runs'),
    path('all_runs/<int:pk>/', runs_detail, name='runs-detail')
])


"""
"""
urlpatterns = [
    path('', api_root),
    path('average_data/', AverageData.as_view(), name='average_data'),
    path('all_runs/', AllData.as_view({'get': 'list', 'post': 'create'}), name='all_runs'),
]
"""