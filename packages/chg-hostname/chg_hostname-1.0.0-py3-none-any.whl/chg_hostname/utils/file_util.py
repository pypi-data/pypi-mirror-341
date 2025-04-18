from pathlib import Path


class FileUtil:
    path: str
    pure_path: Path

    def __init__(self, path: str):
        self.path = path
        self.does_file_exist()

    def does_file_exist(self) -> None:
        self.pure_path = Path(self.path)

        if not self.pure_path.exists():
            raise FileExistsError(f"{self.path} file not found")

    def get(self) -> Path:
        return self.pure_path

    def get_content(self) -> list[str]:
        return self.pure_path.read_text().splitlines(keepends=True)
