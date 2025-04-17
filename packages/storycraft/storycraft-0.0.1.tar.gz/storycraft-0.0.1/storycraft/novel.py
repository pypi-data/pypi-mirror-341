from io import StringIO
import os
from pydantic import BaseModel, Field


class ChapterOutline(BaseModel):
    title: str = Field(
        ..., description="The title of the chapter, without ordinal or chapter number"
    )
    outline: str = Field(..., description="The outline of the chapter")


class Outline(BaseModel):
    outline: str
    chapters: list[ChapterOutline] | None = None
    outline_timestamp: float = 0
    chapter_timestamp: float = 0


class ChapterImage(BaseModel):
    url: str
    prompt: str
    content_type: str


class Chapter(BaseModel):
    title: str
    content: str
    timestamp: float = 0
    image: ChapterImage | None = None


DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE") or "English"


class Novel(BaseModel):
    title: str | None = Field(default=None, description="The title of the novel.")
    language: str = Field(
        default=DEFAULT_LANGUAGE, description="The language of the novel."
    )
    instructions: str = Field(..., description="The instructions for the novel.")
    instructions_timestamp: float = 0
    outline: Outline | None = Field(
        default=None, description="The outline of the novel."
    )
    chapters: list[Chapter] | None = Field(
        default=None,
        description="The list of chapters in the novel. Each chapter is a string.",
    )

    def delete_chapter(self, index: int) -> None:
        """Delete a chapter by index."""
        if self.chapters is None:
            return
        if index < 0 or index >= len(self.chapters):
            return
        del self.chapters[index]

    def is_empty(self) -> bool:
        return self.outline is None and self.chapters is None

    def is_complete(self) -> bool:
        """Check if the novel is complete."""
        if (
            self.outline is None
            or self.chapters is None
            or self.outline.chapters is None
        ):
            return False
        if len(self.outline.chapters) != len(self.chapters):
            return False
        for chapter in self.chapters:
            if chapter == "":
                return False
        if self.outline_is_outdated():
            return False
        if self.chapter_outline_is_outdated():
            return False
        if self.any_chapter_is_outdated():
            return False
        return True

    def outline_is_outdated(self) -> bool:
        """Check if the outline is outdated."""
        if self.outline is None:
            return True
        return self.instructions_timestamp > self.outline.outline_timestamp

    def chapter_outline_is_outdated(self) -> bool:
        """Check if the chapter outline is outdated."""
        if self.outline is None:
            return True
        if self.outline_is_outdated():
            return True
        return self.outline.outline_timestamp > self.outline.chapter_timestamp

    def any_chapter_is_outdated(self) -> bool:
        """Check if the chapter outline is outdated."""
        if self.outline is None or self.outline.chapters is None:
            return True
        if self.chapter_outline_is_outdated():
            return True
        if self.chapters is None:
            return True
        if len(self.outline.chapters) != len(self.chapters):
            return True
        for i in range(len(self.outline.chapters)):
            if self.chapter_is_outdated(i):
                return True
        return False

    def chapter_is_outdated(self, index: int) -> bool:
        """Check if the chapter is outdated."""
        if self.outline is None or self.outline.chapters is None:
            return True
        if self.chapter_outline_is_outdated():
            return True
        if index < 0 or index >= len(self.outline.chapters):
            return True
        if self.chapters is None or index >= len(self.chapters):
            return True
        return self.outline.chapter_timestamp > self.chapters[index].timestamp

    def first_invalid_chapter(self) -> int | None:
        if self.outline is None or self.outline.chapters is None:
            return 0
        if self.chapters is None:
            return 0
        for i in range(len(self.outline.chapters)):
            if i >= len(self.chapters):
                return i
            if self.chapter_is_outdated(i):
                return i
        print(
            "first_invalid_chapter",
            len(self.outline.chapters),
            len(self.chapters),
        )
        return None

    def invalid_chapters(self) -> list[int]:
        assert self.outline is not None
        assert self.outline.chapters is not None
        result = []
        for i in range(len(self.outline.chapters)):
            if i >= len(self.chapters or []):
                result.append(i)
            if self.chapter_is_outdated(i):
                result.append(i)
        return result

    def render_markdown(self, no_outline=False, no_images=False) -> str:
        """Render the novel as a markdown string."""
        with StringIO() as f:
            if self.title:
                f.write("# " + self.title + "\n\n")
            else:
                f.write("# Untitled\n\n")
            if self.outline and not no_outline:
                f.write("---\n\n")
                f.write("# OUTLINE\n\n")
                f.write(self.outline.outline + "\n\n")
                if self.outline.chapters:
                    f.write("## Chapter Outlines\n\n")
                    for i, chapter in enumerate(self.outline.chapters):
                        f.write(f"### {i + 1}. {chapter.title}\n\n")
                        f.write(chapter.outline + "\n\n")
            if self.chapters:
                f.write("---\n\n")
                if not no_outline:
                    f.write("# MAIN CONTENT\n\n")
                for i, c in enumerate(self.chapters):
                    f.write("---\n\n")
                    f.write(f"# {i + 1}. {c.title}\n\n")
                    if c.image and not no_images:
                        label = c.image.prompt or "Image"
                        f.write(f"![{label}]({c.image})\n\n")
                    f.write(c.content + "\n\n")
            return f.getvalue()
