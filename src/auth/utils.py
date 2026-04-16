import uuid
import logging
from passlib.context import CryptContext
context = CryptContext(
    schemes=['argon2', "pbkdf2_sha256"]
)
from src.config import Config
import jwt
from datetime  import datetime, timedelta
class UserPassword:

    @staticmethod
    def generate_password(password):
        return context.hash(password)
    

    @staticmethod
    def verify_password(password, hashed_password):
        return context.verify(password, hashed_password)
    
class HashingToken:

    @staticmethod
    def encode_data(payload: dict):
        data = payload.copy()
        data['jti'] = str(uuid.uuid4())
        return jwt.encode(payload=payload, algorithm=Config.JWT_ALGORITHM, key=Config.JWT_SECRET)
    
    @staticmethod
    def decode_data(encoded_jwt):
        try:
            return jwt.decode(encoded_jwt, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        except jwt.PyJWKError as e:
            logging.exception(e)