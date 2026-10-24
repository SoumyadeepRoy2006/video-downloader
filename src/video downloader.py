from modules.widgets import MainApp
from pathlib import Path

try:
    MainApp(download_location=Path(__file__).parent / "downloads").mainloop()
except KeyboardInterrupt:
    pass
