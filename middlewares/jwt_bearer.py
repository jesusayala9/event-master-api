from fastapi.security import HTTPBearer
from fastapi import Request
from utils.jwt_manager import create_token, validate_token
from fastapi import HTTPException


# # validar datos del usuario
# class JWTBearer(HTTPBearer):
#     async def __call__(self, request: Request):
#         auth = await super().__call__(request)  # obtiene las credenciales del token
#         # valida y decodificar y devuelve los datos contenidos.
#         data = validate_token(auth.credentials)
#         if data['email'] != 'admin@gmail.com':
#             raise HTTPException(
#                 status_code=403, detail='Credenciales son invalidas')

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # Obtener las credenciales del token del encabezado de autorización
        auth = await super().__call__(request)

        # Validar el token JWT
        if not auth:
            raise HTTPException(status_code=401, detail="Token de autenticación no proporcionado")
        if not validate_token(auth.credentials):
            raise HTTPException(status_code=401, detail="Token de autenticación inválido")

        # Si el token es válido, devuelve True
        return True