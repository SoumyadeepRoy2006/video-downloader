from typing import TypedDict, Literal


class SimplifiedSize(TypedDict):
    value: int | float
    unit: Literal["b", "mb", "kb", "gb"]


class FormatInfo(TypedDict):
    id: int
    resolution: str
    res: int
    frame_rate: int
    bitrate: int
    size: int


class VideoInfo(TypedDict):
    id:str
    title: str
    channel_name: str
    thumbnail: str
    formats: list[FormatInfo]
