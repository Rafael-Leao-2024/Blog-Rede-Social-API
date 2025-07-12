from fastapi import APIRouter, Depends, status, HTTPException
from schema import PostSchemaOut, PostOutUnique, PostCreateSchema
from typing import List
from models import Post, pegar_sessao
from sqlalchemy.orm import Session


rotas_posts = APIRouter(prefix='/posts', tags=['Postagem'])


@rotas_posts.get('/', response_model=List[PostSchemaOut])
async def posts(session:Session=Depends(pegar_sessao)):
    posts = session.query(Post).all()
    lista_posts = [
        dict(id=post.id, 
            titulo=post.title, 
            conteudo=post.content, 
            id_usuario=post.user_id, 
            date_create=post.date_create, 
            quantidade_comentarios=len(post.comentarios),
            comentarios=[
                dict(
                    texto=comentario.texto,
                     data_criacao=comentario.data_criacao,
                     id_post=comentario.id_post,
                     id_usuario= comentario.id_usuario if comentario.id_usuario == None else comentario.user.id
                     )
                for comentario in post.comentarios]
            )
        for post in posts
        ]
    return lista_posts


@rotas_posts.get('/{id_post}', response_model=PostOutUnique)
async def pegar_post(id_post:int, session:Session=Depends(pegar_sessao)):
    p = session.query(Post).filter(Post.id == id_post).first()
    dicionario_post = dict(id=p.id, titulo=p.title, conteudo=p.content, id_usuario=p.user_id, date_create=p.date_create, comentarios= [dict(
                    texto=comentario.texto,
                     data_criacao=comentario.data_criacao,
                     id_post=comentario.id_post,
                     id_usuario= comentario.id_usuario if comentario.id_usuario == None else comentario.user.id
                     ) for comentario in p.comentarios])
    return dicionario_post


@rotas_posts.post('/criar-post', status_code=status.HTTP_201_CREATED, response_model=PostOutUnique)
async def criar_post(post_create_schema:PostCreateSchema, session:Session=Depends(pegar_sessao)):
    post_dict = post_create_schema.model_dump()
    p = Post(**post_dict)

    session.add(p)
    session.commit()
    session.refresh(p)

    post = dict(id=p.id, titulo=p.title, conteudo=p.content, id_usuario=p.user_id, date_create=p.date_create, comentarios= [dict(
                    texto=comentario.texto,
                     data_criacao=comentario.data_criacao,
                     id_post=comentario.id_post,
                     id_usuario= comentario.id_usuario if comentario.id_usuario == None else comentario.user.id
                     ) for comentario in p.comentarios])
    return post


@rotas_posts.delete('/{id_post}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_post(id_post:int, session:Session=Depends(pegar_sessao)):
    post = session.query(Post).filter(Post.id == id_post).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post nao encontrado")
    session.delete(post)
    session.commit()
    return {"Mensagem": f"Post de ID {id_post} deletado com sucesso"}