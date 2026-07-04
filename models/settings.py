from dataclasses import asdict
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:

    download_path: str = ""

    write_exif: bool = True

    write_file_date: bool = True

    download_max_quality: bool = True

    continue_download: bool = True

    theme: str = "dark"

    threads: int = 8

    @classmethod
    def from_dict(cls, data: dict) -> "Settings":

        return cls(
            download_path=data.get("download_path", ""),
            write_exif=data.get("write_exif", True),
            write_file_date=data.get("write_file_date", True),
            download_max_quality=data.get("download_max_quality", True),
            continue_download=data.get("continue_download", True),
            theme=data.get("theme", "dark"),
            threads=data.get("threads", 8),
        )

    def to_dict(self) -> dict:

        return asdict(self)
