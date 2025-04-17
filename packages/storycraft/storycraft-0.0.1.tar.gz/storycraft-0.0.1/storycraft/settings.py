import os
from pathlib import Path
import shelve
from pydantic import BaseModel


class Settings(BaseModel):
    auto_save: bool = True
    hide_title: bool = False
    gen_image: bool = False
    markdown_exclude_images: bool = False
    markdown_exclude_outline: bool = False

    @staticmethod
    def __file() -> Path:
        """Return the path to the settings file."""
        return Path.cwd() / ".storycraft"

    @staticmethod
    def fal_api_key_exists() -> bool:
        """Check if the API key exists."""
        if key := os.getenv("FAL_API_KEY"):
            return True
        return os.getenv("FAL_KEY", None) is not None

    @staticmethod
    def load() -> "Settings":
        """Load settings from a file."""
        if not Settings.__file().exists():
            return Settings()
        with shelve.open(Settings.__file()) as db:
            settings = Settings(**db["settings"]) if "settings" in db else Settings()
            if not Settings.fal_api_key_exists():
                settings.gen_image = False
            return settings

    def save(self) -> None:
        """Save settings to a file."""
        with shelve.open(Settings.__file()) as db:
            db["settings"] = self.model_dump()
