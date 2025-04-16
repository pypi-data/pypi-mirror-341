"""
Exceções personalizadas para a API Dinâmica.

Este módulo define exceções personalizadas para a API Dinâmica,
fornecendo mensagens de erro claras e informativas para os usuários.
"""

from rest_framework.exceptions import NotFound, ValidationError, APIException
from rest_framework import status

class ModelNotFoundError(NotFound):
    """
    Exceção lançada quando um modelo não é encontrado.
    
    Attributes:
        model_name (str): Nome do modelo que não foi encontrado.
        app_label (str): Nome do aplicativo onde o modelo deveria estar.
    """
    default_detail = "O modelo especificado não foi encontrado."
    default_code = "model_not_found"

    def __init__(self, model_name, app_label):
        detail = f"Modelo '{model_name}' não encontrado no app '{app_label}' nem no app 'core'."
        super().__init__(detail)

class InvalidRelationshipError(ValidationError):
    """
    Exceção lançada quando um relacionamento inválido é especificado.
    
    Attributes:
        field_name (str): Nome do campo de relacionamento inválido.
        model_name (str): Nome do modelo ao qual o campo deveria pertencer.
    """
    def __init__(self, field_name, model_name):
        detail = f"O campo '{field_name}' não é um relacionamento válido para o modelo '{model_name}'."
        super().__init__({field_name: detail})

class RelatedObjectNotFoundError(ValidationError):
    """
    Exceção lançada quando um objeto relacionado não é encontrado.
    
    Attributes:
        model_name (str): Nome do modelo do objeto relacionado.
        object_id: ID do objeto relacionado que não foi encontrado.
        field_name (str, optional): Nome do campo que contém o relacionamento.
    """
    default_code = 'related_object_not_found'
    
    def __init__(self, model_name, object_id, field_name=None):
        context = {
            "model": model_name,
            "id": str(object_id),
            "code": self.default_code
        }
        
        if field_name:
            message = f"Não foi possível encontrar {model_name} com ID {object_id} para o campo '{field_name}'."
            context["field"] = field_name
        else:
            message = f"Não foi possível encontrar {model_name} com ID {object_id}."
            
        super().__init__({"detail": message, "context": context})

class NestedObjectError(ValidationError):
    """
    Exceção lançada quando ocorre um erro ao processar um objeto aninhado.
    
    Attributes:
        relation_field (str): Nome do campo de relacionamento.
        index (int, optional): Índice do objeto na lista (caso seja uma lista).
        field (str, optional): Campo específico que causou o erro.
        message (str, optional): Mensagem detalhada do erro.
        errors (dict, optional): Detalhes específicos dos erros encontrados.
    """
    default_code = 'nested_object_error'
    
    def __init__(self, relation_field, index=None, field=None, message=None, errors=None):
        path = relation_field
        if index is not None:
            path += f"[{index}]"
        if field:
            path += f".{field}"
        
        error_message = message or "Erro ao processar objeto aninhado"
        
        # Extrair informações sobre campos obrigatórios faltantes
        missing_fields = []
        if message and "violates not-null constraint" in message:
            import re
            null_pattern = r"null value in column \"(\w+)\" of relation"
            match = re.search(null_pattern, message)
            if match:
                missing_fields.append(match.group(1))
                error_message = f"Campo obrigatório faltando: {match.group(1)}"
        
        context = {
            "path": path,
            "relation_field": relation_field,
            "code": self.default_code
        }
        
        if index is not None:
            context["index"] = index
        if field:
            context["field"] = field
        if errors:
            context["errors"] = errors
        if missing_fields:
            context["missing_fields"] = missing_fields
            
        detail = {
            "message": error_message,
            "path": path,
            "context": context
        }
        
        super().__init__({relation_field: detail})

class OperationError(APIException):
    """
    Exceção genérica para erros de operação.
    
    Attributes:
        detail (str): Descrição detalhada do erro.
        operation (str, optional): Nome da operação que falhou.
        reason (str, optional): Razão específica da falha.
        source (str, optional): Origem/componente onde ocorreu o erro.
        data (dict, optional): Dados adicionais relacionados ao erro.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Ocorreu um erro durante a operação."
    default_code = "operation_error"
    
    def __init__(self, detail=None, operation=None, reason=None, source=None, data=None, code=None):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code
        
        error_context = {}
        if operation:
            error_context["operation"] = operation
        if reason:
            error_context["reason"] = reason
        if source:
            error_context["source"] = source
        if data:
            error_context["data"] = data
            
        if error_context:
            self.detail = {"message": self.detail, "context": error_context, "code": self.code}
        
        super().__init__(self.detail)

class InvalidFilterError(ValidationError):
    """
    Exceção lançada quando um filtro inválido é especificado.
    
    Attributes:
        filter_name (str): Nome do filtro inválido.
        reason (str): Razão pela qual o filtro é inválido.
    """
    def __init__(self, filter_name, reason):
        detail = f"Filtro inválido '{filter_name}': {reason}"
        super().__init__({"filter": detail})

class InvalidDepthError(ValidationError):
    """
    Exceção lançada quando um valor de profundidade inválido é especificado.
    
    Attributes:
        depth_value: Valor de profundidade inválido.
        reason (str): Razão pela qual o valor é inválido.
    """
    def __init__(self, depth_value, reason):
        detail = f"Valor de profundidade inválido '{depth_value}': {reason}"
        super().__init__({"depth": detail})