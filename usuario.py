from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from models import pegar_sessao, User
from schema import UserOut
from typing import List


rotas_usuarios = APIRouter(prefix='/usuarios', tags=['Usuarios'])


@rotas_usuarios.get('/', response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def usuarios(session: Session = Depends(pegar_sessao)):
    usuarios = session.query(User).all()
    lista_usuarios = [dict(id=usuario.id, username=usuario.username, email=usuario.email, quantidade_posts=len(usuario.posts)) for usuario in usuarios]
    return lista_usuarios


@rotas_usuarios.get('/{id_usuario}', response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def pegar_usuario(id_usuario: int, session:Session = Depends(pegar_sessao)):
    usuario = session.query(User).filter(User.id == id_usuario).first()
    return usuario


