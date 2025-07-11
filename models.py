from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///banco.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)

    posts = relationship("Post", back_populates="author")
    comentarios = relationship("Comentario", back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_create = Column(DateTime, default=datetime.now)

    comentarios = relationship("Comentario", back_populates="post")
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

    user = relationship("User", back_populates="comentarios")
    post = relationship("Post", back_populates="comentarios")

    def __init__(self, texto, data_criacao, id_post, id_usuario):
        self.texto = texto
        self.data_criacao = data_criacao
        self.id_post = id_post
        self.id_usuario
    
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

# usuario = User("rafael", "rafael100@gmail.com", "1234")
# post = Post('titulo', 'conteudo', 1, datetime.now())

# session.add(post)
# session.add(usuario)

# session.add(comentario)

# session.commit()

# todos = session.query(User).all()[0]

# print(todos.posts)