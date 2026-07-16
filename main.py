print('hello word')

@app.get("/")
def message():
    return "привет"

@app.get("/products")
def products():
    return {"items": ["товар1", "товар2"]}

@app.get("/products/{product_id}")
def products_id(product_id:int):
    return {"id":product_id,"name":f"товар номер{product_id}"}
@app.get("/users")
def products():
    return {"items": ["user2", "user1"]}
@app.get("/users/{users_id}")
def users(user_id:int):
    return {f"user_id":user_id,"status":"active"}