from sqlalchemy.orm import Session

from src.models import Client
from src.repository import ClientRepository, TransactionRepository
from src.schemas import TransactionSchemaInput

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


def get_client_by_id(db: Session, id: str):
    return client_respository.get_by_id(db, id)
