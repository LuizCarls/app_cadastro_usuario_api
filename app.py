from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models import Session, Usuario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API de Cadastro de Usuários", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Adição, visualização e remoção de usuários à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo Usuário à base de dados

    Retorna uma representação dos usuários.
    """
    
    print(form)

    usuario = Usuario(
        nome=form.nome,
        cpf=form.cpf,
        email=form.email,
        cep=form.cep,
        rua=form.rua,
        numero=form.numero,
        complemento=form.complemento,
        cidade=form.cidade,
        estado=form.estado,        
    )

    logger.info(f"Adicionando usuário de nome: '{usuario.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando usuario
        session.add(usuario)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.info("Adicionado usuário: %s"% usuario)
        return apresenta_usuario(usuario), 200

    except IntegrityError as e:
        # como a duplicidade do CPF é a provável razão do IntegrityError
        error_msg = "Usuário de mesmo CPF já salvo na base :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo usuário :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_usuarios():
    """Faz a busca por todos os Usuários cadastrados

    Retorna uma representação da listagem de usuários.
    """
    logger.info(f"Coletando usuários ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuarios = session.query(Usuario).all()

    if not usuarios:
        # se não há usuários cadastrados
        return {"usuarios ": []}, 200
    else:
        logger.info(f"% usuarios encontrados: " % len(usuarios))
        # retorna a representação de usuários
        return apresenta_usuarios(usuarios), 200


@app.get('/busca_usuario_por_id', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def busca_usuario_por_id(query: UsuarioBuscaPorIDSchema):
    """Faz a busca por um Usuário a partir do ID

    Retorna uma representação do usuário encontrado.
    """
    usuario_id = query.id
    logger.info(f"Coletando dados sobre usuário #{usuario_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        # se o usuário não foi encontrado
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao buscar usuário '{usuario_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.info("Usuário econtrado: %s" % usuario)
        # retorna a representação de usuário
        return apresenta_usuario(usuario), 200
    

@app.get('/busca_usuario_por_nome', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def busca_usuario_por_nome(query: UsuarioBuscaPorNomeSchema):
    """Faz a busca por usuários por nome

    Retorna uma representação dos usuários que possuem o nome associado.
    """
    nome = unquote(query.termo)
    logger.info(f"Fazendo a busca por nome: {nome}")
    # criando conexão com a base
    session = Session()
    # fazendo o filtro
    Usuarios = session.query(Usuario).filter(Usuario.nome.ilike(f"%{nome}%")).all()
    
    if not Usuarios:
        # se não há usuários cadastrados
        return {"usuários": []}, 200
    else:
        logger.info(f"%usuários encontrados" % len(Usuarios))
        # retorna a representação de usuário
        return apresenta_usuarios(Usuarios), 200
    

@app.get('/busca_usuario_por_cpf', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def busca_usuario_por_cpf(query: UsuarioBuscaPorCpfSchema):
    """Faz a busca por um Usuário a partir do cpf

    Retorna uma representação do usuário encontrado.
    """
    cpf = unquote(query.termo)
    logger.info(f"Fazendo a busca por nome: {cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.cpf == cpf).first()

    if not usuario:
        # se o usuário não foi encontrado
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao buscar usuário '{cpf}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.info("Usuário econtrado: %s" % usuario)
        # retorna a representação de usuário
        return apresenta_usuario(usuario), 200


@app.delete('/deletar_usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def del_usuario(query: UsuarioBuscaPorIDSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """    
    usuario_id = query.id
    
    # criando conexão com a base
    session = Session()

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if usuario:
        logger.debug(f"Deletando dados do usuário #{usuario.nome}")
            
        # Fazendo a remoção
        count = session.query(Usuario).filter(Usuario.id == usuario_id).delete()
        session.commit()

        if count:
            # Retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado usuário #{usuario.nome}")
            return {"mesage": "Usuário removido", "id": usuario_id, "nome": usuario.nome}
        else:
            error_msg = "Erro ao remover usuário :/"
            logger.warning(f"Erro ao deletar usuário #{usuario.nome}, {error_msg}")
            return {"mesage": error_msg}, 404
    else:
            # Se o usuário não foi encontrado
            error_msg = "Usuário não encontrado na base :/"
            logger.warning(f"Erro ao deletar usuário com ID {usuario_id}, {error_msg}")
            return {"mesage": error_msg}, 404
