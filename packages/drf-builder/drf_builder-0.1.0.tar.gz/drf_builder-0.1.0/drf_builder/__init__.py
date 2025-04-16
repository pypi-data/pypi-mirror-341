"""
API Dinâmica para Django.

Este pacote fornece uma solução para criar endpoints RESTful dinamicamente
para qualquer modelo Django, sem a necessidade de definir viewsets, serializers
ou rotas específicas para cada modelo.

Principais componentes:
- DynamicSerializer: Serializer dinâmico para qualquer modelo
- DynamicModelViewSet: ViewSet dinâmico para operações CRUD
- register_dynamic_api: Função para registrar a API dinâmica em um router

Para mais informações, consulte o README.md.
"""

__version__ = '0.1.0'

# Importe e exponha as principais classes e funções
from .viewsets import DynamicModelViewSet
from .serializers import DynamicSerializer
from .routers import register_dynamic_api, urlpatterns
from .middleware import APIExceptionMiddleware

# Define os componentes públicos disponíveis na importação
__all__ = [
    'DynamicModelViewSet',
    'DynamicSerializer',
    'register_dynamic_api',
    'APIExceptionMiddleware',
    'urlpatterns',
]