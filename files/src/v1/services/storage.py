import shutil
from pathlib import Path
from uuid import UUID, uuid4

from ...config import FilesConfig


class LocalStorageService:
    def __init__(self, config: FilesConfig):
        self.base_path = config.base_path

    def get_path(self, filename: str, user_id: UUID) -> Path:
        """
        Rename file to uuid and save it in the user's directory.
        """
        # TODO: due to performance issues, consider split to subdirectories by prefix
        directory = Path(self.base_path) / str(user_id)
        if not directory.exists():
            directory.mkdir(parents=True)

        file_uuid = uuid4()
        filename = f"{file_uuid}{Path(filename).suffix}"

        return directory / filename

    def save_binary(self, data: bytes, path: Path):
        with open(path, "wb") as f:
            shutil.copyfileobj(data, f)

    def delete(self, path: Path):
        if path.exists():
            path.unlink()
