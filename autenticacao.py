from main import oauth2scheme
from schema import UserSchema
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Optional
from models import pegar_sessao, User
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
from jose import jwt, JWTError 
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
EXPIRACAO_TOKEN_ACESSO = os.getenv("EXPIRACAO_TOKEN_ACESSO")


rota_login = APIRouter(prefix='login', tags=['Login'])

async def pegar_usuario(username:str, session:Session=Depends(pegar_sessao)):
    usuario = session.query(User).filter(User.username==username).first()
    return usuario

def autenticar_usuario(username:str, password:str):
    usuario = pegar_usuario(username=username)
    if not usuario:
        return False
    if not check_password_hash(usuario.password, password):
        return False
    return usuario

def criar_token_acesso(informacoes:dict, tempo_expiracao: Optional[timedelta]=None):
    copia = informacoes.copy()
    if tempo_expiracao:
        expiracao = datetime.utcnow() + tempo_expiracao
    else:
        expiracao = timedelta(minutes=int(EXPIRACAO_TOKEN_ACESSO))
    informacoes.update({'exp': expiracao})
    encode_jwt = jwt.encode(informacoes, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def pegar_usuario_atual():
    pass

def pegar_usuario_atual_ativo():
    pass


@rota_login.get('/token')
async def login(formulario: Annotated[OAuth2PasswordRequestForm, Depends()]):
    autenticar_usuario(usuario=formulario.username, senha=formulario.password)
    pass