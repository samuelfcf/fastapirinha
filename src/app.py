from fastapi import Depends, FastAPI, Response, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.db_session import get_db
from src.models import Client
from src.repository import ClientRepository, TransactionRepository
from src.schemas import TransactionSchemaInput, TransactionSchemaResponse

app = FastAPI()

client_respository = ClientRepository()
transaction_respository = TransactionRepository()


def process_credit(db: Session, body: TransactionSchemaInput, client: Client):
    description = body.descricao
    value = body.valor

    try:
        client.saldo += value
        db.commit()
    except Exception as e:
        print(f'Cannot update saldo: {e}')

    try:
        transaction_data = {
            'client_id': client.id,
            'valor': value,
            'tipo': 'c',
            'descricao': description,
        }
        transaction_respository.create(db, transaction_data)
    except Exception as e:
        print(f'Cannot create transaction: {e}')
        client.saldo -= value
        db.commit()

    return client


def process_debit(db: Session, body: TransactionSchemaInput, client: Client):
    return 1


def get_client_by_id(db: Session, id: str):
    return client_respository.get_by_id(db, id)


def process_transaction(
    db: Session, body: TransactionSchemaInput, client: Client
):
    kind = body.tipo

    match kind:
        case 'c':
            updated_client = process_credit(db, body, client)
        case 'd':
            process_debit(db, body, client)

    return updated_client


@app.post(
    '/clientes/{id}/transacoes',
    response_model=TransactionSchemaResponse,
)
def transactions(
    response: Response,
    id: int,
    body: TransactionSchemaInput,
    db: Session = Depends(get_db),
):
    client = get_client_by_id(db, id)
    if not client:
        response.status_code = 404
        return response

    updated_client = process_transaction(db, body, client)

    response.status_code = status.HTTP_200_OK
    return updated_client


@app.get('/clientes/{id}/extrato')
def statement():
    return {'message': 'toma aqui teu extrato!!'}
