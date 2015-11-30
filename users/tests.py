# -*- coding: utf-8 -*-
from django.contrib.auth.hashers import check_password
from django.test import TestCase

# Create your tests here.

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import Profile
from django.contrib.auth.models import User
import base64




class UsersAPITestCase(APITestCase):
    def setUp(self):
        # Se cran dos usuarios para asociarlos a dos perfiles
        user1 = User.objects.create(username='testuser1', password='testuser1', first_name='test', last_name='user1')
        user2 = User.objects.create(username='testuser2', password='testuser2', first_name='test', last_name='user2')
        user1.save()
        user2.save()

        # Se crean dos perfiles
        profile1 = Profile.objects.create(user=user1,
                                          avatar='https://pixabay.com/es/diablo-rojo-bifurcaci%C3%B3n-de-la-echada-963136/',
                                          latitude='4.0', longitude='4.0', city='boston', state='cund', sales='0')
        profile2 = Profile.objects.create(user=user2,
                                          avatar='https://pixabay.com/es/especies-exóticas-flor-avatar-978415/',
                                          latitude='4.0', longitude='4.0', city='boston', state='cund', sales='0')

        profile1.save()
        profile2.save()

    def test_list_users(self):
        """
        Prueba que se devuelva completa la lista de usuarios
        :return:
        """
        response = self.client.get('/api/1.0/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['user']['username'], 'testuser1')
        self.assertEqual(response.data[1]['user']['username'], 'testuser2')

    def test_get_user(self):
        """
        Prueba que se devuelva uno de los usuarios
        :return:
        """
        response = self.client.get('/api/1.0/users/1/')
        self.assertEqual(response.data['user']['username'], 'testuser1')
        self.assertEqual(response.data['user']['first_name'], 'test')
        self.assertEqual(response.data['user']['last_name'], 'user1')
        self.assertEqual(response.data['user']['password'], 'testuser1')
        self.assertEqual(response.data['latitude'], 4.0)
        self.assertEqual(response.data['longitude'], 4.0)
        self.assertEqual(response.data['city'], 'boston')
        self.assertEqual(response.data['state'], 'cund')
        self.assertEqual(response.data['sales'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/1.0/users/2/')
        self.assertEqual(response.data['user']['username'], 'testuser2')
        self.assertEqual(response.data['user']['first_name'], 'test')
        self.assertEqual(response.data['user']['last_name'], 'user2')
        self.assertEqual(response.data['user']['password'], 'testuser2')
        self.assertEqual(response.data['latitude'], 4.0)
        self.assertEqual(response.data['longitude'], 4.0)
        self.assertEqual(response.data['city'], 'boston')
        self.assertEqual(response.data['state'], 'cund')
        self.assertEqual(response.data['sales'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        """
        Prueba que se devuelva elimine un usuario
        :return:
        """
        response = self.client.delete('/api/1.0/users/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/api/1.0/users/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_new_user(self):
        """
        Prueba que se agregue un usuario que no existe
        :return:
        """

        post_data = {
            'avatar': 'https://pixabay.com/es/diablo-rojo-bifurcaci%C3%B3n-de-la-echada-963136/',
            'latitude': '4.6',
            'longitude': '-74.0',
            'city': 'Bogota',
            'state': 'Cundinamarca',
            'sales': 0,
            'user': {
                'password': 'testuser3',
                'username': 'testuser3',
                'first_name': 'test',
                'last_name': 'user3',
            }
        }

        response = self.client.post('/api/1.0/users/',data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'testuser3')
        self.assertEqual(response.data['user']['first_name'], 'test')
        self.assertEqual(response.data['user']['last_name'], 'user3')
        self.assertTrue(check_password('testuser3',response.data['user']['password']) )
        self.assertEqual(response.data['latitude'], 4.6)
        self.assertEqual(response.data['longitude'], -74.0)
        self.assertEqual(response.data['city'], 'Bogota')
        self.assertEqual(response.data['state'], 'Cundinamarca')
        self.assertEqual(response.data['sales'], 0)

    def test_add_existent_user(self):
        """
        Prueba que no se pueda agregar un usuario que ya existe
        :return:
        """

        post_data = {
            'avatar': 'https://pixabay.com/es/diablo-rojo-bifurcaci%C3%B3n-de-la-echada-963136/',
            'latitude': '4.6',
            'longitude': '-74.0',
            'city': 'Bogota',
            'state': 'Cundinamarca',
            'sales': 0,
            'user': {
                'password': 'testuser2',
                'username': 'testuser2',
                'first_name': 'test',
                'last_name': 'user2',
            }
        }

        response = self.client.post('/api/1.0/users/',data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_existent_user(self):
        """
        Prueba que no se pueda actualizar un usuario que ya existe
        :return:
        """

        post_data = {
            'avatar': 'https://pixabay.com/es/diablo-rojo-bifurcaci%C3%B3n-de-la-echada-963136/',
            'latitude': '4.6',
            'longitude': '-74.0',
            'city': 'Bogota',
            'state': 'Cundinamarca',
            'sales': 0,
            'user': {
                'password': 'testuser2',
                'username': 'testuser2',
                'first_name': 'testupdated',
                'last_name': 'user2updated',
            }
        }

        response = self.client.put('/api/1.0/users/2/',data=post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/1.0/users/2/')
        self.assertEqual(response.data['user']['first_name'], 'testupdated')
        self.assertEqual(response.data['user']['last_name'], 'user2updated')


class LoginTests(APITestCase):

    def setUp(self):
        # Se crean un usuario y su perfil
        user1 = User.objects.create(username='testuser1', password='testuser1', first_name='test', last_name='user1')
        user1.save()

        # Se crean dos perfiles
        profile1 = Profile.objects.create(user=user1,
                                          avatar='https://pixabay.com/es/diablo-rojo-bifurcaci%C3%B3n-de-la-echada-963136/',
                                          latitude='4.0', longitude='4.0', city='boston', state='cund', sales='0')

        profile1.save()
        self.url = '/api/1.0/login/'

    def test_login_OK(self):
        """
        Ensure we can login with the .
        """
        data = base64.b64encode(b'testuser1.testuser1')
        print (data)
        response = self.client.post(self.url,{}, format='json', HTTP_AUTHORIZATION= 'Basic dGVzdHVzZXIxLnRlc3R1c2VyMQ==')
        self.assertEqual(response.status_code, status.HTTP_200_OK)