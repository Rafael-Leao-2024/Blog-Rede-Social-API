from fastapi import FastAPI
from post import rotas_posts
from usuario import rotas_usuarios
from comentario import rotas_comentario

app = FastAPI()

app.include_router(rotas_usuarios)
app.include_router(rotas_posts)
app.include_router(rotas_comentario)


