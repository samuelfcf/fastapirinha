from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.models import Client, Transaction


class ClientRepository:
    def get_by_id(self, db: Session, id: int) -> Client:
        return db.query(Client).get(id)

    def create(self, db: Session, obj) -> Client:

        client = Client(
            created_at=datetime.now(),
            **obj,
        )

        db.add(client)
        db.commit()
        db.refresh(client)

        return client

class TransactionRepository:
    def create(self, db: Session, obj) -> Transaction:

        transaction = Transaction(
            realizada_em=datetime.now(),
            **obj,
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction