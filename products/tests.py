# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from products.models import Product, Category
from rest_framework import status
from users.models import Profile

# Create your tests here.
from rest_framework.test import APITestCase


class ProductsAPITestCase(APITestCase):

    username = 'testuser1'
    password = 'testuser1'

    def setUp(self):

        # Se crean dos usuarios para asociarlos a dos perfiles
        user1 = User.objects.create_user(username='testuser1', password='testuser1', first_name='test', last_name='user1')
        user2 = User.objects.create_user(username='testuser2', password='testuser2', first_name='test', last_name='user2')
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

        # Se crean dos categorias
        category1 = Category.objects.create(name='general',
                                            index=0)
        category2 = Category.objects.create(name='deportes',
                                            index=1)

        category1.save()
        category2.save()

        # Se crean dos productos para asociarlos a dos usuarios y a dos categorias
        product1 = Product.objects.create(name='Producto 1',
                                          description='Descripcion producto 1',
                                          price=24,
                                          seller=profile1,
                                          category=category1)
        product2 = Product.objects.create(name='Producto 2',
                                          description='Descripcion producto 2',
                                          price=312,
                                          seller=profile2,
                                          category=category2)
        product1.save()
        product2.save()

    def _require_login(self, username, password):
        self.client.login(username=username, password=password)

    def test_list_products(self):
        """
        Prueba que se devuelva completa la lista de productos
        :return:
        """
        self._require_login(self.username, self.password)
        response = self.client.get('/api/1.0/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Producto 2')
        self.assertEqual(response.data[1]['description'], 'Descripcion producto 1')

    def test_get_product(self):
        """
        Prueba que se devuelva uno de los productos
        :return:
        """
        self._require_login(self.username, self.password)
        response = self.client.get('/api/1.0/products/1/')
        self.assertEqual(response.data['name'], 'Producto 1')
        self.assertEqual(response.data['description'], 'Descripcion producto 1')
        self.assertEqual(response.data['selling'], True)
        self.assertEqual(response.data['price'], '24.0')
        self.assertEqual(response.data['seller']['user']['username'], 'testuser1')
        self.assertEqual(response.data['category']['name'], 'general')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/1.0/products/2/')
        self.assertEqual(response.data['name'], 'Producto 2')
        self.assertEqual(response.data['description'], 'Descripcion producto 2')
        self.assertEqual(response.data['selling'], True)
        self.assertEqual(response.data['price'], '312.0')
        self.assertEqual(response.data['seller']['user']['username'], 'testuser2')
        self.assertEqual(response.data['category']['name'], 'deportes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        """
        Prueba que se devuelva elimine un producto
        :return:
        """
        self._require_login(self.username, self.password)
        response = self.client.delete('/api/1.0/products/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/api/1.0/products/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_new_product(self):
        """
        Prueba que se agregue un usuario que no existe
        :return:
        """
        self._require_login(self.username, self.password)
        post_data = {
            "category": {
              "name": "deportes",
              "index": 1
            },
            "price": "4500.0",
            "name": "Producto 3",
            "description": "Descripcion de producto 3"
        }

        response = self.client.post('/api/1.0/products/', data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Producto 3')
        self.assertEqual(response.data['description'], 'Descripcion de producto 3')
        self.assertEqual(response.data['selling'], True)
        self.assertEqual(response.data['price'], '4500.0')
        self.assertEqual(response.data['seller']['user']['username'], 'testuser1')
        self.assertEqual(response.data['category']['name'], 'deportes')
