from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schema import ComentarioCreateSchema, ComentarioSchemaOutDadosUser, UpdateSchemaComentario, ComentarioUpdateSchemaOut
from .autenticacao import pegar_usuario_atual_ativo
from .models import Comentario, User, pegar_sessao

rotas_comentario = APIRouter(prefix='/comentarios', tags=['Comentarios'])


@rotas_comentario.get('/', response_model=List[ComentarioSchemaOutDadosUser])
async def comentarios(
    session:Session=Depends(pegar_sessao), 
    usuario:User=Depends(pegar_usuario_atual_ativo)
    ):
    comentarios = session.query(Comentario).filter(Comentario.id_usuario==usuario.id).all()
    return comentarios


@rotas_comentario.post('/criar-comentario', status_code=status.HTTP_201_CREATED)
async def comentar_post(
    comentario_schema:ComentarioCreateSchema, 
    session: Session=Depends(pegar_sessao), 
    usuario:User=Depends(pegar_usuario_atual_ativo)
    ):
    comentario = Comentario(texto=comentario_schema.texto, data_criacao=comentario_schema.data_criacao, id_post=comentario_schema.id_post, id_usuario=usuario.id)
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario

@rotas_comentario.put('/editar-comentario/{id_comentario}', response_model=ComentarioUpdateSchemaOut)
async def editar_comentario(
    id_comentario:int,
    update_comentario: UpdateSchemaComentario,
    session:Session=Depends(pegar_sessao),
    usuario:User=Depends(pegar_usuario_atual_ativo)   
):
    comentario = session.query(Comentario).filter(Comentario.id == id_comentario).first()
    if usuario.id != comentario.id_usuario or update_comentario.texto == "string":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Voce nao pode Editar este Comentario")
    
    texto_antigo = comentario.texto
    comentario.texto = update_comentario.texto

    session.commit()
    session.refresh(comentario)
    
    return {'comentario_antigo': texto_antigo, 'novo_comentario': comentario.texto}


@rotas_comentario.delete('/delete-comentario')
async def deletar_comentario(
    id_comentario: int,
    usuario: User=Depends(pegar_usuario_atual_ativo),
    session: Session=Depends(pegar_sessao)
    ):
    comentario = session.query(Comentario).filter(Comentario.id==id_comentario).first()
    
    if not comentario:
        raise HTTPException(status_code=404, detail="comentario nao encontrado")
    if comentario.id_usuario != usuario.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Voce nao tem permissao para deletar esse comentario")
    
    session.delete(comentario)
    session.commit()
    return {"mensgem": f"comentario de ID {comentario.id} deletado com sucesso"}


