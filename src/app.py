from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.db_session import get_db
from src.schemas import (
    StatementResponse,
    TransactionSchemaInput,
    TransactionSchemaResponse,
)
from src.services import (
    get_client_by_id,
    get_client_statement,
    process_transaction,
)

app = FastAPI(root_path="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def docs():
    return RedirectResponse(url="docs/")

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


@app.get('/clientes/{id}/extrato', response_model=StatementResponse)
def statement(response: Response, id: int, db: Session = Depends(get_db)):
    client = get_client_by_id(db, id)
    if not client:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response

    statement = get_client_statement(db, client)

    response.status_code = status.HTTP_200_OK
    return statement
