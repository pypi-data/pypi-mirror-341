"""
Serializers para a API Dinâmica.

Este módulo define os serializers para a API Dinâmica, permitindo
a serialização e deserialização dinâmica de qualquer modelo Django.
"""

from rest_framework import serializers
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist, ValidationError as DjangoValidationError
from django.core.validators import MaxLengthValidator
from django.db import transaction
import logging

from drf_builder.exceptions import (
    ModelNotFoundError, 
    OperationError, 
    InvalidRelationshipError
)
from drf_builder.utils import get_model_from_names

# Configuração de logging
logger = logging.getLogger(__name__)

class DynamicSerializer(serializers.ModelSerializer):
    """
    Serializer dinâmico que cria um serializer para qualquer modelo baseado no nome passado.
    
    Este serializer permite a criação dinâmica de serializers para qualquer modelo
    Django, facilitando a criação de APIs RESTful sem a necessidade de definir
    serializers específicos para cada modelo.
    
    Attributes:
        model_name (str): Nome do modelo a ser serializado.
        app_label (str): Nome do aplicativo Django onde o modelo está definido.
        depth (int): Nível de profundidade para serialização de relações.
        fields (list): Lista de campos específicos a serem incluídos.
    """
    def __init__(self, *args, model_name=None, app_label=None, depth=0, fields=None, **kwargs):
        if not model_name:
            raise OperationError(
                detail="Nome do modelo é obrigatório",
                operation="DynamicSerializer.__init__",
                reason="model_name não foi fornecido",
                code="missing_model_name"
            )
        
        if not app_label:
            raise OperationError(
                detail="Nome do aplicativo é obrigatório",
                operation="DynamicSerializer.__init__",
                reason="app_label não foi fornecido",
                code="missing_app_label"
            )
        
        # Obtém o modelo usando a função auxiliar
        model = get_model_from_names(app_label, model_name)
        
        # Define os campos do serializer
        model_fields = "__all__"
        if fields is not None:
            model_fields = fields

        # Configura dinamicamente os campos
        Meta = type("Meta", (object,), {
            "model": model,
            "fields": model_fields,
            "depth": depth,
        })
        self.Meta = Meta
        
        # Armazena informações para uso posterior
        self.model_name = model_name
        self.app_label = app_label
        self.depth_value = depth
        self.selected_fields = fields
        
        super().__init__(*args, **kwargs)
        
        # Adiciona validações personalizadas para campos específicos
        self._add_field_validations()
        
    def _add_field_validations(self):
        """
        Adiciona validações personalizadas para campos específicos do modelo.
        
        Este método analisa os campos do modelo e adiciona validações apropriadas
        com base no tipo de campo.
        """
        model = self.Meta.model
        
        for field_name, field in self.fields.items():
            try:
                model_field = model._meta.get_field(field_name)
                
                # Adiciona validação de tamanho máximo para campos de texto
                if hasattr(model_field, 'max_length') and model_field.max_length:
                    field.validators.append(
                        MaxLengthValidator(
                            model_field.max_length,
                            message=f"O campo '{field_name}' não pode ter mais que {model_field.max_length} caracteres."
                        )
                    )
                
                # Adiciona validação para campos numéricos
                if hasattr(model_field, 'validators'):
                    field.validators.extend(model_field.validators)
                    
            except FieldDoesNotExist:
                # Ignora campos que não existem diretamente no modelo (podem ser propriedades)
                pass
        
    @classmethod
    def create_inline_serializer(cls, related_model_name, app_label=None, depthParam=0, fields=None):
        """
        Cria dinamicamente serializers para relacionamentos reversos.
        
        Args:
            related_model_name (str): Nome do modelo relacionado.
            app_label (str): Nome do aplicativo onde o modelo está definido.
            depthParam (int): Nível de profundidade para serialização de relações.
            fields (list): Lista opcional de campos a incluir.
            
        Returns:
            class: Uma classe de serializer para o modelo relacionado.
            
        Raises:
            ModelNotFoundError: Se o modelo relacionado não for encontrado.
        """
        try:
            # Obtém o modelo relacionado usando a função auxiliar
            related_model = get_model_from_names(app_label, related_model_name)
            
            # Define os campos do serializer
            model_fields = "__all__"
            if fields is not None:
                model_fields = fields

            class InlineSerializer(serializers.ModelSerializer):
                """Serializer interno para modelos relacionados."""
                class Meta:
                    model = related_model
                    fields = model_fields
                    depth = depthParam or 0

            return InlineSerializer
            
        except ModelNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro ao criar serializer inline para {related_model_name}: {str(e)}")
            raise OperationError(
                detail=f"Erro ao criar serializer para modelo relacionado",
                operation="create_inline_serializer",
                reason=str(e),
                source="DynamicSerializer"
            )
    
    def create(self, validated_data):
        """
        Cria uma instância do modelo com os dados validados.
        
        Args:
            validated_data (dict): Dados validados para criar a instância.
            
        Returns:
            Model: A instância do modelo criada.
            
        Raises:
            OperationError: Se ocorrer um erro durante a criação.
        """
        model_name = self.Meta.model.__name__
        
        try:
            # Usa uma transação para garantir atomicidade
            with transaction.atomic():
                instance = self.Meta.model.objects.create(**validated_data)
                logger.info(f"Criado {model_name} com ID {instance.pk}")
                return instance
        except DjangoValidationError as e:
            logger.error(f"Erro de validação ao criar {model_name}: {str(e)}")
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else {"non_field_errors": [str(e)]})
        except Exception as e:
            logger.error(f"Erro ao criar {model_name}: {str(e)}")
            raise OperationError(
                detail=f"Erro ao criar objeto",
                operation="create",
                reason=str(e),
                source=f"DynamicSerializer.{model_name}",
                data={"model": model_name}
            )
            
    def update(self, instance, validated_data):
        """
        Atualiza uma instância existente do modelo com os dados validados.
        
        Args:
            instance: A instância do modelo a ser atualizada.
            validated_data (dict): Dados validados para atualizar a instância.
            
        Returns:
            Model: A instância do modelo atualizada.
            
        Raises:
            OperationError: Se ocorrer um erro durante a atualização.
        """
        model_name = self.Meta.model.__name__
        
        try:
            # Usa uma transação para garantir atomicidade
            with transaction.atomic():
                # Atualiza cada campo fornecido
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                
                # Salva as alterações
                instance.save()
                logger.info(f"Atualizado {model_name} com ID {instance.pk}")
                return instance
        except DjangoValidationError as e:
            logger.error(f"Erro de validação ao atualizar {model_name}: {str(e)}")
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else {"non_field_errors": [str(e)]})
        except Exception as e:
            logger.error(f"Erro ao atualizar {model_name}: {str(e)}")
            raise OperationError(
                detail=f"Erro ao atualizar objeto",
                operation="update",
                reason=str(e),
                source=f"DynamicSerializer.{model_name}",
                data={"model": model_name, "id": instance.pk}
            )
            
    def to_representation(self, instance):
        """
        Converte uma instância do modelo em uma representação serializável.
        
        Este método personalizado permite adicionar campos calculados ou
        modificar a representação padrão dos dados.
        
        Args:
            instance: A instância do modelo a ser serializada.
            
        Returns:
            dict: A representação serializada da instância.
        """
        try:
            # Obtém a representação padrão
            representation = super().to_representation(instance)
            
            # Só adiciona metadados se include_meta for True
            if getattr(self, 'include_meta', False):
                representation['_meta'] = {
                    'model': self.model_name,
                    'app': self.app_label
                }
                
                # Se temos campos específicos, indicamos quais foram selecionados
                if hasattr(self, 'selected_fields') and self.selected_fields is not None:
                    representation['_meta']['selected_fields'] = self.selected_fields
            
            return representation
        except Exception as e:
            logger.error(f"Erro ao serializar {self.model_name}: {str(e)}")
            # Não lançamos exceção aqui para não interromper a resposta,
            # mas registramos o erro para investigação
            error_response = {
                'error': f"Erro ao serializar {self.model_name}",
                'id': getattr(instance, 'pk', None)
            }
            
            # Mesmo no caso de erro, respeita a configuração de include_meta
            if getattr(self, 'include_meta', False):
                error_response['_meta'] = {'model': self.model_name, 'app': self.app_label}
                
            return error_response