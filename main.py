from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction, Merchant, Payer
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import and_

app = FastAPI()
app.openapi_version = "3.0.3"


class PayerIdRequestBody(BaseModel):
    payer_id: Optional[int]


class DateRangeRequestBody(BaseModel):
    start_date: str
    end_date: str


class MerchantNameRequestBody(BaseModel):
    merchant_name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_payer/")
def create_account(
    name: str,
    email: str,
    phone_number: str,
    account_balance: float = 0,
    db: Session = Depends(get_db),
):
    payer = Payer(
        name=name,
        email=email,
        phone_number=phone_number,
        account_balance=account_balance,
    )
    db.add(payer)
    db.commit()
    db.refresh(payer)
    return payer


@app.post("/check_balance/")
def check_balance(request: PayerIdRequestBody, db: Session = Depends(get_db)):
    payer = db.query(Payer).filter(Payer.payer_id == request.payer_id).first()
    if payer:
        return payer
    else:
        raise HTTPException(status_code=404, detail="Payer not found")


@app.post("/filter_transactions/")
def filter_transactions(request: DateRangeRequestBody, db: Session = Depends(get_db)):
    try:

        start_date = datetime.strptime(request.start_date, "%d%m%Y")
        end_date = datetime.strptime(request.end_date, "%d%m%Y")

        if start_date > end_date:
            raise HTTPException(
                status_code=400, detail="Start date must be before or equal to end date"
            )

        transactions = (
            db.query(Transaction)
            .filter(
                and_(
                    Transaction.transaction_date >= start_date,
                    Transaction.transaction_date <= end_date,
                )
            )
            .all()
        )

        return transactions

    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Please use 'ddmmyyyy'."
        )


@app.post("/filter_by_merchant/")
def filter_by_merchant(request: MerchantNameRequestBody, db: Session = Depends(get_db)):
    merchant = db.query(Merchant).filter(Merchant.name == request.merchant_name).first()

    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    transactions = (
        db.query(Transaction)
        .filter(Transaction.merchant_id == merchant.merchant_id)
        .all()
    )

    return transactions
