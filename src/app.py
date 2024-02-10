from fastapi import FastAPI

from src.schemas import TransactionSchema

app = FastAPI()


@app.post('/clientes/{id}/transacoes')
def transactions(id: int, body: TransactionSchema):
    response = {'limite': 100000, 'saldo': -9098}
    return response


@app.get('/clientes/{id}/extrato')
def statement():
    return {'message': 'toma aqui teu extrato!!'}
