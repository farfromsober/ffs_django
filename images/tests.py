# -*- coding: utf-8 -*-

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from users.models import Profile
from products.models import Product, Category

# Create your tests here.
from rest_framework.test import APITestCase


class ImageAPITestCase(APITestCase):

    username = 'testuser1'
    password = 'testuser1'
    username2 = 'testuser2'
    password2 = 'testuser2'

    def setUp(self):

        # Se crean dos usuarios para asociarlos a dos perfiles
        self.user1 = User.objects.create_user(username='testuser1', password='testuser1',
                                              first_name='test', last_name='user1')
        self.user2 = User.objects.create_user(username='testuser2', password='testuser2',
                                              first_name='test', last_name='user2')
        self.user1.save()
        self.user2.save()

        # Se crean dos perfiles
        self.profile1 = Profile.objects.create(user=self.user1,
                                               avatar='http://cdn.redmondpie.com/wp-content/uploads/2011/07/Avatar.png',
                                               latitude='4.0', longitude='4.0', city='boston', state='cund', sales='1')
        self.profile2 = Profile.objects.create(user=self.user2,
                                               avatar='https://pixabay.com/es/especies-exóticas-flor-avatar-978415/',
                                               latitude='4.0', longitude='4.0', city='boston', state='cund', sales='1')

        self.profile1.save()
        self.profile2.save()

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
                                               seller=self.profile1,
                                               category=category1)
        self.product2 = Product.objects.create(name='Producto 2',
                                               description='Descripcion producto 2',
                                               price=312,
                                               seller=self.profile2,
                                               category=category2,
                                               selling=False)
        self.product1.save()
        self.product2.save()

    def _require_login(self, username, password):
        self.client.login(username=username, password=password)

    def test_add_new_image_without_authentication(self):
        """
        Prueba que se devuelve un 'Forbidden' si se intenta añadir imágenes
        a un producto sin que el usuario esté autenticado
        """
        post_data = {
            "productId": 1,
            "urls": [
                "http://www.image1.com",
                "http://www.image2.com"
            ]
        }
        response = self.client.post('/api/1.0/images/', data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_image_without_authentication(self):
        """
        Prueba que se devuelve un 'Forbidden' si el usuario intenta
        recuperar las imágenes de un producto sin estar autenticado
        """
        response = self.client.get('/api/1.0/images/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_image_of_not_existing_product(self):
        """
        Prueba que no se devuelve un 'Not found' si no
        existe ningún producto con ese productId
        """
        self._require_login(self.username, self.password)
        response = self.client.get('/api/1.0/images/55/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)