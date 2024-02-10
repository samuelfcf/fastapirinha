from fastapi import FastAPI

app = FastAPI()


@app.post('/clientes/{id}/transacoes')
def transactions():
    return {'message': 'mandei uma transação!!'}


@app.get('/clientes/{id}/extrato')
def statement():
    return {'message': 'toma aqui teu extrato!!'}
