from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from ...models.model_responses import Response
from ...services.index import AuthPermissions
from fastapi.security import HTTPBearer

router_me = APIRouter()


@router_me.get(
    "/",
    dependencies=[
        Security(HTTPBearer()),
        Security(
            AuthPermissions(
                [
                    "5951d0fe-e756-44b3-9bf9-4d7ef753444e",
                    "3f97190c-f6d6-4e4a-8523-5edbccb2ff70",
                ]
            )
        ),
    ],
)
async def main() -> Response:
    handler_error: str = ""
    response: Response = {"message": "Processando", "status": 400}
    try:
        pass
    except Exception as ex:
        handler_error = ex
    finally:
        return response
