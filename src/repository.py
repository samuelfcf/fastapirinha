from datetime import datetime

from sqlalchemy import desc
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

    def get_last_transactions(
        self, db: Session, client_id: int, limit: int = 10
    ) -> list[Transaction]:
        transactions = (
            db.query(Transaction)
            .filter(Transaction.client_id == client_id)
            .order_by(desc(Transaction.realizada_em))
            .limit(limit)
            .all()
        )
        if not transactions:
            return None

        return transactions
