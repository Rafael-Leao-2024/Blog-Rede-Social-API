from fastapi import FastAPI
from post import rotas_posts
from usuario import rotas_usuarios

app = FastAPI()

app.include_router(rotas_posts)
app.include_router(rotas_usuarios)

