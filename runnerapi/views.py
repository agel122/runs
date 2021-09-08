from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.db.models import Max, Avg, Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Run
from .serializers import RunSerializer, UserSerializer
from rest_framework import status


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'all_runs': reverse('all_runs-list', request=request, format=format),
        'average_data': reverse('average_data', request=request, format=format),
        'user_create': reverse('user_create', request=request, format=format),
        'users': reverse('user_list', request=request, format=format),
        'login': reverse('login', request=request, format=format),
    })


class AverageData(APIView):
    def get(self, request):
        data_all = Run.objects.all()
        distance_max = Run.objects.order_by('-distance').first()
        distance_av = int(data_all.aggregate(Avg('distance'))['distance__avg']*1000)
        time_av = int(data_all.aggregate(Avg('time'))['time__avg'])
        speed_av = int(distance_av/time_av)
        serializer = RunSerializer(distance_max)

        speeds = []
        for item in data_all.values():
            speed = float(item['distance'])*1000/float(item['time'])
            speeds.append(speed)
        speed_max = int(max(speeds))
        return Response({
            'max_distance in km': serializer.data,
            'average_distance in m': distance_av,
            'average_time in min': time_av,
            'average_speed m/min': speed_av,
            'max_speed in m/min': speed_max,
        })


class AllData(viewsets.ModelViewSet):
    queryset = Run.objects
    serializer_class = RunSerializer

    def get_queryset(self):
        queryset = self.queryset
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date is not None and end_date is not None:
            queryset = queryset.filter(Q(date__gte=start_date) & Q(date__lte=end_date))
        return queryset.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)










