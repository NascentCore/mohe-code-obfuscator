from sqlalchemy import create_engine, Engine, URL

from .config import DBConfig, DBPoolConfig


def get_url(config: DBConfig) -> str:
    return URL(
        drivername=f"{config.dialect}+{config.driver}",
        username=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.name,
        query={"sslmode": "require" if config.ssl else "disable"},
    ).render_as_string(hide_password=False)


def get_engine(
    config: DBConfig,
    pool_config: DBPoolConfig,
) -> Engine:
    url = get_url(config)
    return create_engine(
        url,
        pool_size=pool_config.max_size,
        max_overflow=pool_config.max_overflow,
        pool_timeout=pool_config.timeout,
        pool_recycle=pool_config.recycle,
        pool_pre_ping=pool_config.pre_ping,
    )


url = get_url(DBConfig())
engine = get_engine(DBConfig(), DBPoolConfig())
