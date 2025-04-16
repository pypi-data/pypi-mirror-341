from django.test import TestCase
from django.db import models
from django.apps import apps
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from drf_builder.viewsets import DynamicModelViewSet
from drf_builder.serializers import DynamicSerializer
from drf_builder.routers import register_dynamic_api


# Modelo de teste simples para usar nos testes
class TestModel(models.Model):
    """Modelo simples para testes."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'tests'
        # Esta configuração é apenas para testes e não cria tabela no banco de dados
        managed = False


class ImportTest(TestCase):
    """Testa se os componentes principais podem ser importados corretamente."""
    
    def test_imports(self):
        """Verifica se as classes principais existem e podem ser importadas."""
        from drf_builder.viewsets import DynamicModelViewSet
        from drf_builder.serializers import DynamicSerializer
        from drf_builder.routers import register_dynamic_api, urlpatterns
        from drf_builder.middleware import APIExceptionMiddleware
        
        self.assertTrue(DynamicModelViewSet is not None)
        self.assertTrue(DynamicSerializer is not None)
        self.assertTrue(register_dynamic_api is not None)
        self.assertTrue(urlpatterns is not None)
        self.assertTrue(APIExceptionMiddleware is not None)


class RouterTest(TestCase):
    """Testa a funcionalidade do router."""
    
    def test_register_dynamic_api(self):
        """Verifica se o registro de API dinâmica funciona."""
        router = DefaultRouter()
        result = register_dynamic_api(router)
        
        # Verifica se o resultado é um router
        self.assertEqual(type(result), type(router))
        
        # Verifica se 'dynamic' foi registrado no router
        has_dynamic = False
        for prefix, viewset, basename in router.registry:
            if prefix == 'dynamic' and viewset == DynamicModelViewSet:
                has_dynamic = True
                break
        
        self.assertTrue(has_dynamic, "O DynamicModelViewSet não foi registrado no router")


class SerializerTest(TestCase):
    """Testa a funcionalidade do serializer dinâmico."""
    
    def test_dynamic_serializer_creation(self):
        """Verifica se o serializer dinâmico pode ser criado para um modelo."""
        # Usando User como modelo para teste, pois é garantido que existe
        serializer = DynamicSerializer(
            model_name='User',
            app_label='auth'
        )
        
        # Verifica se o serializer foi configurado corretamente
        self.assertEqual(serializer.Meta.model, User)
        self.assertEqual(serializer.model_name, 'User')
        self.assertEqual(serializer.app_label, 'auth')


class ViewSetBasicTest(TestCase):
    """Testa funcionalidades básicas do viewset dinâmico."""
    
    def test_viewset_initialization(self):
        """Verifica se o viewset pode ser inicializado."""
        viewset = DynamicModelViewSet()
        
        # Verifica se o viewset tem os atributos esperados
        self.assertTrue(hasattr(viewset, 'get_model'))
        self.assertTrue(hasattr(viewset, 'get_serializer_class'))
        self.assertTrue(hasattr(viewset, 'get_queryset'))


class SimpleJWTIntegrationTest(TestCase):
    """Testa a integração do SimpleJWT com a API."""

    def setUp(self):
        """Configura um usuário para autenticação."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()

    def test_obtain_token(self):
        """Verifica se o endpoint de obtenção de token funciona."""
        response = self.client.post("/api/token/", {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_access_protected_endpoint(self):
        """Verifica se um endpoint protegido requer autenticação."""
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.get("/api/protected-endpoint/")  # Replace with an actual protected endpoint
        self.assertNotEqual(response.status_code, 401)  # Ensure it doesn't return Unauthorized