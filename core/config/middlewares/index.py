import jwt, json
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import dotenv_values
from config.services.redis.index import ServiceRedis
from config.services.postgres.index import ServicePostgres

config = dotenv_values(f".env.{dotenv_values('.env').get('PYTHON_ENV')}")


class appMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        psql_connection = ServicePostgres()
        headers = request.headers.get("authorization", None)
        has_error = ""

        # print("RED", redis_connection.get_connection_health())
        try:
            # if request.url.path == "/docs" or request.url.path == "/openapi.json":
            #     response = await call_next(request)
            #     return response
            has_error = ""
            if not headers:
                raise HTTPException(status_code=401, detail="AUTHENTICATION ERROR")
            if "Bearer" not in headers:
                raise HTTPException(status_code=401, detail="INVALID TOKEN")
            authorization = headers.replace("Bearer ", "")

            jwt_decoded = await self.verifyJwt(authorization)
            get_user_psql = await psql_connection.selectUser(
                req=request, value=jwt_decoded.get("user_id")
            )
            if not get_user_psql:
                raise HTTPException(status_code=401, detail="PSQL AUTHENTICATION ERROR")

            await self.tokenLifeCycle(jwt_decoded, authorization)
            request.state.permissions = get_user_psql.get("permissions")

        except Exception as ex:
            has_error = ex
        finally:
            if has_error:
                return JSONResponse(
                    status_code=has_error.status_code,
                    content={"message": has_error.detail},
                )

            response = await call_next(request)
            return response

    async def verifyJwt(self, value):
        tokens = {"tokens": {"active": [], "blocked": []}}
        try:
            jwt_decoded = jwt.decode(
                jwt=value,
                key=config.get("SECRET_JWT"),
                options={"verify_exp": True},
                algorithms=["RS256"],
            )
        except Exception as ex:
            raise HTTPException(status_code=401, detail="InvalidSignatureError")
        finally:
            return jwt_decoded

    async def tokenLifeCycle(self, jwt_decoded, authorization):
        redis_connection = ServiceRedis()
        try:
            session = await redis_connection.getToken(key=jwt_decoded.get("user_id"))
            if session == None:
                token_list = {"tokens": {"active": [authorization], "blocked": []}}
                await redis_connection.storeToken(key=jwt_decoded.get("user_id"), value=token_list)
                session = await redis_connection.getToken(key=jwt_decoded.get("user_id"))
                print("Sessao Nova")
                return session

            if authorization in session.get("tokens").get("blocked"):
                raise HTTPException(status_code=401, detail="AUTHENTICATION ERROR")

            # if authorization in session.get("tokens").get("active"):
            #     print("sessao ativa")
            #     return session  # O Acess Token é utilizado neste middlare, o endpoint do token que será responsavel por devolver um access token e refresh token

        except Exception:
            raise HTTPException(status_code=401, detail="AUTHENTICATION ERROR")

