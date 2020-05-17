from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'postgresql://postgres:mysecretpassword@db/simple_wallet'


settings = Settings()
