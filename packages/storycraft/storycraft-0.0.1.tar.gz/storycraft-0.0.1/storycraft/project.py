from dataclasses import dataclass
from pathlib import Path
import shutil
from typing import cast
import shortuuid
import slugify
import yaml
from datetime import datetime
import time


from storycraft.novel import Novel
from storycraft.writer import Writer
from storycraft.settings import Settings

PROJECTS_DIR = Path.cwd() / "projects"


class Project:
    def __init__(self, id: str, load_time: float) -> None:
        self.id = id
        self.__load_time = load_time
        self.__initial_title = self.__load_title()
        # Load novel
        self.__writer: Writer | None = None

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Project):
            return False
        return self.id == value.id

    @property
    def title(self) -> str | None:
        if self.__writer is not None:
            return self.writer.novel.title
        return self.__initial_title

    @property
    def novel(self) -> Novel:
        self.__load_novel()
        assert self.__writer is not None
        return self.__writer.novel

    @property
    def markdown_file(self) -> Path:
        """Get the markdown file path."""
        return PROJECTS_DIR / self.id / "novel.md"

    @property
    def writer(self) -> Writer:
        self.__load_novel()
        assert self.__writer is not None
        return self.__writer

    @property
    def dir(self) -> Path:
        """Get the project directory."""
        return PROJECTS_DIR / self.id

    def __load_title(self):
        config_file = PROJECTS_DIR / self.id / "craft.yaml"
        doc = yaml.safe_load(config_file.read_text())
        if "title" in doc:
            return cast(str, doc["title"])
        else:
            return None

    def __load_novel(self) -> None:
        if self.__writer is not None:
            return
        config_file = PROJECTS_DIR / self.id / "craft.yaml"
        doc = yaml.safe_load(config_file.read_text())
        novel = Novel(**doc)
        self.__writer = Writer(novel)

    @staticmethod
    def create(title: str) -> str:
        """Create a new project."""
        title = title.strip()
        title_opt = None if title == "" else title
        id = slugify.slugify(shortuuid.uuid()[:8]).strip()
        path = PROJECTS_DIR / id
        assert not path.exists()
        path.mkdir(parents=True, exist_ok=True)
        config_file = path / "craft.yaml"
        novel = Novel(title=title_opt, instructions="", outline=None, chapters=None)
        config_file.write_text(yaml.dump(novel.model_dump(), allow_unicode=True))
        return id

    @staticmethod
    def delete(id: str) -> None:
        """Delete an existing project."""
        path = PROJECTS_DIR / id
        if not path.exists():
            return
        shutil.rmtree(path)

    @staticmethod
    def get_projects(current: dict[str, "Project"] | None) -> dict[str, "Project"]:
        """Get the list of projects."""
        PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
        projects = current or {}
        for p in PROJECTS_DIR.iterdir():
            if p.is_dir():
                config_file = p / "craft.yaml"
                if config_file.exists():
                    # modified_time = config_file.stat().st_mtime
                    project = Project(id=p.name, load_time=time.time())
                    if project.id not in projects:
                        projects[project.id] = project
                    # elif modified_time > projects[project.id].__load_time:
                    #     print(f"Reloading project {project.id} ...")
                    #     projects[project.id] = project
        return projects

    def save(self, no_outline: bool = False, no_images: bool = False) -> None:
        """Save the project."""
        assert self.__writer is not None
        novel = self.__writer.novel
        config_file = PROJECTS_DIR / self.id / "craft.yaml"
        config_file.write_text(yaml.dump(novel.model_dump(), allow_unicode=True))
        settings = Settings.load()

        # Save the novel as a markdown file
        md_file = PROJECTS_DIR / self.id / "novel.md"

        markdown = self.novel.render_markdown(
            no_outline=settings.markdown_exclude_outline,
            no_images=settings.markdown_exclude_images,
        )
        with open(md_file, "w+", encoding="utf-8") as f:
            f.write(markdown)
