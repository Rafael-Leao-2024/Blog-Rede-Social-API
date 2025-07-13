from pydantic import BaseModel
from typing import List, Optional
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


class ComentarioSchema(BaseModel):
    texto:str
    data_criacao:datetime
    id_post:int

class ComentarioSchemaOut(ComentarioSchema):
    id_usuario:int

class ComentarioSchemaOutDadosUser(ComentarioSchema):
    user: UserSchemaOut
   

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
    comentarios:List[ComentarioSchemaOut]

class PostOutUnique(BaseModel):
    id: int
    titulo:str
    conteudo:str
    id_usuario:int
    date_create: datetime
    comentarios:List[ComentarioSchema]