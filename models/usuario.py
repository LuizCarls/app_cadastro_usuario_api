from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  models import Base


class Usuario(Base):
   
   # Define o nome da tabela de usuários
    __tablename__ = 'usuario'

    # Define a chave primária da tabela de usuários
    id = Column("id_usuario", Integer, primary_key=True)

    # Supondo que os atributos seguintes já estejam em conformidade
    # com o menemônico adotado pela empresa, então não há necessidade
    # de fazer a definição de um "nome" de coluna diferente.

    nome = Column(String(140))  # 140 é o número máximo de caracteres
    cpf = Column(String(14)) # 14 é o número máximo de caracteres
    email = Column(String(140)) # 140 é o número máximo de caracteres
    cep = Column(String(9)) # 9 é o número máximo de caracteres
    rua = Column(String(100)) # 100 é o número máximo de caracteres
    numero = Column(Integer) 
    complemento = Column(String(50)) # 50 é o número máximo de caracteres
    cidade = Column(String(80)) # 80 é o número máximo de caracteres
    estado = Column(String(2)) # 2 é o número máximo de caracteres

    # A data de inserção será o instante de inserção do cadastro do usuário
    data_insercao = Column(DateTime, default=datetime.now())

    # Criando um requisito de unicidade envolvendo uma par de informações
    __table_args__ = (UniqueConstraint("cpf", name="usu_unique_id"),)

    def __init__(self, nome:str, cpf:str, email:str, cep:str, rua:str,
                 numero:int, complemento:str, cidade:str, estado:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Usuário        

        Arguments:
            nome: nome do usuário.
            cpf: cpf do usuário.
            email: email do usuário.
            cep: cpf da residência do usuário.
            rua: rua da residência do usuário.
            numero: número da residência do usuário.
            complemento: complemento da residência do usuário.
            cidade: cidade onde o usuário reside.
            estado: estado onde o usuário reside.
            data_insercao: data do cadastro do usuário.
        """

        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.cidade = cidade        
        self.estado = estado
        self.data_insercao = data_insercao

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Usuário.
        """
        return{
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "cep": self.cep,
            "rua": self.rua,
            "numero": self.numero,
            "complemento": self.complemento,
            "cidade": self.cidade,
            "estado": self.estado, 
            "data_insercao": self.data_insercao
        }

    def __repr__(self):
        """
        Retorna uma representação do Usuário em forma de texto.
        """        
        return f"Usuario(id={self.id}, nome='{self.nome}', cpf='{self.cpf}', email='{self.email}', cep='{self.cep}', rua='{self.rua}', numero='{self.numero}', complemento='{self.complemento}', cidade='{self.cidade}', estado='{self.estado}', data_insercao='{self.data_insercao}')"    
        
