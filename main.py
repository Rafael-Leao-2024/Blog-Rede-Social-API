from fastapi import FastAPI
from post import rotas_posts
from usuario import rotas_usuarios
from comentario import rotas_comentario
from fastapi.security import OAuth2PasswordBearer
from autenticacao import rota_login

app = FastAPI()

oauth2scheme = OAuth2PasswordBearer(tokenUrl='token')

app.include_router(rota_login)
app.include_router(rotas_usuarios)
app.include_router(rotas_posts)
app.include_router(rotas_comentario)


