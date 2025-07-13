# Blog API - Rede Social

Uma API completa para um sistema de blog/rede social, construída com FastAPI.

## 📌 Visão Geral

Esta API fornece funcionalidades para:

- Autenticação de usuários
- Gerenciamento de perfis de usuários
- Criação e gerenciamento de posts
- Sistema de comentários em posts

## 🚀 Tecnologias Utilizadas

- Python 3.9+
- FastAPI
- SQLAlchemy (ORM)
- Pydantic (validação de dados)
- Outras dependências (listadas em `requirements.txt`)

## 🛠️ Rotas da API

### Autenticação

- `POST /login` - Login de usuário (obter token JWT)

### Usuários

- `POST /usuarios` - Criar novo usuário
- `GET /usuarios/{id_usuario}` - Obter informações de um usuário
- `DELETE /usuarios/deletar-usuario/{id_usuario}` - Remover usuário

### Posts

- `POST /posts/criar-post` - Criar novo post
- `GET /posts/{id_post}` - Obter um post específico
- `GET /posts` - Listar todos os posts
- `DELETE /posts/delete/{id_post}` - Remover post

### Comentários

- `POST /comentarios/criar-comentario` - Adicionar comentário a um post
- `GET /comentarios` - Obter todos proprios comentário
- `GET /posts/{post_id}/comentarios` - Listar comentários de um post
- `DELETE /comentarios/delete-comentario` -`{id_comentario}`no body da requisiçao Remover comentário

## ⚡ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/Rafael-Leao-2024/Blog-Rede-Social-API
   cd Blog-Rede-Social-API
   ```
2. Crie e ative um ambiente virtual:

   ```python -m venv venv
   source venv/bin/activate # Linux/Mac
   venv\Scripts\activate # Windows
   ```

3.Instale as dependências:

```
 pip install -r requirements.txt
```

4. Execute a aplicaçao:

```
uvicorn blog.main:app --reload
```

5. Acesse a documentação interativa:

   - Swagger UI: http://localhost:8000/docs
   - Redoc: http://localhost:8000/redoc

📄 Documentação da API

A documentação interativa está disponível automaticamente via:

- Swagger UI: /docs

- ReDoc: /redoc
