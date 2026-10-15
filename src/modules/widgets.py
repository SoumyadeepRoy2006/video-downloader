from typing import Literal
from .dictionaries import VideoInfo, FormatInfo, SimplifiedSize
from .objects import Event, VideoInfoLoader, ThumbnailLoader
from .methods import simplify_size
from PIL import Image
from PIL.ImageFile import ImageFile
from tkinter import Event as TkEvent
from customtkinter import (
    CTk,
    CTkBaseClass,
    CTkFrame as Frame,
    CTkScrollableFrame as ScrollableFrame,
    CTkLabel as Label,
    CTkButton as Button,
    CTkEntry as Entry,
    CTkImage
)


class SearchBar(Frame):
    inner_frame: Frame
    input_main: Entry
    search_button: Button

    active: bool
    on_query: Event

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.active = True
        self.on_query = Event()
        self.pack_propagate(False)

        self.inner_frame = Frame(self, corner_radius=0, fg_color="transparent")
        self.inner_frame.grid_columnconfigure(0, weight=8)
        self.inner_frame.grid_columnconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(2, weight=2)
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_propagate(False)

        self.input_main = Entry(
            self.inner_frame,
            placeholder_text="Enter video URL or ID(YouTube only)",
            fg_color="#202020",
            font=("Segoe UI", 14),
            corner_radius=20,
            border_width=0,
            border_color="#D00030"
        )
        self.input_main.set("dQw4w9WgXcQ")
        self.input_main.bind("<FocusIn>", self._input_mouse_focus)
        self.input_main.bind("<FocusOut>", self._input_mouse_unfocus)

        self.search_button = Button(
            self.inner_frame,
            text="Search",
            text_color="#D00030",
            font=("Segoe UI", 16, "bold"),
            fg_color="#282828",
            height=40,
            width=0,
            border_width=1,
            border_color="#D00030",
            corner_radius=20,
            cursor="hand2",
            command=self.search
        )
        self.search_button.bind("<Enter>", self._button_mouse_enter)
        self.search_button.bind("<Leave>", self._button_mouse_exit)

        self.inner_frame.pack(padx=20, pady=20, fill="both")
        self.input_main.grid(row=0, column=0, sticky="ewns")
        self.search_button.grid(row=0, column=2, sticky="ewns")

    def search(self) -> None:
        query: str = self.input_main.get().strip()
        if query and query != "" and not " " in query:
            self.on_query.invoke(query)
            self.set_active(False)

    def set_active(self, state: bool) -> None:
        widgets = list[CTkBaseClass]([self.input_main, self.search_button])
        self.active = state
        for widget in widgets:
            widget.configure(state="normal" if state else "disabled")
        if not state:
            self._button_mouse_exit(force=True)
            self._input_mouse_unfocus(force=True)
        else:
            self._button_mouse_exit() # It magically fixes the abnormal button shrinking 

    def _input_mouse_focus(self, _: TkEvent | None = None, force: bool = False) -> None:
        if self.active or force:
            self.input_main.configure(border_width=1)

    def _input_mouse_unfocus(self, _: TkEvent | None = None, force: bool = False) -> None:
        if self.active or force:
            self.input_main.configure(border_width=0)

    def _button_mouse_enter(self, _: TkEvent | None = None, force: bool = False) -> None:
        if self.active or force:
            self.search_button.configure(text_color="white", fg_color="#D00030")

    def _button_mouse_exit(self, _: TkEvent | None = None, force: bool = False) -> None:
        if self.active or force:
            self.search_button.configure(text_color="#D00030", fg_color="#282828")


class VideoInfoWindow(Frame):
    default_image: Image.Image

    thumbnail: Label
    title: Label
    channel_name: Label

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.default_image = Image.new("RGBA", (1, 1), "#0000")

        self.thumbnail = Label(self, width=480, height=270, text="", anchor="w", justify="left")
        self._set_default_image()
        self.title = Label(self, text="", font=("Segoe UI", 15, "bold"), anchor="w", justify="left", wraplength=480)
        self.channel_name = Label(self, text="", font=("Segoe UI", 15), anchor="w", justify="left", wraplength=480)

        self.thumbnail.pack(fill="x")
        self.title.pack(fill="x", pady=20)
        self.channel_name.pack(fill="x")

    def _set_default_image(self) -> None:
        self.thumbnail.configure(image=CTkImage(light_image=self.default_image, dark_image=self.default_image, size=(480, 270)))

    def set_info(self, info: VideoInfo) -> None:
        self.title.configure(text=info["title"])
        self.channel_name.configure(text=info["channel_name"])

    def set_thumbnail(self, image: ImageFile) -> None:
        self.thumbnail.configure(image=CTkImage(light_image=image, dark_image=image, size=(480, 270)))

    def clear(self) -> None:
        self._set_default_image()
        self.title.configure(text="")
        self.channel_name.configure(text="")


class FormatInfoWindow(Frame):
    resolution: str
    res: int
    fps: int
    size: int
    bitrate: float

    details_main_window: Frame

    primary_details_window: Frame
    secondary_details_window: Frame

    res_label: Label
    resolution_label: Label
    fps_label: Label

    size_label: Label
    bitrate_label: Label

    download_button: Button

    def __init__(self, *args, info: FormatInfo, **kwargs) -> None:
        self.resolution = info["resolution"]
        self.res = info["res"]
        self.fps = info["frame_rate"]
        self.size = info["size"]
        self.bitrate = info["bitrate"]
        simplified_size: SimplifiedSize = simplify_size(self.size)
        
        super().__init__(*args, **kwargs)
        
        self.configure(corner_radius=10, fg_color="#202020")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=80)
        self.grid_propagate(False)

        self.details_main_window = Frame(self, fg_color="transparent")
        self.details_main_window.grid_rowconfigure(0, weight=3)
        self.details_main_window.grid_rowconfigure(1, weight=2)
        self.details_main_window.grid_columnconfigure(0, weight=1)
        self.details_main_window.grid_propagate(False)

        self.primary_details_window = Frame(self.details_main_window, height=0, fg_color="transparent")
        self.primary_details_window.grid_columnconfigure(0, weight=0, minsize=80)
        self.primary_details_window.grid_columnconfigure((1,2), weight=0)
        self.primary_details_window.grid_rowconfigure(0, weight=1)
        self.primary_details_window.grid_propagate(False)

        self.secondary_details_window = Frame(self.details_main_window, height=0, fg_color="transparent")
        self.secondary_details_window.grid_columnconfigure((0,1), weight=0, minsize=80)
        self.secondary_details_window.grid_rowconfigure(0, weight=0)
        self.secondary_details_window.grid_propagate(False)

        self.res_label = Label(self.primary_details_window, text=f"{self.res}p", justify="left", font=("Segoe UI", 18, "bold"), text_color="white", height=0, width=0, fg_color="transparent")
        self.resolution_label = Label(self.primary_details_window, text=f"{self.resolution}", justify="left", font=("Segoe UI", 14), text_color="white", height=0, width=0, fg_color="transparent")
        self.fps_label = Label(self.primary_details_window, text=f"{self.fps}FPS", justify="left", font=("Segoe UI", 12, "bold"), text_color="white", height=0, width=0, corner_radius=6, fg_color=FormatInfoWindow.fps_color(self.fps))

        self.size_label = Label(self.secondary_details_window, height=0, width=0, text=f"{simplified_size["value"]} {simplified_size["unit"]}", font=("Segoe UI", 12, "bold"))
        self.bitrate_label = Label(self.secondary_details_window, height=0, width=0, text=f"Bitrate: {int(self.bitrate)} kbps", font=("Segoe UI", 12))

        self.download_button = Button(self, text="Download", font=("Segoe UI", 13, "bold"), text_color="white", height=30, width=80, corner_radius=15, fg_color="#D00030")

        self.details_main_window.grid(row=0, column=0, sticky="ewns", padx=(20, 0))

        self.primary_details_window.grid(row=0, column=0, sticky="ewns")
        self.secondary_details_window.grid(row=1, column=0, sticky="ewns")

        self.res_label.grid(column=0, row=0, sticky="w")
        self.resolution_label.grid(column=1, row=0, sticky="w", padx=(0,5))
        self.fps_label.grid(column=2, row=0, sticky="w", ipadx=5, ipady=3)

        self.size_label.grid(column=0, row=0, sticky="wns")
        self.bitrate_label.grid(column=1, row=0, sticky="wns")

        self.download_button.grid(row=0, column=1, sticky="ew", padx=(0,20))

    @staticmethod
    def fps_color(fps: int) -> Literal["#CC3333", "#00cc00", "#e6ac00"]:
        if fps < 30:
            return "#CC3333"
        elif fps < 60:
            return "#00cc00"
        else:
            return "#e6ac00"


class FormatListWindow(Frame):
    child_elements: list[FormatInfoWindow]
    container: ScrollableFrame
    
    def __init__(self, *args, **kwargs) -> None:
        self.child_elements = []
        super().__init__(*args, **kwargs)

        self.container = ScrollableFrame(self, fg_color="transparent")
        self.container._scrollbar.grid_forget()
        self.container.pack(fill="both", expand=True)

    def add(self, info: FormatInfo | list[FormatInfo]) -> None:
        if type(info) == dict:
            new_window = FormatInfoWindow(self.container, info=info, height=60)
            new_window.pack(fill="x", padx=20, pady=5)
            self.child_elements.append(new_window)
        elif type(info) == list:
            self.container.pack_forget()
            for i in info:
                self.add(i)
            self.container.pack(fill="both", expand=True)


    def clear(self) -> None:
        if len(self.child_elements) > 0:
            self.container.pack_forget()
            for widget in self.child_elements:
                widget.pack_forget()
                self.container.after(100, widget.destroy)
            self.child_elements.clear()
            self.container.pack(fill="both", expand=True)


class MainApp(CTk):
    main_frame: Frame
    frame_search: Frame
    frame_results: Frame

    frame_left: Frame
    frame_right: Frame
    
    search_bar: SearchBar
    video_info_window: VideoInfoWindow
    format_info_window: FormatListWindow

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry("1000x700")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = Frame(self, corner_radius=0, fg_color="#141414")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=100)
        self.main_frame.grid_propagate(False)

        self.frame_search = Frame(self.main_frame, height=80, corner_radius=0, fg_color="#383838")
        self.frame_search.grid_columnconfigure((0, 2), weight=1)
        self.frame_search.grid_columnconfigure(1, weight=2)
        self.frame_search.grid_rowconfigure(0, weight=1)
        self.frame_search.grid_propagate(False)

        self.frame_results = Frame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_results.grid_columnconfigure(0, weight=1)
        self.frame_results.grid_columnconfigure(1, weight=0, minsize=420)
        self.frame_results.grid_rowconfigure(0, weight=1)

        self.frame_left = Frame(self.frame_results, corner_radius=0, fg_color="transparent")
        self.frame_left.pack_propagate(False)
        self.frame_right = Frame(self.frame_results, corner_radius=0, fg_color="transparent")


        self.search_bar = SearchBar(self.frame_search, corner_radius=0, fg_color="transparent")
        self.search_bar.on_query += self.search
        
        self.video_info_window = VideoInfoWindow(self.frame_left, fg_color="transparent")
        self.format_info_window = FormatListWindow(self.frame_right, fg_color="transparent")

        self.main_frame.grid(row=0, column=0, sticky="ewns")
        self.frame_search.grid(row=0, column=0, sticky="ewns")
        self.frame_results.grid(row=1, column=0, sticky="ewns")

        self.frame_left.grid(row=0, column=0, sticky="ewns")
        self.frame_right.grid(row=0, column=1, sticky="ewns")

        self.search_bar.grid(row=0, column=1, sticky="ewns")
        self.video_info_window.pack(fill="x", padx=(20,0), pady=50)
        self.format_info_window.pack(fill="both", expand=True, pady=50)

    def _load_thumbnail(self, image: ImageFile) -> None:
        self.video_info_window.set_thumbnail(image)

    def _load_video_info(self, info: VideoInfo) -> None:
        self.video_info_window.set_info(info)

        load_thumbnail = ThumbnailLoader(info["thumbnail"])
        load_thumbnail.on_complete += self._load_thumbnail
        load_thumbnail.run()

    def _load_video_formats(self, info: VideoInfo) -> None:
        self.format_info_window.add(info["formats"])

    def search(self, query: str) -> None:
        if not query == "":
            self.video_info_window.clear()
            self.format_info_window.clear()
            load_info = VideoInfoLoader(query)
            load_info.on_complete += self._load_video_info
            load_info.on_complete += self._load_video_formats
            load_info.on_complete += lambda _: self.search_bar.set_active(True)
            load_info.run()
