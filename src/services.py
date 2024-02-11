from datetime import datetime

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


def get_last_transactions(db: Session, client: Client):
    return transaction_respository.get_last_transactions(db, client.id)


def get_statement_response_object():
    return {
        'saldo': {'total': None, 'data_extrato': None, 'limite': None},
        'ultimas_transacoes': [],
    }


def get_client_statement(db: Session, client: Client):
    last_transactions = get_last_transactions(db, client)

    statement_object = get_statement_response_object()
    statement_object['saldo']['total'] = client.saldo
    statement_object['saldo']['data_extrato'] = datetime.utcnow().strftime(
        '%Y-%m-%dT%H:%M:%S.%fZ'
    )
    statement_object['saldo']['limite'] = client.limite

    if not last_transactions:
        return statement_object

    for transaction in last_transactions:
        transaction_object = {
            'valor': transaction.valor,
            'tipo': transaction.tipo,
            'descricao': transaction.descricao,
            'realizada_em': transaction.realizada_em,
        }
        statement_object['ultimas_transacoes'].append(transaction_object)

    return statement_object
