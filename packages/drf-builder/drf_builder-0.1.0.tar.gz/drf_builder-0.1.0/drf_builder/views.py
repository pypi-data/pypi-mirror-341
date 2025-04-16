"""
Views da API Dinâmica.

Este módulo contém as views utilizadas pela API Dinâmica,
permitindo operações CRUD genéricas em modelos Django.
"""

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from drf_builder.utils import get_schema_info
from drf_builder.exceptions import ModelNotFoundError, OperationError

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schema_view(request):
    """
    Endpoint para obtenção de schema de modelos do sistema.
    
    Query Parameters:
        app: Nome do aplicativo (obrigatório)
        model: Nome do modelo (opcional)
        id: ID do objeto específico (opcional, requer model)
    
    Returns:
        Response: Informações de schema no formato JSON.
    """
    app_name = request.query_params.get('app')
    model_name = request.query_params.get('model')
    obj_id = request.query_params.get('id')
    
    if not app_name:
        return Response(
            {"error": "O parâmetro 'app' é obrigatório"},
            status=400
        )
    
    try:
        # Converter obj_id para inteiro se fornecido
        if obj_id:
            try:
                obj_id = int(obj_id)
            except ValueError:
                return Response(
                    {"error": "O parâmetro 'id' deve ser um número inteiro válido"},
                    status=400
                )
        
        schema_info = get_schema_info(
            app_name=app_name,
            model_name=model_name,
            obj_id=obj_id
        )
        
        return Response(schema_info)
        
    except ModelNotFoundError as e:
        return Response({"error": str(e)}, status=404)
    except ObjectDoesNotExist as e:
        return Response({"error": str(e)}, status=404)
    except OperationError as e:
        return Response({"error": e.detail, "reason": e.reason}, status=400)
    except Exception as e:
        return Response({"error": f"Erro inesperado: {str(e)}"}, status=500)