import database, models

db = database.SessionLocal()
user = db.query(models.User).filter(models.User.username == "admin1").first()
user.role = "admin"
db.commit()
print("User promoted to admin!")