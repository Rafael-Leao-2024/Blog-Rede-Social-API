from fastapi import FastAPI
from blog.post import rotas_posts
from blog.usuario import rotas_usuarios
from blog.comentario import rotas_comentario

from blog.autenticacao import rota_login


app = FastAPI(description="Blog Rede Social API")


app.include_router(rota_login)
app.include_router(rotas_usuarios)
app.include_router(rotas_posts)
app.include_router(rotas_comentario)


