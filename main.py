from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction, Merchant, Payer
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from sqlalchemy import and_

app = FastAPI()
app.openapi_version = "3.0.3"


# Pydantic Models cho Request Body
class PayerCreateRequest(BaseModel):
    name: str
    email: str
    phone_number: str
    account_balance: int = 0


class PayerIdRequestBody(BaseModel):
    payer_id: int


class DateRangeRequestBody(BaseModel):
    start_date: str  # ddmmyyyy
    end_date: str  # ddmmyyyy


class MerchantNameRequestBody(BaseModel):
    merchant_name: str


# Pydantic Models cho Responses
class PayerResponse(BaseModel):
    payer_id: int
    name: str
    email: str
    phone_number: str
    account_balance: int

    class Config:
        orm_mode = True


class TransactionResponse(BaseModel):
    transaction_id: int
    payer_id: int
    merchant_id: int
    transaction_amount: float
    transaction_date: datetime

    class Config:
        orm_mode = True


# Dependency để lấy Session từ database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Tạo Payer mới
@app.post("/create_payer/", response_model=PayerResponse)
def create_account(request: PayerCreateRequest, db: Session = Depends(get_db)):
    payer = Payer(
        name=request.name,
        email=request.email,
        phone_number=request.phone_number,
        account_balance=request.account_balance,
    )
    db.add(payer)
    db.commit()
    db.refresh(payer)
    return payer


# Kiểm tra số dư của Payer
@app.post("/check_balance/", response_model=PayerResponse)
def check_balance(request: PayerIdRequestBody, db: Session = Depends(get_db)):
    payer = db.query(Payer).filter(Payer.payer_id == request.payer_id).first()
    if payer:
        return payer
    else:
        raise HTTPException(status_code=404, detail="Payer not found")


# Lọc các giao dịch theo khoảng thời gian
@app.post("/filter_transactions/", response_model=List[TransactionResponse])
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


# Lọc các giao dịch theo tên Merchant
@app.post("/filter_by_merchant/", response_model=List[TransactionResponse])
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
