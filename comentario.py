from fastapi import APIRouter, Depends
from models import Comentario, pegar_sessao
from sqlalchemy.orm import Session

rotas_comentario = APIRouter(prefix='/comentarios', tags=['Comentarios'])

@rotas_comentario.get('/')
async def comentarios(session:Session=Depends(pegar_sessao)):
    comentarios = session.query(Comentario).all()
    lista_comentarios = [c.id for c in comentarios]
    return lista_comentarios