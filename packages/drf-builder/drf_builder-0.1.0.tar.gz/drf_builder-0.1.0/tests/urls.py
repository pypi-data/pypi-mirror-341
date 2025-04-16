"""
URLs para os testes.
"""
from django.urls import path, include
from drf_builder.routers import register_dynamic_api

# Registra a API dinâmica para testes
router = register_dynamic_api()

urlpatterns = [
    path('api/', include(router.urls)),
]