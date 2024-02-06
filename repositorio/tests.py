
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .views import signout

class SignoutTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba para usarlo en las pruebas
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_signout_redirects_to_login_page(self):
        # Autenticar al usuario creado
        self.client.login(username='testuser', password='testpassword')
        
        # Hacer una solicitud a la vista de signout
        response = self.client.get(reverse('signout'))

        # Verificar que la respuesta sea una redirección
        self.assertEqual(response.status_code, 302)

        # Verificar que la redirección sea a la página de inicio de sesión
        self.assertEqual(response.url, reverse('signin'))

        # Verificar que el usuario ya no esté autenticado
        self.assertFalse(authenticate(username='testuser', password='testpassword'))

