from enum import StrEnum
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pydantic import PostgresDsn, MongoDsn, AmqpDsn, computed_field
from yarl import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, env_ignore_empty=True
    )

    # app info
    PROJECT_NAME: str = "Nexus Iot"
    API_V1_STR: str = "/api/v1"
    DEBUG_MODE: bool
    ENVIRONMENT: Literal["dev", "stg", "prod"]
    # security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTE: int = 30

    # postgresl
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    # mongodb
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_HOST: str
    MONGO_DB_NAME: str
    MONGO_PORT: int

    # rabbitmq
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                port=self.POSTGRES_PORT,
                host=self.POSTGRES_HOST,
                path=self.POSTGRES_DB
            )
        )

    @computed_field
    @property
    def MONGO_DATABASE_URL(self) -> str:
        return str(
            MongoDsn.build(
                scheme="mongodb",
                host=self.MONGO_HOST,
                port=self.MONGO_PORT,
                username=self.MONGO_INITDB_ROOT_USERNAME,
                password=self.MONGO_INITDB_ROOT_PASSWORD,
            )
        )

    @computed_field
    @property
    def RABBITMQ_URL(self) -> str:
        return str(
            AmqpDsn.build(
                scheme="amqp",
                port=self.RABBITMQ_PORT,
                host=self.RABBITMQ_HOST,
                username=self.RABBITMQ_USERNAME,
                password=self.RABBITMQ_PASSWORD,
            )
        )


settings = Settings()
if settings.DEBUG_MODE:
    print(settings.model_dump_json(indent=2))
