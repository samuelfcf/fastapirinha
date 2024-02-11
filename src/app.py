from fastapi import Depends, FastAPI, Response, status
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
        return None

    try:
        transaction_data = {
            'client_id': client.id,
            'valor': value,
            'tipo': 'c',
            'descricao': description,
        }
        transaction_respository.create(db, transaction_data)
    except Exception as e:
        print(f'Cannot process credit: {e}')
        client.saldo -= value
        db.commit()
        raise e

    return client


def process_debit(db: Session, body: TransactionSchemaInput, client: Client):
    description = body.descricao
    value = body.valor

    try:
        client.saldo -= value
        if client.saldo < -client.limite:
            client.saldo += value
            db.commit()
            return None

        db.commit()
    except Exception as e:
        print(f'Cannot process debit: {e}')
        client.saldo += value
        db.commit()
        return None

    try:
        transaction_data = {
            'client_id': client.id,
            'valor': value,
            'tipo': 'd',
            'descricao': description,
        }
        transaction_respository.create(db, transaction_data)
    except Exception as e:
        print(f'Cannot create transaction: {e}')
        client.saldo += value
        db.commit()
        raise e

    return client


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
            updated_client = process_debit(db, body, client)

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
        response.status_code = status.HTTP_404_NOT_FOUND
        return response

    updated_client = process_transaction(db, body, client)
    if not updated_client:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return response

    response.status_code = status.HTTP_200_OK
    return updated_client


@app.get('/clientes/{id}/extrato')
def statement():
    return {'message': 'toma aqui teu extrato!!'}
