import argparse
import subprocess
from pathlib import Path


from . import __title__, __version__
from .config import APIServerConfig, FilesConfig


def main():
    parser = argparse.ArgumentParser(prog=__title__)

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(title="commands", dest="command")

    api_parser = subparsers.add_parser("api", help="Start the API server")
    api_parser.add_argument(
        "--reload",
        action="store_true",
        default=False,
        help="API reload (default: %(default)s)",
    )

    migrate_parser = subparsers.add_parser("migrate", help="Run database migrations")

    init_parser = subparsers.add_parser("init", help="Initialize the storage")

    args = parser.parse_args()

    match args.command:
        case "api":
            _start_api(args.reload)
        case "init":
            _init_storage()
        case "migrate":
            _migrate()
        case _:
            parser.print_help()
            exit(1)


def _migrate():
    """Migrate the database with Alembic."""
    from alembic import command
    from alembic.config import Config

    src = Path(__file__).parent
    alembic_cfg = Config(src / "alembic.ini")
    alembic_cfg.set_main_option("script_location", str(src / "migrations"))
    command.upgrade(alembic_cfg, "head")


def _start_api(reload: bool):
    config = APIServerConfig()
    command = [
        "uvicorn",
        f"src.app:app",
        "--host",
        str(config.host),
        "--port",
        str(config.port),
        "--workers",
        str(config.workers),
        "--timeout-keep-alive",
        str(config.timeout),
    ]

    if reload:
        command.extend(["--reload", "--reload-dir", "src"])

    subprocess.run(command)


def _init_storage():
    """Ensure the base path exists."""
    config = FilesConfig()
    base_path = Path(config.base_path)
    base_path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()
