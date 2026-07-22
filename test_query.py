from database import SessionLocal,User

db = SessionLocal()

try:
    user = db.query(User).filter(User.name == "Аня").first()
    user.age = 23
    db.delete(user)
    db.commit()
    print("успешно")

except AttributeError:
    print("Пользователь не найден")
finally:
    db.close()

