from fastapi import APIRouter, Depends, status, HTTPException
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from typing import List
from .models import pegar_sessao, User
from .schema import UserSchemaOut, UserSchema


rotas_usuarios = APIRouter(prefix='/usuarios', tags=['Usuarios'])


@rotas_usuarios.get('/', response_model=List[UserSchemaOut], status_code=status.HTTP_200_OK)
async def usuarios(session: Session = Depends(pegar_sessao)):
    usuarios = session.query(User).all()
    return usuarios


@rotas_usuarios.get('/{id_usuario}', response_model=UserSchemaOut, status_code=status.HTTP_200_OK)
async def pegar_usuario(id_usuario: int, session:Session = Depends(pegar_sessao)):
    usuario = session.query(User).filter(User.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario nao encontrado!")
    return usuario


@rotas_usuarios.post('/criar-usuario', status_code=status.HTTP_201_CREATED, response_model=UserSchemaOut)
async def criar_usuario(usuario_schema:UserSchema, session:Session=Depends(pegar_sessao)):
    usuario_schema.password = generate_password_hash(usuario_schema.password)
    usuario = User(**usuario_schema.model_dump())
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario