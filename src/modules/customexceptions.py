from yt_dlp.utils import YoutubeDLError


class DownloadCancellationException(YoutubeDLError):
    def __init__(self, msg: str | None = None) -> None:
        super().__init__(msg)


class ProcessCancellationException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)