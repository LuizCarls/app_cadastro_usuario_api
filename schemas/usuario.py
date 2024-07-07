from pydantic import BaseModel
from typing import List
from models.usuario import Usuario


class UsuarioSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    nome: str = "Fulano da Silva"
    cpf: str = "99988877766"
    email: str = "fulano@"
    cep: str = "55555444"
    rua: str = "Rua dos Milagres"
    numero: int = 123
    complemento: str = "A"
    cidade: str = "Fortaleza"
    estado: str = "CE"

class AtualizaUsuarioSchema(BaseModel):
    """ Define como um usuário atualizado deve ser representado
    """
    id: int = 1
    nome: str = "Fulano da Silva"
    cpf: str = "99988877766"
    email: str = "fulano@"
    cep: str = "55555444"
    rua: str = "Rua dos Milagres"
    numero: int = 123
    complemento: str = "A"
    cidade: str = "Fortaleza"
    estado: str = "CE"
    data_insercao: str = "dd/mm/aaaa"    

class UsuarioBuscaPorNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Usuário.
    """
    nome: str = "Fulano da Silva"

class UsuarioBuscaPorCpfSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Usuário.
    """
    cpf: str = "99988877766"


class UsuarioPorIDSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID do usuário.
    """
    id: int = "1"

class UsuarioViewSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    nome: str = "Fulano da Silva"
    cpf: str = "99988877766"
    email: str = "fulano@"
    cep: str = "55555444"
    rua: str = "Rua dos Milagres"
    numero: int = 123
    complemento: str = "A"
    cidade: str = "Fortaleza"
    estado: str = "CE"


class ListagemUsuariosSchema(BaseModel):
    """ Define como uma listagem de usuários será retornada.
    """
    usuarios:List[UsuarioViewSchema]

def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação do usuário seguindo o schema definido em
        ListagemUsuaiosSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "email": usuario.email,
            "cep": usuario.cep,
            "rua": usuario.rua,
            "numero": usuario.numero,
            "complemento": usuario.complemento,
            "cidade": usuario.cidade,
            "estado": usuario.estado,            
        })

    return {"usuarios": result}


class UsuarioViewSchema(BaseModel):
    """ Define como um usuário será retornado.
    """
    id: int = 1
    nome: str = "Fulano da Silva"
    cpf: str = "99988877766"
    email: str = "fulano@"
    cep: str = "55555444"
    rua: str = "Rua dos Milagres"
    numero: int = 123
    complemento: str = "A"
    cidade: str = "Fortaleza"
    estado: str = "CE"   
    data_insercao: str = "dd/mm/aaaa" 


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "cpf": usuario.cpf,
        "email": usuario.email,
        "cep": usuario.cep,
        "rua": usuario.rua,
        "numero": usuario.numero,
        "complemento": usuario.complemento,
        "cidade": usuario.cidade,
        "estado": usuario.estado,
    }
