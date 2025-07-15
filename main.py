from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI( title="Blog Rede Social API",
    description="API para um sistema de blog/rede social com autenticação, posts e comentários",
    version="1.0.0",
    contact={
        "name": "Rafael Leao",
        "email": "rafaelampaz6@gmail.com",
    },
    license_info={
        "name": "MIT",
    })

# Prefixos para versionamento e organização
api_prefix = "/api/v1"

oauth2scheme = OAuth2PasswordBearer(tokenUrl='login/token')

from blog.autenticacao import rota_login
from blog.usuario import rotas_usuarios
from blog.postagem import rotas_posts
from blog.comentario import rotas_comentario

app.include_router(router=rota_login)

app.include_router(router=rotas_usuarios)
app.include_router(router=rotas_posts)
app.include_router(router=rotas_comentario)


