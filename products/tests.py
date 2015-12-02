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
        self.user1 = User.objects.create_user(username='testuser1', password='testuser1',
                                              first_name='test', last_name='user1')
        self.user2 = User.objects.create_user(username='testuser2', password='testuser2',
                                              first_name='test', last_name='user2')
        self.user1.save()
        self.user2.save()

        # Se crean dos perfiles
        profile1 = Profile.objects.create(user=self.user1,
                                          avatar='http://cdn.redmondpie.com/wp-content/uploads/2011/07/Avatar.png',
                                          latitude='4.0', longitude='4.0', city='boston', state='cund', sales='0')
        profile2 = Profile.objects.create(user=self.user2,
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
        self.product1 = Product.objects.create(name='Producto 1',
                                               description='Descripcion producto 1',
                                               price=24,
                                               seller=profile1,
                                               category=category1)
        self.product2 = Product.objects.create(name='Producto 2',
                                               description='Descripcion producto 2',
                                               price=312,
                                               seller=profile2,
                                               category=category2,
                                               selling=False)
        self.product1.save()
        self.product2.save()

    def _require_login(self, username, password):
        self.client.login(username=username, password=password)

    def test_list_products_without_authentication(self):
        """
        Prueba que no se devuelve un listado de productos si no se está autenticado
        :return:
        """
        response = self.client.get('/api/1.0/products/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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

    def test_list_products_filtered_by_category(self):
        """
        Prueba que se devuelva completa la lista de productos
        :return:
        """
        self._require_login(self.username, self.password)
        response = self.client.get('/api/1.0/products/?category=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Producto 2')
        self.assertEqual(response.data[0]['description'], 'Descripcion producto 2')

    def test_get_product_without_authentication(self):
        """
        Prueba que no se devuelve un detalle de producto si no se está autenticado
        :return:
        """
        response = self.client.get('/api/1.0/products/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_non_existing_product(self):
        """
        Prueba que no se devuelve un detalle de producto si éste no existe
        :return:
        """
        self._require_login(self.username, self.password)
        response = self.client.get('/api/1.0/products/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
        self.assertEqual(response.data['selling'], False)
        self.assertEqual(response.data['price'], '312.0')
        self.assertEqual(response.data['seller']['user']['username'], 'testuser2')
        self.assertEqual(response.data['category']['name'], 'deportes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_not_selling_product(self):
        """
        Prueba que no se elimine un producto que no esté en venta
        :return:
        """
        self._require_login(self.username, self.password)
        response = self.client.delete('/api/1.0/products/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_not_my_product(self):
        """
        Prueba que no se elimine un producto del cual no seamos el vendedor
        :return:
        """
        self._require_login(self.username, self.password)
        response = self.client.delete('/api/1.0/products/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product(self):
        """
        Prueba que se elimine un producto
        :return:
        """
        self._require_login(self.username, self.password)
        response = self.client.delete('/api/1.0/products/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/api/1.0/products/1/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_new_product_without_authentication(self):
        """
        Prueba que no se agregue de producto si no se está autenticado
        :return:
        """
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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_new_product(self):
        """
        Prueba que se agregue un producto que no existe
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
        self.assertNotEqual(response.data['published_date'], '')
        self.assertEqual(response.data['name'], 'Producto 3')
        self.assertEqual(response.data['description'], 'Descripcion de producto 3')
        self.assertEqual(response.data['selling'], True)
        self.assertEqual(response.data['price'], '4500.0')
        self.assertEqual(response.data['seller']['user']['username'], self.username)
        self.assertEqual(response.data['category']['name'], 'deportes')

    def test_update_product_without_authentication(self):
        """
        Prueba que se agregue un producto que no existe
        :return:
        """
        post_data = {
            "category": {
                "name": "general",
                "index": 0
            },
            "name": "Producto 2 modified",
            "description": "Descripcion de producto 2 modified",
            "selling": True,
            "price": 20,
        }

        response = self.client.put('/api/1.0/products/1/', data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_not_my_product(self):
        """
        Prueba que se agregue un producto que no existe
        :return:
        """
        post_data = {
            "category": {
                "name": "general",
                "index": 0
            },
            "name": "Producto 2 modified",
            "description": "Descripcion de producto 2 modified",
            "selling": True,
            "price": 20,
        }

        response = self.client.put('/api/1.0/products/2/', data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_product(self):
        """
        Prueba que se agregue un producto que no existe
        :return:
        """
        self._require_login(self.username, self.password)
        post_data = {
            "category": {
                "name": "general",
                "index": 0
            },
            "name": "Producto 2 modified",
            "description": "Descripcion de producto 2 modified",
            "selling": True,
            "price": 20,
        }

        response = self.client.put('/api/1.0/products/1/', data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Producto 2 modified')
        self.assertEqual(response.data['description'], 'Descripcion de producto 2 modified')
        self.assertEqual(response.data['selling'], True)
        self.assertEqual(response.data['price'], '20.0')
        self.assertEqual(response.data['category']['name'], 'general')
