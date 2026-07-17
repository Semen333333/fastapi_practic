from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


balance = {}
class OperationRequest(BaseModel):
    wallet_name:str = Field(...,max_length=127)
    amount:float
    description:str|None = Field(None,max_length=250)
    @field_validator("amount")
    @classmethod
    def amount_not_negative(cls,v:float)->float:
        if v<=0:
            raise ValueError("")
        return v

    @field_validator("wallet_name")
    def not_empty(cls,v:str)->str:
        v = v.strip()
        if not v:
            raise ValueError("Name not fiend")
        return v


@app.get("/balance")
def get_balance(wallet_name:str|None = None):
    if wallet_name is None:
        return {"total balance":sum(balance.values())}
    if wallet_name not in balance:
        raise HTTPException(status_code = 404,
                            detail = f"wallet in not faind")
    return f"wallet:{wallet_name} balance:{balance[wallet_name]}"

@app.post("/balance/{name}")
def create_wallet(name:str,initial_balance:float = 0):
    if name in balance:
        raise HTTPException(status_code=400,detail = "this wallet has already been created")
    balance[name] = initial_balance
    return {
        "message":f"Wallet {name} created",
        "wallet":name,
        "balance":balance[name]
    }
@app.post("/operations/income")
def add_income(operation:OperationRequest):
    if operation.wallet_name not in balance:
        raise HTTPException(status_code=400,detail = "wallet not found")
    balance[operation.wallet_name]+=operation.amount
    return {
        "amount":operation.amount,
        "balance":balance[operation.wallet_name]
    }

@app.post("/operations/expense")
def add_expense(operation:OperationRequest):
    if operation.wallet_name not in balance:
        raise HTTPException(status_code=400,detail = "wallet not found")
    if operation.amount>balance[operation.wallet_name]:
        raise HTTPException(status_code=400,detail = "сумма больше чем есть на счете")
    balance[operation.wallet_name] -= operation.amount
    return {
        "amount":operation.amount,
        "balance":balance[operation.wallet_name]
    }