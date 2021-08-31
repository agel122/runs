from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Max, Avg, Q
from .models import Run
from .serializers import RunSerializer


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer


class MyAdditionalView(APIView):
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


class MyNewAdditionalView(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer

    def list(self, request):
        data_all = Run.objects.all()
        distance_max = Run.objects.order_by('-distance').first()
        serializer1 = RunSerializer(data_all, many=True)
        serializer2 = RunSerializer(distance_max)
        return Response({
            'data': serializer1.data,
            'max_distance': serializer2.data,
        })


class MyFilteredData(generics.ListAPIView):

    serializer_class = RunSerializer

    def get_queryset(self):
        queryset = Run.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date is not None and end_date is not None:
            queryset = queryset.filter(Q(date__gte=start_date) & Q(date__lte=end_date))
        return queryset


class MySummaryViewset(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer

    def get_queryset(self):
        queryset = self.queryset
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date is not None and end_date is not None:
            queryset = queryset.filter(Q(date__gte=start_date) & Q(date__lte=end_date))
        return queryset











