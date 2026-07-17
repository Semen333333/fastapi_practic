from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app = FastAPI()


balance = {}
class OperationRequest(BaseModel):
    wallet_name:str
    amount:float
    description:str|None = None


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
    elif operation.amount<0:
        raise HTTPException(status_code=400, detail="amount not be negative ")
    balance[operation.wallet_name]+=operation.amount
    return {
        "amount":operation.amount,
        "balance":balance[operation.wallet_name]
    }

@app.post("/operations/expense")
def add_expense(operation:OperationRequest):
    if operation.wallet_name not in balance:
        raise HTTPException(status_code=400,detail = "wallet not found")
    elif operation.amount<0:
        raise HTTPException(status_code=400, detail="amount not be negative ")
    balance[operation.wallet_name] -= operation.amount
    return {
        "amount":operation.amount,
        "balance":balance[operation.wallet_name]
    }