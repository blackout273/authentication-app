import jwt, datetime
from datetime import timedelta, datetime

with open(file="private.pem", mode="r") as folder:
    private_key = folder.read()

    payload = {
        "some": "payload",
        "exp": int((datetime.now() + timedelta(days=30)).timestamp()),
        "iat": int(datetime.now().timestamp()),
    }

    encoded = jwt.encode(payload=payload, key=private_key, algorithm="RS256")
    print(encoded)
