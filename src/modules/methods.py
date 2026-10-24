from typing import Any, Literal, TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from yt_dlp.extractor.common import _InfoDict
    from yt_dlp import _Params

from .customexceptions import DownloadCancellationException as CancelException
from .dictionaries import VideoInfo, FormatInfo, SimplifiedSize
from pathlib import Path
from yt_dlp import YoutubeDL

SRC = Path(__file__).parent.parent
FFMPEG_PATH = SRC / "bin"
cancellation: bool = False

def simplify_size(value: float | int, unit: Literal["b", "mb", "kb", "gb"] = "b") -> SimplifiedSize:
    if value < 1024 or unit == "gb":
        if value % 1024 and not unit=="b":
            value = int(value * 10)
            value /= 10

        if not value*10 % 10:
            value = int(value)

        return {"value": value, "unit": unit}
    else:
        if value % 1024:
            value /= 1024
        else:
            value = int(value / 1024)
        match unit:
            case "b":
                unit = "kb"
            case "kb":
                unit = "mb"
            case "mb":
                unit = "gb"
        return simplify_size(value, unit)

def is_digit(string_value:str) -> bool:
    try:
        int(string_value)
        return True
    except ValueError:
        return False

def get_info(video_url: str) -> VideoInfo:
    params: _Params = {
        "skip_download": "True",
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }
    info: VideoInfo

    with YoutubeDL(params) as ytdlp:
        allinfo: _InfoDict = ytdlp.extract_info(video_url, download=False)

        info = {
            "id": str(allinfo["id"]),
            "channel_name": allinfo.get("uploader") or "Failed to get channel name",
            "title": str(allinfo.get("title")),
            "thumbnail": f"https://i.ytimg.com/vi/{allinfo["id"]}/maxresdefault.jpg",
            "formats": [],
        }

        all_formats: Optional[list[dict[str, Any]]] = allinfo.get("formats")
        if all_formats:
            for format in all_formats:
                if ( format.get("ext") == "mp4"
                    and format.get("audio_ext") == "none"
                    and format.get("format_note")
                    and format.get("fps")
                    and (format.get("filesize") or format.get("filesize_approx"))
                ):
                    x: FormatInfo = {
                        "id": int(format["format_id"]) if is_digit(format["format_id"]) else format["format_id"],
                        "res": int(str(format["format_note"]).split("p")[0]),
                        "resolution": format["resolution"],
                        "frame_rate": format["fps"],
                        "bitrate": format["tbr"],
                        "size": format.get("filesize") or format.get("filesize_approx") or 0,
                    }
                    info["formats"].append(x)
    info["formats"].sort(key=lambda x: (x["res"], x["size"]), reverse=True)
    return info

def download_video(video_url: str, format_id: int | str, download_location: Path | str) -> None:
    params: _Params = {
        "format": f"{format_id}+ba",
        "merge_output_format": "mp4",
        "outtmpl":  str(download_location) + "/%(title)s.%(ext)s",
        "ffmpeg_location": str(FFMPEG_PATH),
        "noprogress": True,
        "no_warnings": True,
        "quiet": True
    }

    with YoutubeDL(params) as ytdlp:
        try:
            ytdlp.download([video_url])
        except KeyboardInterrupt:
            print("Download interrupted")
        except CancelException:
            print("Download cancelled")
            global cancellation
            cancellation = False
