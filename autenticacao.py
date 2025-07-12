from schema import UserSchema, TokenDadosSchema, TokenSchema
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Optional
from models import pegar_sessao, User, pegar_usuario
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash
from jose import jwt, JWTError 
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
import os

load_dotenv()

ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
EXPIRACAO_TOKEN_ACESSO = os.getenv("EXPIRACAO_TOKEN_ACESSO")

oauth2scheme = OAuth2PasswordBearer(tokenUrl='login/token')

rota_login = APIRouter(prefix='/login', tags=['Login'])

# def pegar_usuario(username:str, session:Session=Depends(pegar_sessao)):
#     usuario = session.query(User).filter(User.username==username).first()
#     return usuario

def autenticar_usuario(username:str, password:str):
    usuario = pegar_usuario(username=username)
    print(usuario)
    if not usuario:
        return False
    if not check_password_hash(usuario.password, password):
        return False
    return usuario

def criar_token_acesso(informacoes:dict, tempo_expiracao: Optional[timedelta]=None):
    if tempo_expiracao:
        expiracao = datetime.utcnow() + tempo_expiracao
    else:
        expiracao = timedelta(minutes=int(EXPIRACAO_TOKEN_ACESSO))
    informacoes.update({'exp': expiracao})
    encode_jwt = jwt.encode(informacoes, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


async def pegar_usuario_atual(token: Annotated[str, Depends(oauth2scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_dado = TokenDadosSchema(username=username)
    except JWTError:
        raise credentials_exception
    
    usuario = pegar_usuario(username=token_dado.username)
    if not usuario:
        raise credentials_exception
    return usuario


async def pegar_usuario_atual_ativo(usuario_atual: User = Depends(pegar_usuario_atual)):
    if usuario_atual.desabilitado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario Desabilitado")
    return usuario_atual

@rota_login.post('/token', response_model=TokenSchema)
async def login(formulario: Annotated[OAuth2PasswordRequestForm, Depends()]):
    usuario = autenticar_usuario(formulario.username, formulario.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expiracao_token_acesso = timedelta(minutes=int(EXPIRACAO_TOKEN_ACESSO))
    token = criar_token_acesso(informacoes={'sub': usuario.username}, tempo_expiracao=expiracao_token_acesso)
    return {"token_type": "Bearer", "access_token": token}