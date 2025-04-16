# API Dinâmica Django

![API Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Django](https://img.shields.io/badge/Django-3.x-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.x-red.svg)

Uma API RESTful dinâmica baseada em Django Rest Framework que permite operações CRUD em qualquer modelo Django sem a necessidade de criar viewsets específicos para cada modelo.

> ⚠️ **Beta**: Este pacote está em fase beta. Use em ambiente de produção por sua conta e risco.

## Instalação

```bash
pip install drf-builder
```

## Sumário

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Endpoints](#endpoints)
- [Autenticação](#autenticação)
- [Operações HTTP](#operações-http)
  - [GET (Listar)](#get-listar)
  - [GET (Recuperar)](#get-recuperar)
  - [POST (Criar)](#post-criar)
  - [PATCH (Atualizar)](#patch-atualizar)
  - [PUT (Atualizar Completo)](#put-atualizar-completo)
  - [DELETE (Excluir)](#delete-excluir)
- [Recursos Avançados](#recursos-avançados)
  - [Filtragem](#filtragem)
  - [Agrupamento](#agrupamento)
  - [Relacionamentos Aninhados](#relacionamentos-aninhados)
  - [Controle de Profundidade](#controle-de-profundidade)
  - [Seleção de Campos](#seleção-de-campos)
  - [Exclusão em Cascata](#exclusão-em-cascata)
- [Tratamento de Erros](#tratamento-de-erros)
  - [Tipos de Exceções](#tipos-de-exceções)
  - [Exemplos de Mensagens de Erro](#exemplos-de-mensagens-de-erro)
- [Exemplos de Uso](#exemplos-de-uso)
  - [Exemplo 1: CRUD Básico](#exemplo-1-crud-básico)
  - [Exemplo 2: Relacionamentos](#exemplo-2-relacionamentos)
  - [Exemplo 3: Filtragem e Agrupamento](#exemplo-3-filtragem-e-agrupamento)
  - [Exemplo 4: Seleção de Campos](#exemplo-4-seleção-de-campos)
  - [Exemplo 5: Exclusão com Cascata](#exemplo-5-exclusão-com-cascata)
- [Documentação da API](#documentação-da-api)

## Visão Geral

A API Dinâmica é uma solução para interação com modelos Django de forma genérica e flexível. Ela foi projetada para:

- Criar endpoints RESTful para qualquer modelo Django sem código adicional
- Suportar todas as operações CRUD básicas (Create, Read, Update, Delete)
- Permitir filtragem dinâmica de resultados
- Facilitar operações com relacionamentos aninhados
- Fornecer uma estrutura consistente para tratamento de erros
- Permitir seleção de campos específicos para retorno
- Oferecer controle de profundidade para serialização de relacionamentos
- Suportar operações em lote e exclusão em cascata

## Estrutura do Projeto

A API é composta pelos seguintes componentes principais:

- **DynamicModelViewSet**: ViewSet central que gerencia todas as operações CRUD
- **DynamicSerializer**: Serializer que se adapta dinamicamente a qualquer modelo
- **Middleware de Exceções**: Sistema para tratamento padronizado de erros
- **Utilitários**: Funções auxiliares para operações comuns

```python
api/
├── viewsets.py      # Contém DynamicModelViewSet
├── serializers.py   # Contém DynamicSerializer
├── exceptions.py    # Define exceções personalizadas
├── middleware.py    # Implementa tratamento padronizado de erros
├── utils.py         # Funções de utilidade
└── routers.py       # Configuração de rotas
```

## Endpoints

A API segue um padrão de URL consistente:

- **Lista/Criação**: `/api/v1/<app>/<model>/`
- **Recuperar/Atualizar/Excluir**: `/api/v1/<app>/<model>/<pk>/`

Onde:
- `<app>` é o nome do aplicativo Django
- `<model>` é o nome do modelo
- `<pk>` é o ID do registro

## Autenticação

A API usa autenticação JWT (JSON Web Token) através do pacote `rest_framework_simplejwt`. Os seguintes endpoints estão disponíveis para autenticação:

- **Obter Token**: `POST /api/v1/token/`
- **Atualizar Token**: `POST /api/v1/token/refresh/`
- **Verificar Token**: `POST /api/v1/token/verify/`

**Exemplo de obtenção de token:**
```
POST /api/v1/token/
```
```json
{
  "username": "usuario",
  "password": "senha"
}
```

**Resposta de exemplo:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Para autenticar solicitações subsequentes, inclua o token de acesso no cabeçalho HTTP:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Operações HTTP

### GET (Listar)

Retorna uma lista de todos os objetos de um modelo específico.

**Endpoint:**
```
GET /api/v1/<app>/<model>/
```

**Parâmetros de consulta:**
- `depth`: Nível de profundidade para serializar relacionamentos (0-10)
- `filter_<campo>`: Filtrar resultados por campo específico
- `group_by`: Agrupar resultados por um ou mais campos
- `fields`: Seleção de campos específicos para retornar, separados por vírgula

**Exemplo de requisição:**
```
GET /api/v1/blog/post/?filter_status=published&depth=1
```

**Resposta de exemplo:**
```json
[
  {
    "id": 1,
    "title": "Primeiro Post",
    "content": "Conteúdo do post...",
    "status": "published",
    "author": {
      "id": 1,
      "name": "João Silva"
    },
    "_meta": {
      "model": "post",
      "app": "blog"
    }
  },
  {
    "id": 2,
    "title": "Segundo Post",
    "content": "Mais conteúdo...",
    "status": "published",
    "author": {
      "id": 2,
      "name": "Maria Souza"
    },
    "_meta": {
      "model": "post",
      "app": "blog"
    }
  }
]
```

### GET (Recuperar)

Retorna um objeto específico pelo seu ID.

**Endpoint:**
```
GET /api/v1/<app>/<model>/<pk>/
```

**Parâmetros de consulta:**
- `depth`: Nível de profundidade para serializar relacionamentos (0-10)
- `fields`: Seleção de campos específicos para retornar, separados por vírgula

**Exemplo de requisição:**
```
GET /api/v1/blog/post/1/?depth=2
```

**Resposta de exemplo:**
```json
{
  "id": 1,
  "title": "Primeiro Post",
  "content": "Conteúdo do post...",
  "status": "published",
  "author": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@exemplo.com"
  },
  "comment_set": [
    {
      "id": 1,
      "text": "Ótimo post!",
      "created_at": "2023-01-15T14:30:00Z"
    },
    {
      "id": 2,
      "text": "Muito interessante.",
      "created_at": "2023-01-16T10:15:00Z"
    }
  ],
  "_meta": {
    "model": "post",
    "app": "blog"
  }
}
```

### POST (Criar)

Cria um novo objeto do modelo especificado.

**Endpoint:**
```
POST /api/v1/<app>/<model>/
```

**Exemplo de requisição:**
```
POST /api/v1/blog/post/
```

**Payload de exemplo:**
```json
{
  "title": "Novo Post",
  "content": "Este é um novo post",
  "status": "draft",
  "author": 1,
  "comment_set": [
    {
      "text": "Um comentário inicial",
      "author_name": "Leitor Assíduo"
    }
  ]
}
```

**Resposta de exemplo:**
```json
{
  "id": 3,
  "title": "Novo Post",
  "content": "Este é um novo post",
  "status": "draft",
  "author": 1,
  "created_at": "2023-07-10T08:45:12Z",
  "_meta": {
    "model": "post",
    "app": "blog"
  }
}
```

### PATCH (Atualizar)

Atualiza parcialmente um objeto existente.

**Endpoint:**
```
PATCH /api/v1/<app>/<model>/<pk>/
```

**Exemplo de requisição:**
```
PATCH /api/v1/blog/post/3/
```

**Payload de exemplo:**
```json
{
  "status": "published",
  "comment_set": [
    {
      "id": 5,
      "text": "Comentário atualizado"
    },
    {
      "text": "Novo comentário"
    }
  ]
}
```

**Resposta de exemplo:**
```json
{
  "id": 3,
  "title": "Novo Post",
  "content": "Este é um novo post",
  "status": "published",
  "author": 1,
  "created_at": "2023-07-10T08:45:12Z",
  "_meta": {
    "model": "post",
    "app": "blog"
  }
}
```

### PUT (Atualizar Completo)

Atualiza completamente um objeto existente, substituindo todos os campos.

**Endpoint:**
```
PUT /api/v1/<app>/<model>/<pk>/
```

**Exemplo de requisição:**
```
PUT /api/v1/blog/post/3/
```

**Payload de exemplo:**
```json
{
  "title": "Título Completamente Novo",
  "content": "Conteúdo totalmente atualizado",
  "status": "published",
  "author": 1,
  "comment_set": [
    {
      "id": 5,
      "text": "Comentário atualizado"
    },
    {
      "text": "Novo comentário"
    }
  ]
}
```

**Resposta de exemplo:**
```json
{
  "id": 3,
  "title": "Título Completamente Novo",
  "content": "Conteúdo totalmente atualizado",
  "status": "published",
  "author": 1,
  "created_at": "2023-07-10T08:45:12Z",
  "updated_at": "2023-07-11T10:22:45Z",
  "_meta": {
    "model": "post",
    "app": "blog"
  }
}
```

**Observação**: Diferente do PATCH, o PUT requer que todos os campos obrigatórios sejam fornecidos, mesmo que não estejam sendo alterados.

### DELETE (Excluir)

Remove um objeto específico pelo seu ID.

**Endpoint:**
```
DELETE /api/v1/<app>/<model>/<pk>/
```

**Exemplo de requisição:**
```
DELETE /api/v1/blog/post/3/
```

**Payload opcional para exclusão em cascata:**
```json
{
  "comment_set": [
    {
      "id": 5
    },
    {
      "id": 6
    }
  ]
}
```

**Resposta:** Status HTTP 204 No Content

## Recursos Avançados

### Filtragem

A API suporta filtragem dinâmica usando o prefixo `filter_` seguido pelo nome do campo.

**Exemplos:**

Filtrar posts por autor:
```
GET /api/v1/blog/post/?filter_author=1
```

Filtrar posts por status:
```
GET /api/v1/blog/post/?filter_status=published
```

Combinando múltiplos filtros:
```
GET /api/v1/blog/post/?filter_status=published&filter_author=1
```

### Agrupamento

O parâmetro `group_by` permite agrupar resultados por um ou mais campos, retornando contagens.

**Exemplo:**
```
GET /api/v1/blog/post/?group_by=status
```

**Resposta de exemplo:**
```json
[
  {
    "status": "published",
    "count": 15
  },
  {
    "status": "draft",
    "count": 7
  }
]
```

Agrupamento por múltiplos campos:
```
GET /api/v1/blog/post/?group_by=status,author
```

**Resposta de exemplo:**
```json
[
  {
    "status": "published",
    "children": [
      {
        "author": 1,
        "count": 8
      },
      {
        "author": 2,
        "count": 7
      }
    ]
  },
  {
    "status": "draft",
    "children": [
      {
        "author": 1,
        "count": 3
      },
      {
        "author": 2,
        "count": 4
      }
    ]
  }
]
```

### Relacionamentos Aninhados

A API suporta a criação e atualização de objetos relacionados em uma única operação.

**Exemplo de criação com objetos aninhados:**
```json
{
  "title": "Post com comentários",
  "content": "Conteúdo...",
  "author": 1,
  "comment_set": [
    {
      "text": "Primeiro comentário",
      "author_name": "João"
    },
    {
      "text": "Segundo comentário",
      "author_name": "Maria"
    }
  ]
}
```

**Exemplo de atualização com objetos aninhados:**
```json
{
  "title": "Título atualizado",
  "comment_set": [
    {
      "id": 1,
      "text": "Comentário atualizado"
    },
    {
      "text": "Novo comentário"
    }
  ]
}
```

#### Validação de Objetos Aninhados

A API valida automaticamente os objetos aninhados, garantindo que:

1. Todos os campos obrigatórios estejam presentes
2. Os tipos de dados estejam corretos
3. Os objetos relacionados referenciados existam
4. As permissões sejam respeitadas

Se alguma validação falhar, a operação inteira é revertida (transação atômica) e um erro detalhado é retornado, indicando qual objeto aninhado apresentou o problema.

### Controle de Profundidade

O parâmetro `depth` controla quantos níveis de objetos relacionados são incluídos na resposta.

```
GET /api/v1/blog/post/1/?depth=0  # Apenas o objeto principal
GET /api/v1/blog/post/1/?depth=1  # Inclui objetos diretamente relacionados
GET /api/v1/blog/post/1/?depth=2  # Inclui também os objetos relacionados aos relacionados
```

**Exemplo com depth=0:**
```json
{
  "id": 1,
  "title": "Primeiro Post",
  "content": "Conteúdo...",
  "author": 1
}
```

**Exemplo com depth=1:**
```json
{
  "id": 1,
  "title": "Primeiro Post",
  "content": "Conteúdo...",
  "author": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@exemplo.com"
  }
}
```

**Limitações de Profundidade:**
- A profundidade máxima permitida é 10 (para evitar problemas de desempenho)
- Valores negativos resultarão em erro

### Seleção de Campos

O parâmetro `fields` permite selecionar apenas campos específicos para retornar na resposta.

```
GET /api/v1/blog/post/?fields=id,title,status  # Retorna apenas id, título e status
GET /api/v1/blog/post/1/?fields=title,content,author  # Retorna apenas título, conteúdo e autor
```

**Exemplo com seleção de campos:**
```json
{
  "id": 1,
  "title": "Primeiro Post",
  "status": "published",
  "_meta": {
    "model": "post",
    "app": "blog",
    "selected_fields": ["id", "title", "status"]
  }
}
```

A seleção de campos também funciona em combinação com outros parâmetros:

```
GET /api/v1/blog/post/?fields=title,author&depth=1  # Campos específicos com relacionamentos
GET /api/v1/blog/post/?fields=title,status&group_by=status  # Campos específicos com agrupamento
```

**Observações:**
- O campo `id` é sempre incluído, mesmo se não for explicitamente solicitado
- Se um campo solicitado não existir no modelo, ele será ignorado
- Para operações de agrupamento, os campos de agrupamento são automaticamente incluídos

### Exclusão em Cascata

A API suporta exclusão em cascata controlada de objetos relacionados.

**Exemplo de exclusão em cascata:**
```
DELETE /api/v1/blog/post/1/
```

**Payload para exclusão em cascata:**
```json
{
  "comment_set": [
    {
      "id": 1
    },
    {
      "id": 2
    }
  ],
  "tag_set": []  // Exclui todos os tags relacionados
}
```

**Observações:**
- Um array vazio (`[]`) indica que todos os objetos relacionados devem ser excluídos
- Um array com objetos contendo IDs especifica quais objetos relacionados devem ser excluídos
- Se nenhum payload for fornecido, apenas o objeto principal é excluído

## Tratamento de Erros

A API implementa um sistema abrangente de tratamento de erros, fornecendo respostas consistentes e informativas quando ocorrem problemas.

### Tipos de Exceções

| Exceção                     | Código HTTP | Descrição                                            |
|-----------------------------|-------------|------------------------------------------------------|
| ModelNotFoundError          | 404         | Modelo especificado não encontrado                   |
| RelatedObjectNotFoundError  | 404         | Objeto relacionado não encontrado                    |
| InvalidRelationshipError    | 400         | Relacionamento inválido especificado                 |
| NestedObjectError           | 400         | Erro ao processar objeto aninhado                    |
| InvalidFilterError          | 400         | Filtro inválido especificado                         |
| InvalidDepthError           | 400         | Valor de profundidade inválido                       |
| OperationError              | 400         | Erro genérico durante a operação                     |
| ValidationError             | 400         | Erro de validação nos dados fornecidos               |

### Exemplos de Mensagens de Erro

**Modelo não encontrado:**
```json
{
  "message": "Modelo 'article' não encontrado no app 'blog' nem no app 'core'.",
  "type": "ModelNotFoundError"
}
```

**Objeto relacionado não encontrado:**
```json
{
  "message": "Não foi possível encontrar Author com ID 99 para o campo 'author'.",
  "type": "RelatedObjectNotFoundError",
  "details": {
    "detail": "Não foi possível encontrar Author com ID 99 para o campo 'author'.",
    "context": {
      "model": "Author",
      "id": "99",
      "code": "related_object_not_found",
      "field": "author"
    }
  }
}
```

**Erro de validação:**
```json
{
  "message": "Erro de validação: title: Este campo é obrigatório.",
  "type": "ValidationError",
  "details": {
    "title": "Este campo é obrigatório."
  },
  "fields": {
    "title": "Este campo é obrigatório."
  }
}
```

**Erro em objeto aninhado:**
```json
{
  "comment_set": {
    "message": "Campos obrigatórios faltando em comment: text",
    "path": "comment_set[0]",
    "context": {
      "path": "comment_set[0]",
      "relation_field": "comment_set",
      "code": "nested_object_error",
      "index": 0,
      "missing_fields": ["text"]
    }
  }
}
```

**Filtro inválido:**
```json
{
  "filter": "Filtro inválido 'invalid_field': O campo não existe no modelo Post.",
  "type": "InvalidFilterError"
}
```

**Profundidade inválida:**
```json
{
  "depth": "Valor de profundidade inválido 'xyz'. Deve ser um número inteiro válido.",
  "type": "InvalidDepthError"
}
```

## Exemplos de Uso

### Exemplo 1: CRUD Básico

**Criar um autor:**
```
POST /api/v1/blog/author/
```
```json
{
  "name": "João Silva",
  "email": "joao@exemplo.com",
  "bio": "Escritor de tecnologia"
}
```

**Resposta:**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@exemplo.com",
  "bio": "Escritor de tecnologia",
  "created_at": "2023-07-01T14:30:00Z",
  "_meta": {
    "model": "author",
    "app": "blog"
  }
}
```

**Recuperar o autor:**
```
GET /api/v1/blog/author/1/
```

**Atualizar o autor:**
```
PATCH /api/v1/blog/author/1/
```
```json
{
  "bio": "Escritor de tecnologia e entusiasta de IA"
}
```

**Excluir o autor:**
```
DELETE /api/v1/blog/author/1/
```

### Exemplo 2: Relacionamentos

**Criar um post com comentários:**
```
POST /api/v1/blog/post/
```
```json
{
  "title": "API Dinâmica",
  "content": "Como criar uma API dinâmica com Django",
  "status": "published",
  "author": 2,
  "tag_set": [
    { "name": "django" },
    { "name": "api" },
    { "name": "python" }
  ],
  "comment_set": [
    {
      "text": "Excelente tutorial!",
      "author_name": "Leitor"
    }
  ]
}
```

**Atualizar um post e seus comentários:**
```
PATCH /api/v1/blog/post/1/
```
```json
{
  "status": "featured",
  "comment_set": [
    {
      "id": 1,
      "text": "Comentário atualizado"
    },
    {
      "text": "Novo comentário"
    }
  ]
}
```

### Exemplo 3: Filtragem e Agrupamento

**Filtrar posts publicados:**
```
GET /api/v1/blog/post/?filter_status=published
```

**Agrupar posts por status:**
```
GET /api/v1/blog/post/?group_by=status
```

**Filtrar e agrupar:**
```
GET /api/v1/blog/post/?filter_author=2&group_by=status
```

**Relacionamentos profundos:**
```
GET /api/v1/blog/post/1/?depth=2
```

**Resposta:**
```json
{
  "id": 1,
  "title": "API Dinâmica",
  "content": "Como criar uma API dinâmica com Django",
  "status": "featured",
  "author": {
    "id": 2,
    "name": "Maria Souza",
    "email": "maria@exemplo.com",
    "bio": "Desenvolvedora Python"
  },
  "tag_set": [
    {
      "id": 1,
      "name": "django",
      "post": 1
    },
    {
      "id": 2,
      "name": "api",
      "post": 1
    },
    {
      "id": 3,
      "name": "python",
      "post": 1
    }
  ],
  "comment_set": [
    {
      "id": 1,
      "text": "Comentário atualizado",
      "author_name": "Leitor",
      "post": 1
    },
    {
      "id": 2,
      "text": "Novo comentário",
      "post": 1
    }
  ],
  "_meta": {
    "model": "post",
    "app": "blog"
  }
}
```

### Exemplo 4: Seleção de Campos

**Selecionar campos específicos:**
```
GET /api/v1/blog/post/?fields=title,status,created_at
```

**Resposta:**
```json
[
  {
    "id": 1,
    "title": "API Dinâmica",
    "status": "featured",
    "created_at": "2023-07-01T14:30:00Z",
    "_meta": {
      "model": "post",
      "app": "blog",
      "selected_fields": ["id", "title", "status", "created_at"]
    }
  },
  {
    "id": 2,
    "title": "Segundo Post",
    "status": "published",
    "created_at": "2023-07-05T09:15:00Z",
    "_meta": {
      "model": "post",
      "app": "blog",
      "selected_fields": ["id", "title", "status", "created_at"]
    }
  }
]
```

**Combinar seleção de campos com profundidade:**
```
GET /api/v1/blog/post/1/?fields=title,author,comment_set&depth=1
```

**Resposta:**
```json
{
  "id": 1,
  "title": "API Dinâmica",
  "author": {
    "id": 2,
    "name": "Maria Souza",
    "email": "maria@exemplo.com"
  },
  "comment_set": [
    {
      "id": 1,
      "text": "Comentário atualizado",
      "author_name": "Leitor"
    },
    {
      "id": 2,
      "text": "Novo comentário"
    }
  ],
  "_meta": {
    "model": "post",
    "app": "blog",
    "selected_fields": ["id", "title", "author", "comment_set"]
  }
}
```

**Selecionar campos em uma operação de agrupamento:**
```
GET /api/v1/blog/post/?fields=status,author&group_by=status
```

**Resposta:**
```json
[
  {
    "status": "published",
    "count": 15
  },
  {
    "status": "draft",
    "count": 7
  }
]
```

Note que ao usar seleção de campos com agrupamento, os campos de agrupamento têm prioridade e sempre serão incluídos na resposta.

### Exemplo 5: Exclusão com Cascata

**Excluir um post e alguns comentários específicos:**
```
DELETE /api/v1/blog/post/1/
```

**Payload:**
```json
{
  "comment_set": [
    { "id": 1 },
    { "id": 3 }
  ]
}
```

**Excluir um post e todos os seus comentários:**
```
DELETE /api/v1/blog/post/2/
```

**Payload:**
```json
{
  "comment_set": []
}
```

## Documentação da API

A API inclui documentação interativa através do Swagger UI e ReDoc. Se a documentação estiver habilitada nas configurações (`API_DOCS_ENABLED = True`), os seguintes endpoints estarão disponíveis:

- **Swagger UI**: `/api/v1/swagger/`
- **ReDoc**: `/api/v1/redoc/`
- **Arquivo JSON da API**: `/api/v1/docs.json`
- **Arquivo YAML da API**: `/api/v1/docs.yaml`

A documentação interativa permite:
- Visualizar todos os endpoints disponíveis
- Testar chamadas diretamente da interface
- Ver modelos de dados e exemplos de requisição/resposta
- Verificar parâmetros e opções de cada endpoint

A documentação da API é atualizada automaticamente e reflete a estrutura atual da API, incluindo modelos dinâmicos e endpoints.
