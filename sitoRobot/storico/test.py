import jwt
import datetime

SECRET_KEY = "mysecretkey"

# Creazione del token
expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
token = jwt.encode({"username": "test_user", "exp": expiration}, SECRET_KEY, algorithm="HS256")

print("Token generato:", token)

# Decodifica del token
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
print("Token decodificato:", decoded)
