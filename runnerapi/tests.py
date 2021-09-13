import json
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from .models import Run
from .views import AverageData, AllData
from .serializers import RunSerializer, UserSerializer


class RegistrationTestCase(APITestCase):

    def test_registration_ok(self):
        data = {'username': 'testuser',
                'email': 'testuser@email.com',
                'password': 'testpass'}
        response = self.client.post('/user_create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_nok(self):
        data = {'username': 'testuser',
                'email': 'testuser@email.com'}
        response = self.client.post('/user_create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    url1 = reverse('all_runs-list')

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser88',
                                              password='testpass88',
                                              email='testuser88@email.com')
        self.user2 = User.objects.create_user(username='testuser99',
                                              password='testpass99',
                                              email='testuser99@email.com')
        self.token = Token.objects.create(user=self.user1)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_all_runs_list_authonticated(self):
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_runs_list_unauthonticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_runs_post_authonticated(self):
        response = self.client.post(reverse('all_runs-list'),
                                    {"date": "2021-09-11",
                                     "distance": 20,
                                     "time": 20})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_all_runs_post_unauthonticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('all_runs-list'),
                                    {"date": "2021-09-11",
                                     "distance": 20,
                                     "time": 20})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_runs_put_authonticated(self):
        self.client.post(reverse('all_runs-list'),
                               {"date": "2021-09-11",
                                "distance": 20,
                                "time": 20})
        response = self.client.put(reverse('all_runs-detail', kwargs={'pk': 1}),
                                   {"date": "2021-09-11",
                                    "distance": 22,
                                    "time": 22})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_all_runs_put_unauthonticated(self):
        self.client.force_authenticate(user=None)
        self.client.post(reverse('all_runs-list'),
                               {"date": "2021-09-11",
                                "distance": 20,
                                "time": 20})
        response = self.client.put(reverse('all_runs-detail', kwargs={'pk': 1}),
                                   {"date": "2021-09-11",
                                    "distance": 22,
                                    "time": 22})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_runs_delete_authonticated(self):
        self.client.post(reverse('all_runs-list'),
                               {"date": "2021-09-11",
                                "distance": 20,
                                "time": 20})
        response = self.client.delete(reverse('all_runs-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_all_runs_delete_unauthonticated(self):
        self.client.force_authenticate(user=None)
        self.client.post(reverse('all_runs-list'),
                               {"date": "2021-09-11",
                                "distance": 20,
                                "time": 20})
        response = self.client.delete(reverse('all_runs-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_average_data_get_authonticated(self):
        self.client.post(reverse('all_runs-list'),
                         {"date": "2021-09-11",
                          "distance": 20,
                          "time": 20})
        self.client.post(reverse('all_runs-list'),
                         {"date": "2021-09-11",
                          "distance": 10,
                          "time": 10})
        response = self.client.get(reverse('average_data'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_distance in m'], 15000)
        self.assertEqual(response.data['max_distance in km'], {"id": 1,
                                                               "owner": 1,
                                                               "date": "2021-09-11",
                                                               "distance": "20.000",
                                                               "time": 20},)
        self.assertEqual(response.data['average_distance in m'], 15000)
        self.assertEqual(response.data['average_time in min'], 15)
        self.assertEqual(response.data['average_speed m/min'], 1000)
        self.assertEqual(response.data['max_speed in m/min'], 1000)

    def test_average_data_get_unauthonticated(self):
        self.client.force_authenticate(user=None)
        self.client.post(reverse('all_runs-list'),
                         {"date": "2021-09-11",
                          "distance": 20,
                          "time": 20})
        response = self.client.get(reverse('average_data'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_average_data_get_useronly(self):
        self.client.post(reverse('all_runs-list'),
                         {"date": "2021-09-11",
                          "distance": 20,
                          "time": 20})
        self.client.force_authenticate(user=self.user2)
        self.client.post(reverse('all_runs-list'),
                         {"date": "2021-09-11",
                          "distance": 10,
                          "time": 10})
        response = self.client.get(reverse('average_data'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_distance in m'], 10000)
























