from pydantic import BaseModel, constr, PositiveInt, validator
from typing_extensions import Literal

class TransactionSchema(BaseModel):
    valor: PositiveInt
    tipo: Literal['c', 'd'] # type: ignore
    descricao: constr(strip_whitespace=True, min_length=1, max_length=10) # type: ignore
        