import copy
import json
import os
import time
from typing import Any, AsyncGenerator, TypeVar
from jinja2 import Environment, FileSystemLoader, select_autoescape
import typer
import asyncio
from pathlib import Path
from agentia import Agent
from agentia.chat_completion import ChatCompletion, MessageStream
from pydantic import BaseModel, Field

from storycraft.imgen import generate_image
from storycraft.novel import Chapter, ChapterImage, Novel, Outline, ChapterOutline

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings=dict(help_option_names=["-h", "--help"]),
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)

STRUCTURIZATION_PROMPT = """
Restructure the following text into json. Restructure and transform faithfully, don't change, add, or delete any text.
"""


T = TypeVar("T", bound=BaseModel)


class Writer:
    def __init__(self, novel: Novel) -> None:
        self.novel = novel
        self.__terminate = False
        self.__env = Environment(
            loader=FileSystemLoader(Path(__file__).parent / "prompts"),
            autoescape=select_autoescape(),
        )
        self.__generation_model = os.getenv("MODEL", "deepseek/deepseek-chat-v3-0324")
        self.__structurization_model = os.getenv(
            "STRUCTURIZATION_MODEL", "openai/gpt-4o-mini"
        )
        self.__loop: asyncio.AbstractEventLoop | None = None

    def num_chapters(self) -> int | None:
        assert self.novel.outline is not None
        assert self.novel.outline.chapters is not None
        return len(self.novel.outline.chapters)

    def get_outline(self) -> Outline:
        assert self.novel.outline is not None
        return self.novel.outline

    def __gen_prompt(self, template: str, variables: dict[str, Any]):
        t = self.__env.get_template(template)
        prompt = t.render(**variables)
        return prompt

    def __create_agent(
        self, outline: Outline | None = None, title=True, procedural=False
    ):
        variables: dict[str, Any] = {
            "user_instructions": self.novel.instructions,
            "language": self.novel.language,
        }
        if title:
            variables["title"] = self.novel.title
        if outline:
            variables["outline"] = outline
        instructions = self.__gen_prompt("instructions.md", variables)

        def end_of_output():
            """Use this tool to indicate the end of output."""
            self.__terminate = True
            return "DONE"

        tools: list[Any] = []
        if procedural:
            tools.append(end_of_output)

        return Agent(
            model=self.__generation_model,
            instructions=instructions,
            tools=tools,
        )

    def __gen_sync(self, completion: ChatCompletion[MessageStream]):
        if self.__loop is None:
            self.__loop = asyncio.new_event_loop()

        def to_sync_gen(
            loop: asyncio.AbstractEventLoop, async_gen: AsyncGenerator[str, None]
        ):
            while True:
                try:
                    yield loop.run_until_complete(anext(async_gen))
                except StopAsyncIteration:
                    break

        async def gen_async(completion: ChatCompletion[MessageStream]):
            async for res in completion:
                async for chunk in res:
                    yield chunk

        yield from to_sync_gen(self.__loop, gen_async(completion))

    def __run_completion(
        self, completion: ChatCompletion[MessageStream], procedural: bool = True
    ):
        content = ""
        for s in self.__gen_sync(completion):
            content += s
            yield s

        if procedural:
            iterations = 0
            for i in range(5):
                self.__terminate = False
                # print(f"[CONTINUE {i}]")
                iterations += 1
                c = completion.agent.chat_completion(
                    "Continue, or call the `end_of_output` tool if you are finished. Don't write anything more if the current content is finished.",
                    stream=True,
                )
                for s in self.__gen_sync(c):
                    content += s
                    yield s
                if self.__terminate:
                    break
            print(f"[DONE: {len(content)}B, {iterations + 1} iterations]")
        return content

    def __run_agent(
        self,
        prompt: str,
        *,
        outline: Outline | None = None,
        procedural: bool = False,
        title=True,
    ):
        agent = self.__create_agent(outline=outline, title=title, procedural=procedural)
        completion = agent.chat_completion(prompt, stream=True)
        val = yield from self.__run_completion(completion, procedural)
        return val

    def __gen_structurized(self, text: str, schema: type[T]) -> T:
        agent = Agent(
            model=self.__structurization_model,
            instructions=STRUCTURIZATION_PROMPT.strip(),
        )
        completion = agent.chat_completion(text, response_format=schema)

        async def get_message(completion: ChatCompletion):
            x = await completion
            return x.content or ""

        result = asyncio.run(get_message(completion))
        data = json.loads(result)
        return schema(**data)

    def gen_outline(self, prompt: str | None = None):
        instructions = self.novel.instructions
        if prompt is not None and prompt.strip() == "":
            prompt = None
        if prompt is not None:
            instructions = instructions + "\n\n" + prompt
        prompt = self.__gen_prompt("outline.md", {"user_instructions": instructions})
        result = yield from self.__run_agent(prompt, procedural=False, title=False)
        result = result.strip("- \n\t")
        if self.novel.outline:
            self.novel.outline.outline = result
        else:
            self.novel.outline = Outline(outline=result)
        self.novel.outline.outline_timestamp = time.time()

    def gen_outline_with_title(self):
        prompt = self.__gen_prompt(
            "outline-with-title.md", {"user_instructions": self.novel.instructions}
        )
        result = yield from self.__run_agent(prompt, procedural=False, title=False)

        class OutlineWithTitle(BaseModel):
            title: str = Field(..., description="The title of the doc")
            content: str = Field(
                ..., description="All the remaining content of the doc"
            )

        owt = self.__gen_structurized(result, OutlineWithTitle)
        self.novel.title = owt.title
        if self.novel.outline:
            self.novel.outline.outline = owt.content
        else:
            self.novel.outline = Outline(outline=owt.content)
        self.novel.outline.outline_timestamp = time.time()

    def gen_title(self):
        prompt = self.__gen_prompt("title.md", {})
        result = ""
        for s in self.__run_agent(prompt, procedural=False, title=False):
            result += s
        # print(f"[TITLE] {result}")
        self.novel.title = result.strip()

    def gen_chapter_outlines(self, prompt: str | None = None):
        assert self.novel.outline is not None
        if prompt is not None and prompt.strip() == "":
            prompt = None
        prompt = self.__gen_prompt("extended-outline.md", {"prompt": prompt})
        outline = copy.deepcopy(self.novel.outline)
        outline.chapters = None
        result = yield from self.__run_agent(prompt, outline=outline, procedural=False)

        class ChapterOutlines(BaseModel):
            chapters: list[ChapterOutline] = Field(
                ..., description="The list of chapters in the outline"
            )

        sos = self.__gen_structurized(result, ChapterOutlines)
        self.novel.outline.chapters = sos.chapters
        self.novel.outline.chapter_timestamp = time.time()

    def gen_chapter(self, index: int, prompt: str | None = None):
        assert self.novel.outline is not None
        assert self.novel.outline.chapters is not None
        assert index < len(self.novel.outline.chapters)
        if index > 0:
            assert self.novel.chapters is not None
            assert index <= len(self.novel.chapters)

        chapter_outline = self.novel.outline.chapters[index]
        if prompt is not None and prompt.strip() == "":
            prompt = None
        chapter_size = 1000
        if v := os.getenv("CHAPTER_SIZE"):
            match v.strip().lower():
                case "short" | "small":
                    chapter_size = 200
                case "medium":
                    chapter_size = 500
                case "long" | "large":
                    chapter_size = 1000
                case _:
                    pass
        prompt = self.__gen_prompt(
            "chapter-content.md",
            {
                "index": index,
                "title": chapter_outline.title,
                "outline": chapter_outline.outline,
                "prompt": prompt,
                "chapter_size": chapter_size,
            },
        )
        result = yield from self.__run_agent(
            prompt, outline=self.novel.outline, procedural=False
        )
        result = result.strip("- \n\t")
        if self.novel.chapters is None:
            self.novel.chapters = []
        chapter = Chapter(
            title=chapter_outline.title,
            content=result,
        )
        if index >= len(self.novel.chapters):
            self.novel.chapters.append(chapter)
        else:
            self.novel.chapters[index] = chapter
        self.novel.chapters[index].timestamp = time.time()

    def gen_chapter_image(self, index: int, *, base64: bool) -> ChapterImage | None:
        assert self.novel.outline is not None
        assert self.novel.outline.chapters is not None
        assert index < len(self.novel.outline.chapters)
        assert self.novel.chapters is not None
        assert index < len(self.novel.chapters)
        chapter_outline = self.novel.outline.chapters[index]
        chapter = self.novel.chapters[index]
        if self.__loop is None:
            self.__loop = asyncio.new_event_loop()
        self.__loop.run_until_complete(
            generate_image(self.novel, chapter_outline, chapter, base64=base64)
        )
        return chapter.image
