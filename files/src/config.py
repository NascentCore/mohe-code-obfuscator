import os
from dataclasses import dataclass


@dataclass
class APIConfig:
    external_address_header: str = os.getenv(
        "EXTERNAL_ADDRESS_HEADER", "X-Envoy-External-Address"
    )
    users_base_url = os.getenv("USERS_BASE_URL", "http://localhost:9004")
    user_id_header: str = os.getenv("USER_ID_HEADER", "X-User-ID")
    bases_base_url = os.getenv("BASES_BASE_URL", "http://localhost:9005")


@dataclass
class APIServerConfig:
    port: int = os.getenv("API_PORT", 9001)
    host: str = os.getenv("API_HOST", "0.0.0.0")
    workers: int = int(os.getenv("API_WORKERS", 1))
    timeout: int = int(os.getenv("API_TIMEOUT", 10))


@dataclass
class DBConfig:
    dialect: str = os.getenv("DB_DIALECT", "postgresql")
    driver: str = os.getenv("DB_DRIVER", "psycopg")
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", 5432))
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "postgres")
    name: str = os.getenv("DB_NAME", "workbench-files")
    ssl: bool = os.getenv("DB_SSL", "false").lower() == "true"


@dataclass
class DBPoolConfig:
    max_size: int = int(os.getenv("DB_POOL_MAX_SIZE", 10))
    max_overflow: int = int(os.getenv("DB_POOL_MAX_OVERFLOW", 5))
    timeout: int = int(os.getenv("DB_POOL_TIMEOUT", 30))
    recycle: int = int(os.getenv("DB_POOL_RECYCLE", 300))
    pre_ping: bool = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"


@dataclass
class FilesConfig:
    base_path: str = os.getenv("BASE_PATH", "/data/workbench-files")

    @property
    def allowed_extensions(self) -> list[str]:
        if extensions := os.getenv(
            "ALLOWED_EXTENSIONS",
            "pdf,doc,docx,xls,xlsx,ppt,pptx,txt,markdown,md,jpg,jpeg,png",
        ):
            return extensions.split(",")

    @property
    def max_file_size(self) -> int:
        """
        Max file size in bytes, default 100MB
        """
        return int(os.getenv("MAX_FILE_SIZE_MB", 100)) * 1024 * 1024
