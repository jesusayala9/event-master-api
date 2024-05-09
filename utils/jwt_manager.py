# from jwt import encode
# from jwt import decode

# # crear token

# # encode recibe(dato, key, algoritmo para cifrar)


# def create_token(data: dict):
#     token: str = encode(payload=data, key='my_secret_key', algorithm='HS256')
#     return token

# # decode recibe(dato, key, algoritmo para decifrar el token)

# def validate_token(token: str) -> dict:
#     data: dict = decode(token, key='my_secret_key', algorithms=['HS256'])
#     return data
