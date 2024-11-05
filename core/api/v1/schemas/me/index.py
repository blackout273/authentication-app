from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ...models.model_responses import Response

router_me = APIRouter()


@router_me.get("/")
async def main() -> Response:
    handler_error: str = ""
    response: Response = {"message": "Processando", "status": 400}
    try:
        pass
    except Exception as ex:
        handler_error = ex
    finally:
        return response
