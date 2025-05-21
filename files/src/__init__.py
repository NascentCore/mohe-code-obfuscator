from pathlib import Path

__title__ = "workbench_files"

def _get_version():
    with open(Path(__file__).parent / "VERSION") as f:
        return f.read().strip()


__version__ = _get_version()
