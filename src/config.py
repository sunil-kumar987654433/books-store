from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str
    REDIS_PORT: int

    MAIL_USERNAME: str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_SERVER:str

    REDIS_URL: str # it is same as broker url



    model_config = SettingsConfigDict(
        env_file = '.env',
        extra="ignore"
    )

Config = Settings()

broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL