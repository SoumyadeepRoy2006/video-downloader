from typing import Self, NoReturn
from collections.abc import Callable
from abc import ABC, abstractmethod as abstract
from threading import Thread
import requests as request
from io import BytesIO
from PIL import Image
from .customexceptions import ProcessCancellationException
from .methods import get_info


class Event:
    _subscribers: list[Callable[..., None]]

    def __init__(self) -> None:
        self._subscribers = []

    def __iadd__(self, other: Callable[..., None]) -> Self:
        if other:
            self._subscribers.append(other)
        return self

    def __isub__(self, other: Callable[..., None]) -> Self:
        if other and other in self._subscribers:
            self._subscribers.remove(other)
        return self

    def invoke(self, *args, **kwargs) -> None:
        subscribers = list[Callable[..., None]](self._subscribers)
        for sub in subscribers:
            Thread(target=lambda: sub(*args, **kwargs)).start()


class Process(ABC):
    running: bool
    on_complete: Event

    def __init__(self) -> None:
        self._running = False
        self.on_complete = Event()

    @abstract
    def _run(self) -> None:
        pass

    def run(self) -> None:
        Thread(target=self._run).start()

    def cancel(self) -> NoReturn:
        self.running = False
        raise ProcessCancellationException("Process is running, exception uncaught")
    

class VideoInfoLoader(Process):
    query: str

    def __init__(self, query: str) -> None:
        super().__init__()
        self.query = query

    def _run(self) -> None:
        info = get_info(self.query)
        self.on_complete.invoke(info)


class ThumbnailLoader(Process):
    url: str

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    def _run(self) -> None:
        result = request.get(self.url)
        result.raise_for_status()

        if result.status_code == 200:
            data = BytesIO(result.content)
            image = Image.open(data)
            self.on_complete.invoke(image)
        else:
            self.on_complete.invoke(None)
        self.running = False
