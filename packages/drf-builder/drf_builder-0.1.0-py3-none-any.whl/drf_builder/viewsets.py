"""
ViewSets para a API Dinâmica.

Este módulo define os ViewSets para a API Dinâmica, permitindo
operações CRUD em qualquer modelo Django através de endpoints RESTful.
"""

from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist, FieldError
from rest_framework import viewsets, response, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from django.conf import settings

from drf_builder.serializers import DynamicSerializer
from drf_builder.exceptions import (
    ModelNotFoundError, InvalidRelationshipError, 
    RelatedObjectNotFoundError, OperationError,
    InvalidFilterError, InvalidDepthError,
    NestedObjectError
)
from drf_builder.utils import resolve_foreign_keys, get_model_from_names, build_nested_results

import logging

# Configuração de logging
logger = logging.getLogger(__name__)

"""
ViewSet dinâmico para trabalhar com qualquer modelo especificado pela URL.

Este ViewSet permite a criação de endpoints RESTful para qualquer modelo
Django sem a necessidade de definir ViewSets específicos para cada modelo.
    
Suporta:
- Listagem, criação, recuperação, atualização e exclusão de registros
- Filtragem de registros
- Agrupamento de resultados
- Operações aninhadas (nested) para relacionamentos
- Controle de profundidade de serialização
- Seleção de campos específicos para retorno
    
Parâmetros de URL:
    app (str): Nome do aplicativo Django onde o modelo está definido.
    model (str): Nome do modelo a ser manipulado.
    pk (int): ID do objeto para operações específicas (retrieve, update, delete).
        
Parâmetros de consulta:
    depth (int): Nível de profundidade para serialização de relações (padrão: 0).
    group_by (str): Campos para agrupar resultados, separados por vírgula.
    filter_* (str): Filtros para consulta (ex: filter_name=valor).
    fields (str): Campos específicos a serem retornados, separados por vírgula.
"""
class DynamicModelViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend]
    
    def get_model(self):
        """
        Obtém o modelo a partir dos parâmetros da URL.
        
        Returns:
            Model: O modelo Django correspondente.
            
        Raises:
            ModelNotFoundError: Se o modelo não for encontrado.
            ValidationError: Se os parâmetros necessários não forem fornecidos.
        """
        model_name = self.kwargs.get("model")
        app_label = self.kwargs.get("app")
        
        if not model_name:
            raise ValidationError({"model": "O nome do modelo é obrigatório."})
            
        if not app_label:
            raise ValidationError({"app": "O nome do aplicativo é obrigatório."})
        
        try:
            return get_model_from_names(app_label, model_name)
        except Exception:
            # Usar exceção personalizada em vez da genérica
            raise ModelNotFoundError(model_name, app_label)

    def get_queryset(self):
        """
        Obtém o queryset para o modelo especificado, aplicando filtros se necessário.
        
        Returns:
            QuerySet: O queryset filtrado.
            
        Raises:
            InvalidFilterError: Se ocorrer um erro durante a filtragem.
        """
        model = self.get_model()
        queryset = model.objects.all()
        
        # Aplica filtros dinâmicos baseados nos parâmetros de consulta
        for param, value in self.request.query_params.items():
            if param.startswith('filter_'):
                field_name = param[7:]  # Remove 'filter_' do nome do parâmetro
                filter_kwargs = {field_name: value}
                try:
                    queryset = queryset.filter(**filter_kwargs)
                except FieldError as e:
                    raise InvalidFilterError(field_name, str(e))
                except Exception as e:
                    logger.error(f"Erro ao aplicar filtro {field_name}: {str(e)}")
                    raise InvalidFilterError(field_name, f"Erro inesperado: {str(e)}")
                    
        return queryset

    def get_serializer_class(self):
        """
        Define dinamicamente o serializer baseado no DynamicSerializer.
        
        Returns:
            class: A classe do serializer configurada para o modelo.
            
        Raises:
            InvalidDepthError: Se ocorrer um erro no parâmetro de profundidade.
        """
        model_name = self.kwargs.get("model")
        app_label = self.kwargs.get("app")
        model = self.get_model()
        
        # Controle de profundidade baseado em parâmetros de consulta
        depth_param = self.request.query_params.get("depth", "0")
        try:
            depth = int(depth_param)
            if depth < 0 or depth > 10:  # Limita a profundidade para evitar problemas de desempenho
                raise InvalidDepthError(depth, "A profundidade deve estar entre 0 e 10.")
        except ValueError:
            raise InvalidDepthError(depth_param, "Deve ser um número inteiro válido.")

        # Configuração para seleção de campos específicos
        fields_param = self.request.query_params.get("fields", None)
        specific_fields = None
        
        if fields_param:
            fields_list = [field.strip() for field in fields_param.split(",")]
            
            # Verificar se os campos solicitados existem no modelo
            valid_fields = []
            invalid_fields = []
            
            # Obter todos os nomes de campos do modelo
            model_fields = [field.name for field in model._meta.get_fields()]
            
            for field in fields_list:
                if field == 'id' or field in model_fields:
                    valid_fields.append(field)
                else:
                    invalid_fields.append(field)
            
            if invalid_fields:
                logger.warning(f"Campos inválidos solicitados: {', '.join(invalid_fields)}")
            
            # Se temos campos válidos, definimos specific_fields
            if valid_fields:
                # Garantir que 'id' esteja sempre incluído
                if 'id' not in valid_fields:
                    valid_fields.insert(0, 'id')
                specific_fields = valid_fields

        # Obtém a configuração global para inclusão de metadados
        include_meta = getattr(settings, 'API_INCLUDE_META', True)

        # Configura serializers para relacionamentos
        related_serializers = {}
        if depth > 0:  # Configura relacionamentos apenas se a profundidade for maior que 0
            for field in model._meta.get_fields():
                if field.one_to_many or field.one_to_one:  # Detecta FK reversas
                    related_model_name = field.related_model._meta.model_name
                    related_app_label = field.related_model._meta.app_label
                    related_name = field.related_name or f"{related_model_name}_set"
                    
                    try:
                        # Não passa include_meta para os serializers relacionados
                        related_serializers[related_name] = DynamicSerializer.create_inline_serializer(
                            related_model_name, 
                            related_app_label, 
                            depthParam=max(depth - 1, 0)
                        )
                    except Exception as e:
                        logger.warning(f"Não foi possível criar serializer para {related_name}: {str(e)}")

        # Criar uma classe personalizada de serializer dinamicamente
        class CustomDynamicSerializer(DynamicSerializer):
            def __init__(self, *args, **kwargs):
                # Remove include_meta dos kwargs antes de passar para o parent
                include_meta_value = kwargs.pop('include_meta', include_meta)
                
                kwargs["model_name"] = model_name
                kwargs["app_label"] = app_label
                kwargs["depth"] = depth
                kwargs["fields"] = specific_fields
                super().__init__(*args, **kwargs)
                
                # Define include_meta depois da inicialização
                self.include_meta = include_meta_value

            # Adiciona os serializers relacionados com base na profundidade
            if depth > 0:
                for related_name, serializer in related_serializers.items():
                    locals()[related_name] = serializer(many=True, read_only=True)

        return CustomDynamicSerializer

    def get_object(self):
        """
        Recupera o objeto especificado pelo ID na URL.
        
        Returns:
            Model instance: A instância do modelo correspondente ao ID.
            
        Raises:
            RelatedObjectNotFoundError: Se o objeto não for encontrado.
        """
        try:
            return super().get_object()
        except Exception as e:
            logger.error(f"Erro ao recuperar objeto: {str(e)}")
            model_name = self.kwargs.get("model", "")
            pk = self.kwargs.get("pk", "")
            # Usar exceção personalizada para objetos não encontrados
            raise RelatedObjectNotFoundError(model_name, pk)
            
    def list(self, request, *args, **kwargs):
        """
        Lista os objetos do modelo, com suporte a agrupamento.
        
        Args:
            request: A requisição HTTP.
            
        Returns:
            Response: A resposta HTTP com os objetos listados.
            
        Raises:
            OperationError: Se ocorrer um erro durante a listagem.
            ValidationError: Se houver erro nos parâmetros de agrupamento.
        """
        group_by = request.query_params.get("group_by", None)
        fields_param = request.query_params.get("fields", None)

        try:
            if group_by:
                # Se temos campos específicos e agrupamento, aplicamos ambos
                if fields_param:
                    # Obter os campos para agrupamento
                    group_by_fields = group_by.split(",")
                    
                    # Obter campos específicos solicitados
                    fields_list = [field.strip() for field in fields_param.split(",")]
                    
                    # Garantir que todos os campos de agrupamento estejam nos campos selecionados
                    for group_field in group_by_fields:
                        if group_field not in fields_list:
                            fields_list.append(group_field)
                    
                    # Executar consulta agrupada apenas com os campos solicitados
                    queryset = self.get_queryset().values(*fields_list).annotate(count=Count("id"))
                else:
                    # Agrupamento normal sem seleção de campos
                    group_by_fields = group_by.split(",")
                    queryset = self.get_queryset().values(*group_by_fields).annotate(count=Count("id"))
                
                results = build_nested_results(queryset, group_by_fields)
                return response.Response(results)
            else:
                return super().list(request, *args, **kwargs)
        except FieldError as e:
            raise ValidationError({"group_by": f"Erro ao agrupar por campos: {str(e)}"})
        except Exception as e:
            logger.error(f"Erro ao listar objetos: {str(e)}")
            raise OperationError(
                detail="Erro ao listar objetos",
                operation="list",
                reason=str(e),
                source="DynamicModelViewSet"
            )
        
    def create(self, request, *args, **kwargs):
        """
        Cria um novo objeto com suporte a relacionamentos aninhados.
        
        Args:
            request: A requisição HTTP com os dados do objeto.
            
        Returns:
            Response: A resposta HTTP com o objeto criado.
            
        Raises:
            OperationError: Se ocorrer um erro durante a criação.
            InvalidRelationshipError: Se um relacionamento especificado for inválido.
            NestedObjectError: Se ocorrer um erro ao processar objetos aninhados.
        """
        data = request.data
        model = self.get_model()
        
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            # Extraindo dados relacionados antes de salvar o objeto principal
            related_fields = {}
            for field_name, value in list(data.items()):
                if isinstance(value, list):  # Detecta campos de relação reversa
                    related_fields[field_name] = data.pop(field_name)

            # Resolver campos ForeignKey de forma dinâmica
            resolved_data = resolve_foreign_keys(model, data)

            # Salvando o objeto principal
            instance = serializer.Meta.model.objects.create(**resolved_data)

            # Salvando objetos relacionados
            for field_name, values in related_fields.items():
                try:
                    related_manager = getattr(instance, field_name)  # Ex.: questao_set
                    if not hasattr(related_manager, 'create'):
                        raise InvalidRelationshipError(field_name, model.__name__)
                        
                    # Obtenha o modelo relacionado para descobrir campos obrigatórios
                    related_model = related_manager.model
                    required_fields = []
                    
                    # Identificar campos obrigatórios no modelo relacionado
                    for f in related_model._meta.get_fields():
                        if not f.auto_created and not f.blank and not f.null and not f.has_default() and f.concrete:
                            required_fields.append(f.name)
                    
                    if isinstance(values, list):
                        for index, item in enumerate(values):
                            try:
                                # Verificar se todos os campos obrigatórios estão presentes
                                missing_fields = []
                                for req_field in required_fields:
                                    # Ignorar o campo da FK relacionada ao modelo pai
                                    if req_field not in item and not any(
                                        f.name == req_field and f.related_model == model 
                                        for f in related_model._meta.get_fields() if f.is_relation
                                    ):
                                        missing_fields.append(req_field)
                                
                                if missing_fields:
                                    raise NestedObjectError(
                                        relation_field=field_name,
                                        index=index,
                                        message=f"Campos obrigatórios faltando: {', '.join(missing_fields)}",
                                        errors={"missing_fields": missing_fields}
                                    )
                                    
                                item = resolve_foreign_keys(related_manager.model, item)
                                related_manager.create(**item)  # Cria cada item relacionado
                            except ValidationError as e:
                                # Usar NestedObjectError para problemas com objetos aninhados
                                raise NestedObjectError(
                                    relation_field=field_name,
                                    index=index,
                                    errors=e.detail if hasattr(e, 'detail') else {"error": str(e)}
                                )
                            except Exception as e:
                                # Usar NestedObjectError para problemas com objetos aninhados
                                raise NestedObjectError(
                                    relation_field=field_name,
                                    index=index,
                                    message=str(e)
                                )
                except AttributeError:
                    raise InvalidRelationshipError(field_name, model.__name__)

            # Retorna a resposta com o objeto criado
            return response.Response(
                self.get_serializer(instance).data, 
                status=status.HTTP_201_CREATED
            )
        except (ValidationError, InvalidRelationshipError, NestedObjectError):
            raise  # Repassa exceções específicas
        except Exception as e:
            logger.error(f"Erro ao criar objeto: {str(e)}")
            raise OperationError(
                detail="Erro ao criar objeto", 
                operation="create",
                reason=str(e),
                source="DynamicModelViewSet"
            )
        
    def update(self, request, *args, **kwargs):
        """
        Atualiza totalmente um objeto com suporte a relacionamentos aninhados.

        Args:
            request: A requisição HTTP com o objeto atualizado.

        Returns:
            Response: A resposta HTTP com o objeto atualizado.

        Raises:
            OperationError: Se ocorrer um erro durante a atualização.
            InvalidRelationshipError: Se um relacionamento especificado for inválido.
            NestedObjectError: Se ocorrer um erro ao processar objetos aninhados.
        """
        try:
            # Obtém o objeto principal a ser atualizado com base no ID da URL
            instance = self.get_object()
            data = request.data

            # Identifica campos relacionados no JSON (ex.: *_set)
            related_sets = {key: value for key, value in data.items() if isinstance(value, list)}
            main_data = {key: value for key, value in data.items() if not isinstance(value, list)}

            # Atualiza os dados do modelo principal
            serializer = self.get_serializer(instance, data=main_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Processa os relacionamentos
            self._process_related_items(instance, related_sets)

            # Retorna o modelo principal com os dados atualizados
            response_serializer = self.get_serializer(instance)
            return response.Response(response_serializer.data, status=status.HTTP_200_OK)
        except (ValidationError, InvalidRelationshipError, NestedObjectError, RelatedObjectNotFoundError):
            raise
        except Exception as e:
            logger.error(f"Erro ao atualizar objeto: {str(e)}")
            raise OperationError(
                detail="Erro ao atualizar objeto",
                operation="update",
                reason=str(e),
                source="DynamicModelViewSet"
            )
    
    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente um objeto com suporte a relacionamentos aninhados.
        
        Args:
            request: A requisição HTTP com os dados a serem atualizados.
            
        Returns:
            Response: A resposta HTTP com o objeto atualizado.
            
        Raises:
            OperationError: Se ocorrer um erro durante a atualização.
            InvalidRelationshipError: Se um relacionamento especificado for inválido.
            NestedObjectError: Se ocorrer um erro ao processar objetos aninhados.
        """
        try:
            # Obtém o objeto principal a ser atualizado com base no ID da URL
            instance = self.get_object()
            data = request.data

            # Identifica campos relacionados no JSON (ex.: *_set)
            related_sets = {key: value for key, value in data.items() if isinstance(value, list)}
            main_data = {key: value for key, value in data.items() if not isinstance(value, list)}

            # Atualiza os dados do modelo principal
            serializer = self.get_serializer(instance, data=main_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Processa os relacionamentos
            self._process_related_items(instance, related_sets)

            # Retorna o modelo principal com os dados atualizados
            response_serializer = self.get_serializer(instance)
            return response.Response(response_serializer.data, status=status.HTTP_200_OK)
        except (ValidationError, InvalidRelationshipError, NestedObjectError, RelatedObjectNotFoundError):
            raise  # Repassa exceções específicas
        except Exception as e:
            logger.error(f"Erro ao atualizar objeto: {str(e)}")
            raise OperationError(
                detail="Erro ao atualizar objeto",
                operation="update",
                reason=str(e),
                source="DynamicModelViewSet" 
            )
    
    def _process_related_items(self, parent_instance, related_items):
        """
        Processa itens relacionados durante atualização.
        
        Args:
            parent_instance: A instância do objeto pai.
            related_items: Dicionário com os itens relacionados.
            
        Raises:
            InvalidRelationshipError: Se um relacionamento especificado for inválido.
            RelatedObjectNotFoundError: Se um objeto relacionado não for encontrado.
            NestedObjectError: Se ocorrer um erro ao processar objetos aninhados.
        """
        app_label = self.kwargs.get("app")
        
        for related_field, related_items_data in related_items.items():
            try:
                # Verifica se o campo relacionado existe
                related_manager = getattr(parent_instance, related_field, None)
                if related_manager is None or not hasattr(related_manager, 'model'):
                    raise InvalidRelationshipError(related_field, parent_instance._meta.model_name)
                
                related_model = related_manager.model
                related_model_name = related_model._meta.model_name
                
                # Determina o nome da chave estrangeira
                fk_name = None
                for field in related_model._meta.fields:
                    if field.is_relation and field.related_model == parent_instance._meta.model:
                        fk_name = field.name
                        break
                
                if not fk_name:
                    raise NestedObjectError(
                        relation_field=related_field,
                        message=f"Não foi possível determinar a chave estrangeira para {related_field}."
                    )

                # Processa os dados do relacionamento
                for index, item_data in enumerate(related_items_data):
                    item_id = item_data.get("id")
                    if item_id:
                        # Atualiza o registro existente
                        try:
                            related_instance = related_model.objects.get(pk=item_id)
                            # Verifica se o objeto pertence ao pai
                            if getattr(related_instance, fk_name).pk != parent_instance.pk:
                                raise NestedObjectError(
                                    relation_field=related_field,
                                    index=index,
                                    message=f"O objeto com ID {item_id} não pertence a este {parent_instance._meta.model_name}."
                                )
                                
                            related_serializer = DynamicSerializer(
                                related_instance, 
                                data=item_data, 
                                model_name=related_model_name, 
                                app_label=app_label, 
                                partial=True
                            )
                            related_serializer.is_valid(raise_exception=True)
                            related_serializer.save()
                        except ObjectDoesNotExist:
                            raise RelatedObjectNotFoundError(
                                model_name=related_model_name,
                                object_id=item_id,
                                field_name=related_field
                            )
                    else:
                        # Cria um novo registro relacionado
                        item_data[fk_name] = parent_instance.id
                        related_serializer = DynamicSerializer(
                            data=item_data, 
                            model_name=related_model_name, 
                            app_label=app_label
                        )
                        
                        try:
                            related_serializer.is_valid(raise_exception=True)
                            related_serializer.save()
                        except ValidationError as e:
                            raise NestedObjectError(
                                relation_field=related_field,
                                index=index,
                                errors=e.detail if hasattr(e, 'detail') else {"error": str(e)}
                            )
            except (InvalidRelationshipError, RelatedObjectNotFoundError, NestedObjectError):
                raise  # Repassa exceções específicas
            except Exception as e:
                logger.error(f"Erro ao processar itens relacionados {related_field}: {str(e)}")
                raise NestedObjectError(
                    relation_field=related_field,
                    message=f"Erro inesperado: {str(e)}"
                )

    def destroy(self, request, *args, **kwargs):
        """
        Exclui um objeto com suporte a exclusão em cascata controlada.
        
        Args:
            request: A requisição HTTP.
            
        Returns:
            Response: A resposta HTTP vazia (204 No Content).
            
        Raises:
            OperationError: Se ocorrer um erro durante a exclusão.
            InvalidRelationshipError: Se um relacionamento especificado for inválido.
            RelatedObjectNotFoundError: Se um objeto relacionado não for encontrado.
        """
        try:
            instance = self.get_object()
            data = request.data

            # Verifica se há instruções para exclusão em cascata
            if data:
                self._process_cascade_deletion(instance, data)

            # Exclui o objeto principal
            self.perform_destroy(instance)

            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except (InvalidRelationshipError, RelatedObjectNotFoundError):
            raise  # Repassa exceções específicas
        except Exception as e:
            logger.error(f"Erro ao excluir objeto: {str(e)}")
            raise OperationError(
                detail="Erro ao excluir objeto",
                operation="delete",
                reason=str(e),
                source="DynamicModelViewSet"
            )
    
    def _process_cascade_deletion(self, parent_instance, related_data):
        """
        Processa exclusão em cascata de objetos relacionados.
        
        Args:
            parent_instance: A instância do objeto pai.
            related_data: Dicionário com os dados dos objetos relacionados a serem excluídos.
            
        Raises:
            InvalidRelationshipError: Se um relacionamento especificado for inválido.
            RelatedObjectNotFoundError: Se um objeto relacionado não for encontrado.
        """
        for related_field, nested_data in related_data.items():
            # Verifica se o campo relacionado existe
            related_manager = getattr(parent_instance, related_field, None)
            if related_manager is None or not hasattr(related_manager, 'all'):
                raise InvalidRelationshipError(related_field, parent_instance._meta.model_name)

            # Processa registros aninhados
            if nested_data:
                for nested_item in nested_data:
                    try:
                        # Filtra os objetos relacionados com base nos critérios fornecidos
                        related_instance = related_manager.get(**nested_item)
                        # Exclui o objeto relacionado
                        related_instance.delete()
                    except ObjectDoesNotExist:
                        model_name = related_manager.model._meta.model_name
                        # Usar representação de string para o item aninhado
                        item_repr = ", ".join(f"{k}={v}" for k, v in nested_item.items())
                        raise RelatedObjectNotFoundError(
                            model_name=model_name,
                            object_id=item_repr,
                            field_name=related_field
                        )
            else:
                # Exclui todos os registros relacionados
                related_manager.all().delete()