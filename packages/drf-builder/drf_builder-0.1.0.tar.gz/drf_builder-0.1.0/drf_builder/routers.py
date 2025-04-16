"""
Configuração de rotas para a API dinâmica.

Este módulo define as rotas para a API dinâmica, permitindo acesso a qualquer
modelo Django através de endpoints RESTful padronizados.

Endpoints disponíveis:
- GET/POST /<app>/<model>/: Lista todos os objetos ou cria um novo objeto
- GET/PATCH/DELETE /<app>/<model>/<pk>/: Recupera, atualiza ou exclui um objeto específico
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_builder.viewsets import DynamicModelViewSet
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

# Definição das rotas para a API dinâmica
urlpatterns = [
    # Rota para listar e criar objetos
    path('<str:app>/<str:model>/', 
         DynamicModelViewSet.as_view({
             'get': 'list',    # Listar todos os objetos
             'post': 'create'  # Criar um novo objeto
         }), 
         name='dynamic-model-list'),
    
    # Rota para recuperar, atualizar e excluir objetos específicos
    path('<str:app>/<str:model>/<int:pk>/', 
         DynamicModelViewSet.as_view({
             'get': 'retrieve',         # Recuperar um objeto específico
             'patch': 'partial_update', # Atualizar parcialmente um objeto
             'put': 'update',           # Atualizar um objeto completo
             'delete': 'destroy'        # Excluir um objeto
         }), 
         name='dynamic-model-detail'),
]

def register_dynamic_api(router=None):
    """
    Registra a API dinâmica em um router existente ou cria um novo.
    
    Args:
        router (DefaultRouter, optional): Router existente para registrar as rotas.
            Se None, um novo router será criado.
            
    Returns:
        DefaultRouter: O router com as rotas registradas.
        
    Raises:
        Exception: Se ocorrer um erro ao registrar as rotas.
        
    Example:
        # Em urls.py do projeto
        from django.urls import path, include
        from api.routers import register_dynamic_api
        
        router = register_dynamic_api()
        
        urlpatterns = [
            path('api/', include(router.urls)),
        ]
    """
    try:
        if router is None:
            router = DefaultRouter()
        
        # Adiciona as rotas da API dinâmica ao router
        router.registry.extend([
            ('dynamic', DynamicModelViewSet, 'dynamic'),
        ])
        
        return router
    except Exception as e:
        logger.error(f"Erro ao registrar API dinâmica: {str(e)}")
        # Como esta função é usada na inicialização, repassar o erro é adequado
        # para que o problema seja identificado durante a configuração do projeto
        raise Exception(f"Falha ao registrar API dinâmica: {str(e)}")