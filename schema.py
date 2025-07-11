from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserSchemaOut(BaseModel):
    id: int
    username: str
    email: str
    quantidade_posts: int


class ComentarioSchema(BaseModel):
    texto:str
    data_criacao:datetime
    id_post:int
    id_usuario:int | str | None


class PostCreateSchema(BaseModel):
    title: str
    content: str
    user_id: int


class PostSchemaOut(BaseModel):
    id: int
    titulo:str
    conteudo:str
    id_usuario:int
    date_create: datetime
    quantidade_comentarios:int
    comentarios:List[ComentarioSchema]

class PostOutUnique(BaseModel):
    id: int
    titulo:str
    conteudo:str
    id_usuario:int
    date_create: datetime
    comentarios:List[ComentarioSchema]