"""
Utilitários para a API Dinâmica.

Este módulo fornece funções auxiliares para a API Dinâmica,
facilitando operações comuns e melhorando a organização do código.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from django.db import models
from drf_builder.exceptions import (
    RelatedObjectNotFoundError,
    ModelNotFoundError,
    OperationError,
    InvalidRelationshipError
)
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

def resolve_foreign_keys(model, data):
    """
    Substitui IDs em campos ForeignKey por instâncias relacionadas.
    
    Args:
        model: O modelo ao qual os dados pertencem.
        data: Dicionário com os dados do modelo.
        
    Returns:
        dict: Dados atualizados com instâncias ForeignKey.
        
    Raises:
        RelatedObjectNotFoundError: Se um objeto relacionado não for encontrado.
        OperationError: Se ocorrer um erro inesperado durante a resolução.
    """
    resolved_data = data.copy()
    
    try:
        for field in model._meta.get_fields():
            if field.is_relation and not field.auto_created and field.many_to_one:
                field_name = field.name
                if field_name in resolved_data and resolved_data[field_name] is not None:
                    related_model = field.related_model
                    related_id = resolved_data[field_name]
                    
                    try:
                        # Substitui o ID pelo objeto correspondente
                        resolved_data[field_name] = related_model.objects.get(pk=related_id)
                    except ObjectDoesNotExist:
                        # Usar a exceção personalizada diretamente
                        raise RelatedObjectNotFoundError(
                            model_name=related_model.__name__,
                            object_id=related_id,
                            field_name=field_name
                        )
        return resolved_data
    except RelatedObjectNotFoundError:
        # Repassar exceções específicas
        raise
    except Exception as e:
        logger.error(f"Erro ao resolver chaves estrangeiras: {str(e)}")
        # Usar OperationError em vez de ValidationError genérica
        raise OperationError(
            detail="Erro ao processar relacionamentos",
            operation="resolve_foreign_keys",
            reason=str(e),
            source="drf_builder.utils"
        )

def get_model_from_names(app_label, model_name):
    """
    Obtém um modelo Django a partir do nome do aplicativo e do modelo.
    
    Args:
        app_label (str): Nome do aplicativo Django.
        model_name (str): Nome do modelo.
        
    Returns:
        Model: O modelo Django correspondente.
        
    Raises:
        ModelNotFoundError: Se o modelo não for encontrado.
    """
    # Normaliza o nome do modelo para capitalizar apenas a primeira letra
    normalized_model_name = model_name[0].upper() + model_name[1:].lower()
    
    try:
        # Tenta obter o modelo do app especificado
        return apps.get_model(app_label=app_label, model_name=normalized_model_name)
    except LookupError:
        try:
            # Tenta buscar o modelo no app "core" como fallback
            return apps.get_model(app_label="core", model_name=normalized_model_name)
        except LookupError:
            # Lança a exceção personalizada diretamente
            raise ModelNotFoundError(model_name, app_label)

def build_nested_results(queryset, group_by_fields):
    """
    Constrói resultados aninhados para agrupamento.
    
    Args:
        queryset: O queryset com os resultados agrupados.
        group_by_fields: Lista de campos para agrupar.
        
    Returns:
        list: Resultados aninhados.
        
    Raises:
        OperationError: Se ocorrer um erro durante o processamento do aninhamento.
    """
    try:
        results = []
        for item in queryset:
            current_level = results
            for i, field in enumerate(group_by_fields):
                value = item[field]
                found = False
                
                for entry in current_level:
                    if entry.get(field) == value:
                        # Se for o último campo, adiciona a contagem
                        if i == len(group_by_fields) - 1:
                            entry["count"] = item["count"]
                        
                        current_level = entry.setdefault("children", [])
                        found = True
                        break
                
                if not found:
                    new_entry = {field: value}
                    
                    # Se for o último campo, adiciona a contagem
                    if i == len(group_by_fields) - 1:
                        new_entry["count"] = item["count"]
                    else:
                        new_entry["children"] = []
                    
                    current_level.append(new_entry)
                    current_level = new_entry.get("children", [])

        return results
    except Exception as e:
        logger.error(f"Erro ao construir resultados aninhados: {str(e)}")
        raise OperationError(
            detail="Erro ao construir resultados aninhados",
            operation="build_nested_results",
            reason=str(e),
            source="drf_builder.utils"
        )

def get_schema_info(app_name=None, model_name=None, obj_id=None):
    """
    Retorna o schema das tabelas de um app, de uma tabela específica ou de um objeto.
    
    Args:
        app_name (str, opcional): Nome do aplicativo Django.
        model_name (str, opcional): Nome do modelo específico.
        obj_id (int, opcional): ID do objeto específico.
        
    Returns:
        dict: Informações do schema, contendo campos e seus tipos, além de relações de chave estrangeira.
        
    Raises:
        ModelNotFoundError: Se o modelo especificado não for encontrado.
        ObjectDoesNotExist: Se o objeto especificado não for encontrado.
        OperationError: Se ocorrer um erro durante a obtenção do schema.
    """
    try:
        result = {}
        
        # Caso 1: Schema de todas as tabelas de um app
        if app_name and not model_name:
            app_models = apps.get_app_config(app_name).get_models()
            result = {}
            
            for model in app_models:
                model_schema = _get_model_schema(model)
                result[model.__name__] = model_schema
                
        # Caso 2: Schema de uma tabela específica
        elif app_name and model_name:
            model = get_model_from_names(app_name, model_name)
            result = _get_model_schema(model)
            
            # Caso 3: Schema de um objeto específico
            if obj_id:
                try:
                    obj = model.objects.get(pk=obj_id)
                    result['instance_values'] = {
                        field.name: getattr(obj, field.name) 
                        for field in model._meta.fields
                    }
                except ObjectDoesNotExist:
                    raise ObjectDoesNotExist(f"Objeto {model_name} com id={obj_id} não encontrado")
                    
        else:
            raise OperationError(
                detail="Parâmetros insuficientes para consultar schema",
                operation="get_schema_info",
                reason="É necessário fornecer pelo menos o nome do app",
                source="drf_builder.utils"
            )
            
        return result
        
    except ModelNotFoundError:
        # Repassar exceção específica
        raise
    except ObjectDoesNotExist:
        # Repassar exceção específica
        raise
    except Exception as e:
        logger.error(f"Erro ao obter schema: {str(e)}")
        raise OperationError(
            detail="Erro ao obter informações de schema",
            operation="get_schema_info",
            reason=str(e),
            source="drf_builder.utils"
        )

def _get_model_schema(model):
    """
    Função auxiliar para obter o schema de um modelo específico.
    
    Args:
        model: Modelo Django.
        
    Returns:
        dict: Schema do modelo com campos, tipos e relações.
    """
    schema = {
        'fields': {},
        'foreign_keys': {}
    }
    
    for field in model._meta.get_fields():
        # Ignora campos de relações reversas
        if field.auto_created and not field.concrete:
            continue
            
        # Obtém o tipo do campo
        field_type = field.get_internal_type() if hasattr(field, 'get_internal_type') else type(field).__name__
        
        # Registra o campo no schema
        schema['fields'][field.name] = field_type
        
        # Registra chaves estrangeiras
        if field.is_relation and field.many_to_one:
            related_model = field.related_model
            schema['foreign_keys'][field.name] = {
                'model': related_model.__name__,
                'app': related_model._meta.app_label
            }
            
    return schema