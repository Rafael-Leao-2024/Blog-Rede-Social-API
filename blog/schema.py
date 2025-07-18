from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TokenDadosSchema(BaseModel):
    username: Optional[str]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    desabilitado:bool | None = None


class UserSchemaOut(BaseModel):
    id: int
    username: str
    email: str
    desabilitado: bool


class ComentarioCreateSchema(BaseModel):
    texto:str
    data_criacao:datetime
    id_post:int
    

class UpdateSchemaComentario(BaseModel):
    texto: str


class ComentarioUpdateSchemaOut(BaseModel):
    comentario_antigo:str
    novo_comentario:str 


class ComentarioSchemaOutDadosUser(ComentarioCreateSchema):
    id_usuario:int
    user: UserSchemaOut
   

class PostCreateSchema(BaseModel):
    title: str
    content: str


class UpdatePostSchema(PostCreateSchema):
    pass


class PostSchemaOut(BaseModel):
    id: int
    title:str
    content:str
    author: UserSchemaOut
    date_create: datetime
    comentarios: List[ComentarioSchemaOutDadosUser]
