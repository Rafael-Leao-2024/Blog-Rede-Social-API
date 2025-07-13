from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(description="Blog Rede Social API")
oauth2scheme = OAuth2PasswordBearer(tokenUrl='login/token')

from blog.autenticacao import rota_login
from blog.usuario import rotas_usuarios
from blog.post import rotas_posts
from blog.comentario import rotas_comentario

app.include_router(router=rota_login)
app.include_router(router=rotas_usuarios)
app.include_router(router=rotas_posts)
app.include_router(router=rotas_comentario)


