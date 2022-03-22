from typing import List

from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from database import Base, engine
from models import QuoteRecord, Quote
from sqlalchemy.orm import Session

from schemas import QuoteCreateRequest, QuoteUpdateRequest

Base.metadata.create_all(engine)

app_name = "quote"

app = FastAPI()


@app.post(f"/api/{app_name}", response_model=Quote, status_code=status.HTTP_201_CREATED)
def create_quote(quote: QuoteCreateRequest):
    session = Session(bind=engine, expire_on_commit=False)
    quote_record = QuoteRecord(quote=quote.quote, author_name=quote.author_name)

    session.add(quote_record)
    session.commit()
    session.close()

    json_compatible_item_data = jsonable_encoder(quote_record)
    return JSONResponse(content=json_compatible_item_data)


@app.get(f"/api/{app_name}/{{id}}", response_model=Quote)
def read_quote(id: int):
    session = Session(bind=engine, expire_on_commit=False)

    quote_record = session.query(QuoteRecord).get(id)
    session.close()

    if not quote_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    json_compatible_item_data = jsonable_encoder(quote_record)
    return JSONResponse(content=json_compatible_item_data)


@app.get(f"/api/{app_name}", response_model=List[Quote])
def read_quotes():
    session = Session(bind=engine, expire_on_commit=False)

    quote_records = session.query(QuoteRecord).all()
    session.close()

    json_compatible_item_data = jsonable_encoder(quote_records)
    return JSONResponse(content=json_compatible_item_data)


@app.put(f"/api/{app_name}/{{id}}", response_model=Quote)
def update_quote(id: int, quote: QuoteUpdateRequest):
    session = Session(bind=engine, expire_on_commit=False)

    if not (quote_record := session.query(QuoteRecord).get(id)):
        session.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if quote.quote:
        quote_record.quote = quote.quote

    if quote.author_name:
        quote.author_name = quote.author_name

    session.commit()

    session.close()

    json_compatible_item_data = jsonable_encoder(quote_record)
    return JSONResponse(content=json_compatible_item_data)


@app.delete(f"/api/{app_name}/{{id}}", response_model=Quote)
def delete_quote(id: int):
    session = Session(bind=engine, expire_on_commit=False)

    if not (quote_record := session.query(QuoteRecord).get(id)):
        session.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    session.delete(quote_record)
    session.commit()
    session.close()

    json_compatible_item_data = jsonable_encoder(quote_record)
    return JSONResponse(content=json_compatible_item_data)
