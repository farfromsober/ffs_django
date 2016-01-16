# -*- coding: utf-8 -*-

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from users.models import Profile
from products.models import Product
from images.models import Image
from products.models import Product, Category

# Create your tests here.
from rest_framework.test import APITestCase, APIClient


class ImageAPITestCase(APITestCase):

    username = 'testuser1'
    password = 'testuser1'
    username2 = 'testuser2'
    password2 = 'testuser2'

    # Setup each test
    def setUp(self):

        self.client = APIClient()

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

    # Helper to login
    def _require_login(self, user):
        self.client.force_authenticate(user)

    ## CREATE tests ##

    def test_add_new_image_without_authentication(self):
        """
        Prueba que se devuelve un 'Unauthorized' si se intenta añadir imágenes
        a un producto sin que el usuario esté autenticado
        """
        post_data = {
            "productId": 1,
            "urls": [
                "http://www.image1.com"
            ]
        }
        response = self.client.post('/api/1.0/images/', data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_new_image_status_code_created(self):
        """
        Prueba que se devuelve un 'Unauthorized' si se intenta añadir imágenes
        a un producto sin que el usuario esté autenticado
        """
        self._require_login(self.user1)

        post_data = {
            "productId": 1,
            "urls": [
                "http://www.image1.com"
            ]
        }
        response = self.client.post('/api/1.0/images/', data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_new_image_storage(self):

        self._require_login(self.user1)

        post_data = {
            "productId": 1,
            "urls": [
                "http://www.image1.com"
            ]
        }
        self.client.post('/api/1.0/images/', data=post_data, format='json')

        product1 = Product.objects.get(pk=1)
        image1 = Image.objects.get(product = product1)
        self.assertEqual(image1.url, "http://www.image1.com")

    ## RETRIEVE test ##

    def test_get_image_without_authentication(self):
        """
        Prueba que se devuelve un 'Unauthorized' si el usuario intenta
        recuperar las imágenes de un producto sin estar autenticado
        """
        response = self.client.get('/api/1.0/images/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_image_of_not_existing_product(self):
        """
        Prueba que se devuelve un 'Not found' si no
        existe ningún producto con ese productId
        """
        self._require_login(self.user1)
        response = self.client.get('/api/1.0/images/55/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_image_of_product(self):
        """
        Prueba que se devuelve un array de urls
        asociado al producto
        """
        self._require_login(self.user1)

        product1 = Product.objects.get(pk=1)
        image1 = Image.objects.create(product=product1, url="http://www.image1.com")

        response = self.client.get('/api/1.0/images/1')
        self.assertEqual(response.data, image1.url)

    ## UPDATE test ##

    def test_update_image_without_authentication(self):
        """
        Prueba que se devuelve un 'Unauthorized' si el usuario intenta
        recuperar las imágenes de un producto sin estar autenticado
        """
        response = self.client.put('/api/1.0/images/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ## DESTROY test ##

    def test_destroy_image_not_allowed(self):
        """
        Prueba que no se devuelve un 'Not allowed' si
        el usuario intenta hacer un DELETE de un producto
        """
        self._require_login(self.user1)
        response = self.client.delete('/api/1.0/images/1/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    ## LIST test ##

    def test_list_image_not_allowed(self):
        """
        Prueba que no se devuelve un 'Not allowed' si
        el usuario intenta hacer un DELETE de un producto
        """
        self._require_login(self.user1)
        response = self.client.get('/api/1.0/images/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)