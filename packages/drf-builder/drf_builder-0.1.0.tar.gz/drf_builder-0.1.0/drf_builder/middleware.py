"""
Middleware para tratamento padronizado de exceções na API.

Este módulo fornece um middleware para capturar e formatar exceções
lançadas pela API, garantindo respostas consistentes para erros.

O middleware transforma diferentes tipos de exceções em respostas JSON formatadas,
oferecendo informações detalhadas para facilitar a depuração e solução de problemas.

Exceções suportadas:
- ModelNotFoundError: Quando um modelo não é encontrado
- RelatedObjectNotFoundError: Quando um objeto relacionado não existe
- InvalidRelationshipError: Quando um relacionamento é inválido
- NestedObjectError: Quando há problemas com objetos aninhados
- InvalidFilterError: Quando um filtro é inválido
- InvalidDepthError: Quando a profundidade solicitada é inválida
- OperationError: Erros genéricos em operações
- ValidationError: Erros de validação de dados

Cada tipo de exceção gera um formato padronizado de resposta com detalhes
relevantes para identificação e correção do problema encontrado.
"""

import logging
import traceback
import json
import re
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import APIException, ValidationError
from rest_framework import status

from drf_builder.exceptions import (
    ModelNotFoundError, 
    OperationError, 
    InvalidRelationshipError, 
    RelatedObjectNotFoundError, 
    NestedObjectError, 
    InvalidFilterError, 
    InvalidDepthError
)

# Configuração de logging
logger = logging.getLogger(__name__)

# Mapeamento entre classes de exceção e códigos HTTP
EXCEPTION_STATUS_CODE_MAP = {
    ModelNotFoundError: status.HTTP_404_NOT_FOUND,
    RelatedObjectNotFoundError: status.HTTP_404_NOT_FOUND,
    InvalidRelationshipError: status.HTTP_400_BAD_REQUEST,
    NestedObjectError: status.HTTP_400_BAD_REQUEST,
    InvalidFilterError: status.HTTP_400_BAD_REQUEST,
    InvalidDepthError: status.HTTP_400_BAD_REQUEST,
    OperationError: status.HTTP_400_BAD_REQUEST,
    ValidationError: status.HTTP_400_BAD_REQUEST,
}


def api_exception_handler(exc, context):
    """
    Função personalizada para manipulação de exceções da API.
    
    Esta função estende o tratamento de exceções padrão do DRF,
    fornecendo um formato consistente para todas as respostas de erro.
    
    Args:
        exc (Exception): A exceção que foi lançada
        context (dict): O contexto da exceção
        
    Returns:
        Response: Uma resposta HTTP formatada contendo informações do erro
    """
    # Usar o manipulador de exceções do DRF primeiro
    response = drf_exception_handler(exc, context)
    
    # Se já temos uma resposta, não precisamos fazer nada
    if response is not None:
        return response

    # Para exceções não tratadas pelo DRF, criar uma resposta personalizada
    if isinstance(exc, Exception):
        status_code = EXCEPTION_STATUS_CODE_MAP.get(
            exc.__class__, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        error_data = {
            "message": str(exc),
            "type": exc.__class__.__name__,
        }
        
        # Registrar exceção não tratada
        logger.error(
            f"Exceção não tratada: {exc.__class__.__name__}, Mensagem: {str(exc)}",
            exc_info=True
        )
        
        return JsonResponse(error_data, status=status_code)
    
    return None


class APIExceptionMiddleware:
    """
    Middleware para capturar e formatar exceções lançadas pela API.
    
    Este middleware garante que todas as exceções sejam capturadas e 
    formatadas de maneira consistente, com informações úteis para
    diagnóstico de problemas.
    """
    
    def __init__(self, get_response):
        """
        Inicializa o middleware.
        
        Args:
            get_response: A próxima função/middleware na cadeia de requisição
        """
        self.get_response = get_response
        
    def __call__(self, request):
        """
        Processa a requisição e captura exceções.
        
        Args:
            request: A requisição HTTP
            
        Returns:
            HttpResponse: A resposta HTTP
        """
        try:
            response = self.get_response(request)
            return response
        except Exception as exc:
            # Não tratar exceções para requisições que não são da API
            if not request.path.startswith('/api/'):
                raise
            
            return self.handle_exception(request, exc)
    
    def handle_exception(self, request, exc):
        """
        Manipula exceções lançadas durante o processamento de requisições da API.
        
        Args:
            request: A requisição HTTP
            exc: A exceção que foi lançada
            
        Returns:
            JsonResponse: Uma resposta JSON formatada com informações do erro
        """
        # Prepara o contexto para o handler de exceções
        context = {
            'view': getattr(request, 'view', None),
            'request': request,
        }
        
        # Verifica se é uma exceção personalizada da API
        if isinstance(exc, APIException):
            error_data = self.format_api_exception(exc)
            status_code = exc.status_code
        else:
            # Para qualquer outra exceção
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_data = self.format_unexpected_exception(exc, request)
        
        # Registrar erro
        logger.error(
            f"API Error: {error_data.get('message')}",
            extra={
                'path': request.path,
                'method': request.method,
                'error_data': error_data,
            },
            exc_info=True
        )
        
        return JsonResponse(error_data, status=status_code)
    
    def format_api_exception(self, exc):
        """
        Formata exceções da API para um formato padronizado.
        
        Args:
            exc (APIException): A exceção a ser formatada
            
        Returns:
            dict: Os dados formatados do erro
        """
        # Tratamento especial para NestedObjectError
        if isinstance(exc, NestedObjectError):
            return self.format_nested_object_error(exc)
            
        if hasattr(exc, 'get_full_details'):
            details = exc.get_full_details()
        elif hasattr(exc, 'detail'):
            details = exc.detail
        else:
            details = str(exc)
        
        error_data = {
            "message": str(exc),
            "type": exc.__class__.__name__,
            "details": details
        }
        
        # Adicionar código para identificação do erro
        if hasattr(exc, 'default_code'):
            error_data["code"] = exc.default_code
        
        # Adicionar contexto para exceções personalizadas
        if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
            if 'context' in exc.detail:
                error_data["context"] = exc.detail['context']
                
        # Tratamento especial para erros de validação em campos não nulos
        if isinstance(exc, ValidationError) and hasattr(exc, 'detail'):
            error_data = self.enhance_validation_error(exc, error_data)
        
        return error_data
    
    def format_nested_object_error(self, exc):
        """
        Formata erros específicos de objetos aninhados.
        
        Args:
            exc (NestedObjectError): A exceção de objeto aninhado
            
        Returns:
            dict: Os dados formatados do erro
        """
        message = str(exc)
        context = {}
        
        # Extrai informações do contexto se disponíveis
        if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                if isinstance(value, dict) and 'context' in value:
                    context = value['context']
                    if 'message' in value:
                        message = value['message']
        
        # Identifica campos obrigatórios faltantes
        missing_fields = self.extract_missing_fields_from_message(message)
        
        # Constrói uma mensagem de erro mais amigável
        if missing_fields:
            field_path = context.get('path', '')
            relation_field = context.get('relation_field', '')
            
            # Identificar modelo relacionado e índice
            model_name = ""
            if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
                for field, details in exc.detail.items():
                    if isinstance(details, dict) and 'path' in details:
                        parts = details['path'].split('[')
                        if len(parts) > 0:
                            model_name = parts[0]
                            break
            
            # Cria uma mensagem mais clara
            if model_name:
                friendly_message = f"Campos obrigatórios faltando em {model_name}: {', '.join(missing_fields)}"
            else:
                friendly_message = f"Campos obrigatórios faltando: {', '.join(missing_fields)}"
            
            # Atualiza o contexto com informações mais úteis
            updated_context = context.copy()
            updated_context['missing_fields'] = missing_fields
            
            return {
                relation_field: {
                    "message": friendly_message,
                    "path": field_path,
                    "context": updated_context
                }
            }
        
        # Se não identificarmos campos específicos, retornamos o erro original
        return {
            key: {
                "message": message,
                "path": context.get('path', ''),
                "context": context
            } for key, value in exc.detail.items() if isinstance(value, dict)
        }
    
    def extract_missing_fields_from_message(self, message):
        """
        Extrai campos obrigatórios faltantes de uma mensagem de erro.
        
        Args:
            message (str): A mensagem de erro
            
        Returns:
            list: Lista de campos obrigatórios faltantes
        """
        # Padrões comuns para erros de nulo em violação de constraint
        null_pattern = r"null value in column \"(\w+)\" of relation"
        not_null_match = re.search(null_pattern, message)
        
        if not_null_match:
            return [not_null_match.group(1)]
            
        # Padrão para erros de integridade (campo não fornecido)
        integrity_pattern = r"violates not-null constraint.*column: (\w+)"
        integrity_match = re.search(integrity_pattern, message)
        
        if integrity_match:
            return [integrity_match.group(1)]
        
        # Outros padrões podem ser adicionados conforme necessário
        
        return []
    
    def enhance_validation_error(self, exc, error_data):
        """
        Melhora a formatação dos erros de validação.
        
        Args:
            exc (ValidationError): A exceção de validação
            error_data (dict): Os dados do erro já formatados
            
        Returns:
            dict: Os dados do erro com formatação aprimorada
        """
        if not hasattr(exc, 'detail'):
            return error_data
        
        detail = exc.detail
        
        # Se for um dicionário de erros por campo
        if isinstance(detail, dict):
            # Formata as mensagens por campo
            formatted_errors = {}
            for field, errors in detail.items():
                if isinstance(errors, list):
                    # Converte lista de erros em uma única mensagem
                    formatted_errors[field] = ", ".join([str(error) for error in errors])
                else:
                    formatted_errors[field] = errors
                    
            error_data["fields"] = formatted_errors
            
            # Cria uma mensagem resumida
            field_errors = []
            for field, message in formatted_errors.items():
                if field != 'non_field_errors':
                    field_errors.append(f"{field}: {message}")
            
            if field_errors:
                error_data["message"] = "Erro de validação: " + "; ".join(field_errors)
        
        return error_data
    
    def format_unexpected_exception(self, exc, request):
        """
        Formata exceções inesperadas para um formato padronizado.
        
        Args:
            exc (Exception): A exceção a ser formatada
            request: A requisição HTTP
            
        Returns:
            dict: Os dados formatados do erro
        """
        error_data = {
            "message": "Ocorreu um erro interno no servidor.",
            "type": exc.__class__.__name__,
        }
        
        # Em ambiente de desenvolvimento, incluir mais detalhes
        if settings.DEBUG:
            error_data.update({
                "detail": str(exc),
                "traceback": traceback.format_exc().split("\n"),
                "request": {
                    "method": request.method,
                    "path": request.path,
                    "query_params": dict(request.GET),
                    "content_type": request.content_type,
                }
            })
            
            # Se o corpo da requisição for JSON, adicionar ao contexto
            if request.content_type == 'application/json':
                try:
                    body = json.loads(request.body.decode('utf-8'))
                    # Remove campos sensíveis
                    if 'password' in body:
                        body['password'] = '[REDACTED]'
                    error_data["request"]["body"] = body
                except Exception:
                    pass
        
        return error_data
