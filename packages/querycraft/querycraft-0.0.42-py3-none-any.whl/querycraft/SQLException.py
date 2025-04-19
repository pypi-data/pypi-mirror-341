
from querycraft.LLM import *

class SQLException(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

    def __unicode__(self):
        return self.message

class SQLQueryException(SQLException):
    model = "gemma3:1b"

    @classmethod
    def set_model(cls, model):
        cls.model = model

    @classmethod
    def get_model(cls):
        return cls.model

    def __init__(self, message, sqlhs, sqlok, sgbd, bd = ""):
        super().__init__(message)
        self.sqlhs = sqlhs
        self.sqlok = sqlok
        self.sgbd = sgbd
        self.hints = LLM(SQLQueryException.get_model()).run(str(self.message), self.sqlok, self.sqlhs, self.sgbd, bd)

    def __str__(self):
        if self.hints == "":
            return (f"Erreur sur la requête SQL avec {self.sgbd} :\n -> Requête proposée : {self.sqlhs}\n -> Message {self.sgbd} :\n{self.message}")
        else:
            return (f"Erreur sur la requête SQL avec {self.sgbd} :\n -> Requête proposée : {self.sqlhs}\n -> Message {self.sgbd} :\n{self.message}\n -> Aide : {self.hints}")

    def __repr__(self):
        return self.__str__()
    def __unicode__(self):
        return self.__str__()