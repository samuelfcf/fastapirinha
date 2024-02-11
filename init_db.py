from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Client

engine = create_engine(
    'postgresql://app_user:app_password@api_rinha_db:5432/app_db'
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


def populate_data():
    try:
        client_data = [
            {'id': 1, 'limite': 100000, 'saldo': 0},
            {'id': 2, 'limite': 80000, 'saldo': 0},
            {'id': 3, 'limite': 1000000, 'saldo': 0},
            {'id': 4, 'limite': 10000000, 'saldo': 0},
            {'id': 5, 'limite': 500000, 'saldo': 0},
        ]
        for data in client_data:
            client = Client(**data)
            db.add(client)

        db.commit()
    except Exception as e:
        print(e)
    finally:
        db.close()


populate_data()
