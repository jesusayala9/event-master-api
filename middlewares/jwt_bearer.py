from fastapi.security import HTTPBearer
from fastapi import Request
from utils.jwt_manager import create_token, validate_token
from fastapi import HTTPException


# validar datos del usuario
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)  # obtiene las credenciales del token
        # valida y decodificar y devuelve los datos contenidos.
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(
                status_code=403, detail='Credenciales son invalidas')