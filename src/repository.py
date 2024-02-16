from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.models import Client, Transaction


class ClientRepository:
    def get_by_id(self, db: Session, id: int) -> Client:
        try:
            return db.query(Client).with_for_update().get(id)
        except Exception as e:
            print(f'Error [get_by_id]: {e}')
        finally:
            db.close()

    def create(self, db: Session, obj) -> Client:
        try:
            client = Client(
                created_at=datetime.now(),
                **obj,
            )

            db.add(client)
            db.commit()
            db.refresh(client)
        except Exception as e:
            print(f'Error [create client]: {e}')
        finally:
            db.close()

        return client


class TransactionRepository:
    def create(self, db: Session, obj) -> Transaction:
        try:
            transaction = Transaction(
                realizada_em=datetime.now(),
                **obj,
            )

            db.add(transaction)
            db.commit()
            db.refresh(transaction)
        except Exception as e:
            print(f'Error [create transaction]: {e}')
        finally:
            db.close()

        return transaction

    def get_last_transactions(
        self, db: Session, client_id: int, limit: int = 10
    ) -> list[Transaction]:
        try:
            transactions = (
                db.query(Transaction)
                .filter(Transaction.client_id == client_id)
                .with_for_update()
                .order_by(desc(Transaction.realizada_em))
                .limit(limit)
                .all()
            )
            if not transactions:
                return None
        except Exception as e:
            print(f'Error [get_last_transaction]: {e}')
        finally:
            db.close()

        return transactions
