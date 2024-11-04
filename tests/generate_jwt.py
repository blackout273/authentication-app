import jwt
with open(file="private.pem",mode='r') as folder:
    encoded = jwt.encode(payload={"some": "payload"},key=folder.read(), algorithm="RS256")
    print(encoded)
