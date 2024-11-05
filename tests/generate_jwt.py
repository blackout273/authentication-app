import jwt, datetime, json
from datetime import timedelta, datetime

with open(file="private.pem", mode="r") as folder:
    private_key = folder.read()

    payload = {
        "permissions":json.dumps(["5951d0fe-e756-44b3-9bf9-4d7ef753444e","3f97190c-f6d6-4e4a-8523-5edbccb2ff70"]),
        "exp": int((datetime.now() + timedelta(days=30)).timestamp()),
        "iat": int(datetime.now().timestamp()),
    }

    encoded = jwt.encode(payload=payload, key=private_key, algorithm="RS256")
    print(encoded)
