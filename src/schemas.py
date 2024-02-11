from pydantic import BaseModel, PositiveInt, constr
from typing_extensions import Literal


class TransactionSchemaInput(BaseModel):
    valor: PositiveInt
    tipo: Literal['c', 'd']   # type: ignore
    descricao: constr(
        strip_whitespace=True, min_length=1, max_length=10
    )   # type: ignore


class TransactionSchemaResponse(BaseModel):
    limite: int
    saldo: int


class StatementResponse(BaseModel):
    saldo: dict
    ultimas_transacoes: list
