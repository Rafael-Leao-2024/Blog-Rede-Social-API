from fastapi import APIRouter, Depends, status
from models import Comentario, pegar_sessao
from sqlalchemy.orm import Session
from schema import ComentarioSchema

rotas_comentario = APIRouter(prefix='/comentarios', tags=['Comentarios'])


@rotas_comentario.get('/')
async def comentarios(session:Session=Depends(pegar_sessao)):
    comentarios = session.query(Comentario).all()
    lista_comentarios = [dict(text=c.texto, data=c.data_criacao, id_post=c.id_post, user=c.user) for c in comentarios]
    return lista_comentarios


@rotas_comentario.post('/criar-comentario', status_code=status.HTTP_201_CREATED)
async def comentar_post(comentario_schema:ComentarioSchema, session: Session=Depends(pegar_sessao)):
    comentario = Comentario(texto=comentario_schema.texto, data_criacao=comentario_schema.data_criacao, id_post=comentario_schema.id_post, id_usuario=comentario_schema.id_usuario)
    session.add(comentario)
    session.commit()
    return comentario_schema.model_dump()