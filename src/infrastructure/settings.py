from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationSettings(BaseModel):
    """
    Application settings.
    """

    name: str = "football-fan"
    version: str = "0.0.1"
    description: str = "Football Fan API"
    root_path: str = "/football-fan"


class APISettings(BaseModel):
    """
    API settings.
    """

    version: str = "v1"
    path: str = "/api/v1"


class ServerSettings(BaseModel):
    """
    Server settings.
    """

    http_port: int = 3000


class FeatureFlags(BaseModel):
    """
    Feature flags.
    """

    pass


class LoggerSettings(BaseModel):
    """
    Logger settings.
    """

    name: str = "football-fan-api"
    level: str = "TRACE"
    fmt: str = (
        "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
    )
    file: str = "app.log"
    max_bytes: int = 1048576  # 1MB
    backup_count: int = 5  # Number of backup log files to keep


class PostgresSettings(BaseModel):
    """
    Postgres settings.
    """

    dialect: str = "postgresql+psycopg2"
    host: str = "localhost"
    port: int = 5432
    database_name: str = "postgres"
    username: str = "postgres"
    password: str = "postgres"

    @property
    def url(self):
        """
        Get the postgres URL.
        """
        return f"{self.dialect}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"


class CorsSettings(BaseModel):
    """
    CORS settings.
    """

    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers: list[str] = ["*"]


class Settings(BaseSettings):
    """
    Settings class that loads the application settings from the configuration file.
    """

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )
    py_env: str = "local"  # Settings type (local, dev, prod)
    app: ApplicationSettings = ApplicationSettings()
    api: APISettings = APISettings()
    server: ServerSettings = ServerSettings()
    feature_flags: FeatureFlags = FeatureFlags()
    logger: LoggerSettings = LoggerSettings()
    postgres: PostgresSettings = PostgresSettings()
    cors: CorsSettings = CorsSettings()

    @property
    def is_production(self):
        """
        Check if the environment is production.
        """
        return self.py_env == "production"

    @staticmethod
    @lru_cache()
    def load():
        """
        Load the environment.
        """
        return Settings()


def get_settings():
    """
    Dependency that provides application settings.
    This function loads the application settings from the configuration file.

    Returns
    -------
    Settings
        An instance of the Settings class containing the application configuration.
    """
    settings = Settings.load()
    if not settings:
        raise ValueError("Settings could not be loaded")
    return settings
