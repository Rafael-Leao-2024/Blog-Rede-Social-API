from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from models import pegar_sessao, User
from schema import UserSchemaOut, UserSchema
from typing import List


rotas_usuarios = APIRouter(prefix='/usuarios', tags=['Usuarios'])


@rotas_usuarios.get('/', response_model=List[UserSchemaOut], status_code=status.HTTP_200_OK)
async def usuarios(session: Session = Depends(pegar_sessao)):
    usuarios = session.query(User).all()
    lista_usuarios = [dict(id=usuario.id, username=usuario.username, email=usuario.email, quantidade_posts=len(usuario.posts)) for usuario in usuarios]
    return lista_usuarios


@rotas_usuarios.get('/{id_usuario}', response_model=UserSchemaOut, status_code=status.HTTP_200_OK)
async def pegar_usuario(id_usuario: int, session:Session = Depends(pegar_sessao)):
    usuario = session.query(User).filter(User.id == id_usuario).first()
    usuario_output = dict(id=usuario.id, username=usuario.username, email=usuario.email, quantidade_posts=len(usuario.posts))
    return usuario_output


@rotas_usuarios.post('/criar-usuario', status_code=status.HTTP_201_CREATED, response_model=UserSchemaOut)
async def criar_usuario(usuario_schema:UserSchema, session:Session=Depends(pegar_sessao)):
    usuario = User(**usuario_schema.model_dump())
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario