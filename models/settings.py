from dataclasses import dataclass


@dataclass(slots=True)
class Settings:

    download_path: str = ""

    write_exif: bool = True

    write_file_date: bool = True

    max_quality: bool = True

    continue_download: bool = True

    theme: str = "dark"

    workers: int = 8