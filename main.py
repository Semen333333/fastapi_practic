from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field, field_validator
from database import SessionLocal, Wallets

app = FastAPI()

class OperationRequest(BaseModel):
    wallet_name:str = Field(...,max_length=127)
    amount:float
    description:str|None = Field(None,max_length=250)
    @field_validator("amount")
    def amount_not_negative(cls,v:float)->float:
        if v<0:
            raise ValueError("")
        return v

    @field_validator("wallet_name")
    def not_empty(cls,v:str)->str:
        v = v.strip()
        if not v:
            raise ValueError("Name not fiend")
        return v

class CreateBalance(BaseModel):
    wallet_name:str = Field(...,max_length=127)
    amount:float
    @field_validator("wallet_name")
    def name_empty(cls,v:str)->str:
        v = v.strip()
        if not v:
            raise ValueError("Name not fiend")
        return v
    @field_validator("amount")
    def create_amount_not_negative(cls,v:float)->float:
        if v<=0:
            raise ValueError("")
        return v

@app.get("/balance")
def get_balance(wallet_name:str|None = None):
    db = SessionLocal()
    if wallet_name is None:
        return {"total balance": sum(s[0] for s in (db.query(Wallets.balance)).all())}
    wallet = db.query(Wallets).filter(Wallets.wallet_name == wallet_name).first()
    if wallet is None:
        raise HTTPException(status_code = 404,
                            detail = f"wallet in not faind")
    resalt = f"wallet:{wallet_name} balance:{wallet.balance}"
    db.close()
    return resalt

@app.post("/wallets")
def create_wallet(wallet:CreateBalance):
    db = SessionLocal()
    if db.query(Wallets).filter(Wallets.wallet_name == wallet.wallet_name).first():
        raise HTTPException(status_code=400,detail = "this wallet has already been created")
    new_wallet = Wallets(wallet_name= wallet.wallet_name,balance = wallet.amount)
    db.add(new_wallet)
    db.commit()
    db.close()
    resalt =  {
        "message":f"Wallet {wallet.wallet_name} created",
        "wallet":wallet.wallet_name,
        "balance":new_wallet.balance
    }
    db.close()
    return resalt

@app.post("/operations/income")
def add_income(operation:OperationRequest):
    db = SessionLocal()
    wallet = db.query(Wallets).filter(Wallets.wallet_name ==operation.wallet_name).first()
    if wallet is None:
        raise HTTPException(status_code=400,detail = "wallet not found")
    wallet.balance +=operation.amount
    db.commit()
    resalt =  {
        "amount":operation.amount,
        "balance":wallet.balance
    }
    db.close()
    return resalt

@app.post("/operations/expense")
def add_expense(operation:OperationRequest):
    db = SessionLocal()
    wallet = db.query(Wallets).filter(Wallets.wallet_name == operation.wallet_name).first()
    if wallet is None:
        raise HTTPException(status_code=400,detail = "wallet not found")
    if operation.amount>wallet.balance:
        raise HTTPException(status_code=400,detail = "сумма больше чем есть на счете")
    wallet.balance -=operation.amount
    db.commit()
    resalt = {
        "amount":operation.amount,
        "balance":wallet.balance
    }
    db.close()
    return resalt