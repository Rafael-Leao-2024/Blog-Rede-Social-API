from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import List
from sqlalchemy.orm import Session
from .models import Post, pegar_sessao, User
from .schema import PostSchemaOut, PostCreateSchema
from .autenticacao import pegar_usuario_atual_ativo


rotas_posts = APIRouter(prefix='/posts', tags=['Postagem'], dependencies=[Depends(pegar_usuario_atual_ativo)])


@rotas_posts.get('/', response_model=List[PostSchemaOut])
async def posts(session:Session=Depends(pegar_sessao)):
    todas_postagens = session.query(Post).all()
    return todas_postagens


@rotas_posts.get('/posts_paginacao', response_model=List[PostSchemaOut])
async def posts_paginacao(
    session: Session = Depends(pegar_sessao),
    pagina: int = Query(default=1, ge=1, description="Número da página"),
    limite: int = Query(default=10, le=10, ge=1, description="Itens por página (máx. 10)")
):
    offset = (pagina - 1) * limite    
    todas_postagens = session.query(Post).offset(offset).limit(limite).all()    
    return todas_postagens


@rotas_posts.get('/{id_post}', response_model=PostSchemaOut)
async def pegar_post(id_post:int, session:Session=Depends(pegar_sessao)):
    postagem = session.query(Post).filter(Post.id == id_post).first()
    if postagem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Postagem nao encontrado!")
    return postagem


@rotas_posts.post('/criar-post', status_code=status.HTTP_201_CREATED, response_model=PostSchemaOut)
async def criar_post(
    post_create_schema:PostCreateSchema, 
    session:Session=Depends(pegar_sessao), 
    usuario:User=Depends(pegar_usuario_atual_ativo)
    ):
    postagem = Post(title=post_create_schema.title, content=post_create_schema.content, user_id=usuario.id)
    session.add(postagem)
    session.commit()
    session.refresh(postagem)
    return postagem


@rotas_posts.delete('/delete/{id_post}')
async def deletar_post(id_post:int, session:Session=Depends(pegar_sessao)):
    post = session.query(Post).filter(Post.id == id_post).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post nao encontrado")
    session.delete(post)
    session.commit()
    return {"Mensagem": f"Post de ID {id_post} deletado com sucesso"}