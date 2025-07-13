from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///banco.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    desabilitado = Column(Boolean)

    posts = relationship("Post", back_populates="author", cascade='all, delete')
    comentarios = relationship("Comentario", back_populates="user", cascade='all, delete')

    def __init__(self, username, email, password, desabilitado=False):
        self.username = username
        self.email = email
        self.password = password
        self.desabilitado = desabilitado

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_create = Column(DateTime, default=datetime.now)

    comentarios = relationship("Comentario", back_populates="post", cascade='all, delete')
    author = relationship("User", back_populates="posts")

    def __init__(self, title, content, user_id, date_create=datetime.utcnow()):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.date_create = date_create

    def _repr__(self):
        return f"Posts(title={self.title}, content={self.content})"  


class Comentario(Base):
    __tablename__ = 'comentarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    id_post = Column(Integer, ForeignKey('posts.id'))
    id_usuario = Column(Integer, ForeignKey('users.id'))

    user = relationship("User")
    post = relationship("Post", back_populates="comentarios")

    def __init__(self, texto, id_post, id_usuario, data_criacao=datetime.utcnow()):
        self.texto = texto
        self.data_criacao = data_criacao
        self.id_post = id_post
        self.id_usuario = id_usuario
    
    def __repr__(self):
        return f"Comentario('texto= {self.texto}')"


Base.metadata.create_all(engine)

def pegar_sessao():
    try:
        Session = sessionmaker(engine)
        session = Session()
        yield session
    finally:
        session.close()


def pegar_usuario(username):
    try:
        Session = sessionmaker(engine)
        session = Session()
        usuario = session.query(User).filter(User.username==username).first()
        return usuario
    finally:
        session.close()

