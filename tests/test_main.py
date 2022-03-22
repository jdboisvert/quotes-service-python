from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import status

from models import QuoteRecord
from database import Base
from main import app, app_name, get_db

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = Session(bind=engine, expire_on_commit=False)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def __set_up_quotes(number_of_quotes: int = 1) -> List[QuoteRecord]:
    quote_records = []
    session = Session(bind=engine, expire_on_commit=False)

    for i in range(number_of_quotes):
        quote_record = QuoteRecord(
            quote=f"This is test quote {i}.", author_name="Tester"
        )

        session.add(quote_record)
        session.commit()
        quote_records.append(quote_record)

    session.close()

    return quote_records


def test_create_quote(test_db):
    quote = "This is a test."
    author_name = "Tester"

    response = client.post(
        f"/api/{app_name}",
        json={"quote": quote, "author_name": author_name},
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()

    assert data["quote"] == quote
    assert data["author_name"] == author_name
    assert "id" in data
    assert type(data["id"]) is int


def test_get_quote(test_db):
    quote_record = __set_up_quotes(number_of_quotes=1)[0]

    response = client.get(f"/api/{app_name}/{quote_record.id}")

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["quote"] == quote_record.quote
    assert data["id"] == quote_record.id
    assert data["author_name"] == quote_record.author_name


def test_get_quote_404(test_db):
    response = client.get(f"/api/{app_name}/12345")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_quotes(test_db):
    quote_record = __set_up_quotes(number_of_quotes=1)[0]

    response = client.get(f"/api/{app_name}")

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    quote_item = data[0]
    assert quote_item["quote"] == quote_record.quote
    assert quote_item["id"] == quote_record.id
    assert quote_item["author_name"] == quote_record.author_name


def test_delete_quote(test_db):
    quote_record = __set_up_quotes(number_of_quotes=1)[0]

    response = client.delete(f"/api/{app_name}/{quote_record.id}")

    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["quote"] == quote_record.quote
    assert data["id"] == quote_record.id
    assert data["author_name"] == quote_record.author_name

    session = Session(bind=engine, expire_on_commit=False)

    deleted_quote_record = session.query(QuoteRecord).get(quote_record.id)
    session.close()

    assert not deleted_quote_record


def test_delete_quote_404(test_db):
    response = client.delete(f"/api/{app_name}/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_quote_quote_only(test_db):
    quote_record = __set_up_quotes(number_of_quotes=1)[0]

    updated_quote = "This is an update"

    response = client.put(
        f"/api/{app_name}/{quote_record.id}",
        json={"quote": updated_quote},
    )

    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["quote"] == updated_quote
    assert data["id"] == quote_record.id
    assert data["author_name"] == quote_record.author_name


def test_update_quote_author_name_only(test_db):
    quote_record = __set_up_quotes(number_of_quotes=1)[0]

    updated_author_name = "Tester 2"

    response = client.put(
        f"/api/{app_name}/{quote_record.id}",
        json={"author_name": updated_author_name},
    )

    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["quote"] == quote_record.quote
    assert data["id"] == quote_record.id
    assert data["author_name"] == updated_author_name


def test_update_quote(test_db):
    quote_record = __set_up_quotes(number_of_quotes=1)[0]

    updated_quote = "This is an update"
    updated_author_name = "Tester 2"

    response = client.put(
        f"/api/{app_name}/{quote_record.id}",
        json={"quote": updated_quote, "author_name": updated_author_name},
    )

    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["quote"] == updated_quote
    assert data["id"] == quote_record.id
    assert data["author_name"] == updated_author_name


def test_update_quote_404(test_db):
    response = client.put(
        f"/api/{app_name}/999999",
        json={"quote": "This is a test", "author_name": "Tester 3"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
