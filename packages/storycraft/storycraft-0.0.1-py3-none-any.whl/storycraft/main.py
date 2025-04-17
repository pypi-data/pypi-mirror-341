import os
from typing import Annotated
import typer
from pathlib import Path
import streamlit.web.bootstrap
import rich

from storycraft.novel import DEFAULT_LANGUAGE, Novel
from .writer import Writer


app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings=dict(help_option_names=["-h", "--help"]),
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


def __check_env(image: bool = False) -> None:
    if "OPENROUTER_API_KEY" not in os.environ:
        rich.print(
            f"[bold red]ERROR:[/bold red] [red]OPENROUTER_API_KEY is not set in your environment.[/red]"
        )
        raise typer.Abort()
    if "FAL_API_KEY" not in os.environ and "FAL_KEY" not in os.environ:
        color = "red" if image else "yellow"
        label = "ERROR" if image else "WARNING"
        rich.print(
            f"[bold {color}]{label}:[/bold {color}] [{color}]FAL_KEY or FAL_API_KEY is not set in your environment. Image generation is disabled.\nPlease create an API key at https://fal.ai/dashboard/keys[/{color}]"
        )
        if image:
            raise typer.Abort()


@app.command(help="Generate a novel")
def gen(
    prompt_file: Path,
    language: Annotated[
        str,
        typer.Option("--language", "--lang", "-l", help="The language of the novel"),
    ] = DEFAULT_LANGUAGE,
    out: Annotated[
        Path | None, typer.Option("--out", "-o", help="The output file")
    ] = None,
    images: Annotated[
        bool,
        typer.Option(
            "--images",
            "-i",
            help="Generate images while writing novels",
        ),
    ] = False,
    embed_images: Annotated[
        bool,
        typer.Option(
            "--embed-images",
            "-e",
            help="Embed images as base64 URLs in the markdown file. By default temporary web URLs are used and are valid for ~7 days.",
        ),
    ] = False,
):
    __check_env(image=images)

    if not prompt_file.is_file():
        rich.print(
            f"[bold red]ERROR:[/bold red] [red]{prompt_file} is not a file.[/red]"
        )
        raise typer.Abort()

    if not out:
        out = prompt_file.with_suffix(".out.md")

    prompt = prompt_file.read_text()
    novel = Novel(title=prompt_file.stem, instructions=prompt, language=language)
    writer = Writer(novel)

    with open(out, "w+", encoding="utf-8") as f:
        for s in writer.gen_outline_with_title():
            print(s, end="", flush=True, file=f)

    md = novel.render_markdown()
    with open(out, "w+", encoding="utf-8") as f:
        f.write(md)
        print("## Chapter Outlines\n", file=f)
        for s in writer.gen_chapter_outlines():
            print(s, end="", flush=True, file=f)

    md = novel.render_markdown()
    with open(out, "w+", encoding="utf-8") as f:
        f.write(md)
        num_chapters = writer.num_chapters()
        outline = writer.get_outline()
        assert outline.chapters is not None, "No chapters found"
        assert num_chapters is not None, "No chapters found"
        print("---\n", file=f)
        print("# MAIN CONTENT\n", file=f)
        for c in range(num_chapters):
            print("---\n", file=f)
            print(f"# {c + 1}. {outline.chapters[c].title}\n", file=f)
            for s in writer.gen_chapter(c):
                print(s, end="", flush=True, file=f)
            print("\n", flush=True, file=f)
            if images:
                if image := writer.gen_chapter_image(c, base64=embed_images):
                    assert novel.chapters is not None
                    label = image.prompt or "Image"
                    print(f"\n![{label}]({image.url})\n", flush=True, file=f)
            print("\n", flush=True, file=f)

    md = novel.render_markdown()
    with open(out, "w+", encoding="utf-8") as f:
        f.write(md)


@app.command(help="Start the web app server")
def serve(port: int = 8501, dev: bool = False):
    __check_env()
    entry = Path(__file__).parent / "app.py"
    streamlit.web.bootstrap.load_config_options(
        flag_options={
            "server.port": port,
            "server.fileWatcherType": "auto" if dev else "none",
            "runner.magicEnabled": False,
        }
    )
    if pp := os.environ.get("PYTHONPATH"):
        os.environ["PYTHONPATH"] = f"{pp}:{entry.parent}"
    else:
        os.environ["PYTHONPATH"] = str(entry.parent)
    # if not dev:
    os.environ["STREAMLIT_CLIENT_SHOW_ERROR_DETAILS"] = "type"

    streamlit.web.bootstrap.run(str(entry), False, [], {})


def main():
    app()
