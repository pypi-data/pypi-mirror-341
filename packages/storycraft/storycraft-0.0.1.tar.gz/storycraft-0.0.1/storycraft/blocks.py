from enum import Enum
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from storycraft.novel import Novel
from storycraft.project import Project
from storycraft.writer import Writer
from storycraft.settings import Settings


def __autosave() -> bool:
    return Settings.load().auto_save


def __hide_title() -> bool:
    return Settings.load().hide_title


def __gen_image() -> bool:
    return Settings.load().gen_image


def __project() -> tuple[Project, Writer, Novel]:
    p = st.session_state["active_project"]
    return p, p.writer, p.novel


def __get_key(name: str, image=False, title=False) -> str:
    if image:
        return f"{name}.key.image"
    if title:
        return f"{name}.key.title"
    return f"{name}.key"


def __should_expand(gen: bool, key: str) -> bool:
    k = __get_key(key)
    k2 = __get_key(key, image=True)

    return gen or st.session_state.get(k, False) or st.session_state.get(k2, False)


class ReGen:
    def __init__(self, text: bool, image: bool, title: bool, prompt: str | None = None):
        self.text = text
        self.image = image
        self.title = title
        self.prompt = prompt


def __regenerate_button(key: str, image=False, title=False) -> ReGen | None:
    with st.popover(f"Regenerate", icon="✨"):
        if title:
            if st.button(
                "Regenerate Title",
                type="secondary",
                key=__get_key(key, title=True),
                icon="📔",
                use_container_width=True,
            ):
                return ReGen(text=False, image=False, title=True)
        if image:
            disabled = not __gen_image()
            if st.button(
                "Redraw Image",
                type="secondary",
                key=__get_key(key, image=True),
                icon="🏞️",
                use_container_width=True,
                disabled=disabled,
            ):
                return ReGen(text=False, image=True, title=False)
        # prompt = st.text_area(
        #     "Instructions",
        #     key=f"{key}.prompt",
        #     placeholder="Additional instructions for the generation ...",
        #     height=100,
        # )
        if st.button(
            "Regenerate",
            type="secondary",
            key=__get_key(key),
            icon="✨",
            use_container_width=True,
        ):
            return ReGen(text=True, image=True, title=False, prompt=None)
        return None


def __gen_title(title: DeltaGenerator):
    project, writer, novel = __project()
    # Generate
    with title:
        with st.spinner("Generating Title ...", show_time=True):
            writer.gen_title()
            if not __hide_title():
                t = novel.title or "Untitled"
                st.write("### 📔 " + t)
            else:
                st.empty()
    if __autosave() or not novel.title:
        project.save()


def __outline(gen: bool, prompt: str | None = None):
    project, writer, novel = __project()
    # Generate
    if gen:
        st.empty()
        st.write_stream(writer.gen_outline(prompt))
        # writer.gen_title()
        if __autosave() or (novel.outline and not novel.outline.chapters):
            project.save()
    # Render
    assert novel.outline is not None
    outline = novel.outline
    st.write(outline.outline)
    # Update title
    # if gen:
    #     with title:
    #         if not __hide_title():
    #             t = novel.title or "Untitled"
    #             st.write("### 📔 " + t)
    #     if novel.outline and not novel.outline.chapters:
    #         project.save()


def outline_block(gen: bool, title: DeltaGenerator):
    project, writer, novel = __project()
    if gen or novel.outline:
        outdated = (
            not gen
            and novel.outline_is_outdated()
            and not st.session_state.get(__get_key("outline"), False)
        )
        with st.status(
            "_Outline_" + (" :red-badge[Outdated]" if outdated else ""),
            expanded=__should_expand(gen, "outline"),
            state="running" if not outdated else "error",
        ):
            inner_outline = st.empty()
            with inner_outline:
                __outline(gen)
            if regen := __regenerate_button("outline", title=True):
                if regen.text:
                    with inner_outline:
                        __outline(True, prompt=regen.prompt)
                    __gen_title(title)
                    st.rerun()
                if regen.title:
                    __gen_title(title)
                    st.rerun()


def __chapter_outlines(gen: bool, prompt: str | None = None):
    project, writer, novel = __project()
    # Generate
    if gen:
        st.empty()
        st.write_stream(writer.gen_chapter_outlines(prompt))
        if __autosave() or not novel.chapters:
            project.save()
    # Render
    assert novel.outline is not None
    outline = novel.outline
    assert outline.chapters is not None
    with st.container(border=False):
        for i, chapter in enumerate(outline.chapters):
            st.write(f"### {i + 1}. {chapter.title}")
            st.write(chapter.outline)


def chapter_outlines_block(gen: bool):
    project, writer, novel = __project()
    if gen or (novel.outline and novel.outline.chapters):
        outdated = (
            not gen
            and novel.chapter_outline_is_outdated()
            and not st.session_state.get(__get_key("chapter_outlines"), False)
        )
        with st.status(
            "_Chapter Outlines_" + (" :red-badge[Outdated]" if outdated else ""),
            expanded=__should_expand(gen, "chapter_outlines"),
            state="running" if not outdated else "error",
        ):
            inner_outline = st.empty()
            with inner_outline:
                __chapter_outlines(gen)
            if regen := __regenerate_button("chapter_outlines"):
                with inner_outline:
                    __chapter_outlines(True, prompt=regen.prompt)
                    st.rerun()


def __chapter_image(i: int, gen: bool):
    project, writer, novel = __project()
    # Generate
    should_save = __autosave() or (not novel.chapters) or (i == len(novel.chapters))
    if gen:
        st.empty()
        if __gen_image():
            with st.spinner("Generating Image ...", show_time=True):
                if image := writer.gen_chapter_image(i, base64=True):
                    assert novel.chapters is not None
                    chapter = novel.chapters[i]
                    st.image(image.url, use_container_width=True)
                    if should_save:
                        project.save()
    # Render
    assert novel.chapters is not None
    chapter = novel.chapters[i]
    if chapter.image:
        st.image(chapter.image.url, use_container_width=True)


def __chapter(i: int, gen: bool, prompt: str | None = None):
    project, writer, novel = __project()
    # Generate
    should_save = __autosave() or (not novel.chapters) or (i == len(novel.chapters))
    if gen:
        st.empty()
        with st.container(border=False):
            st.write_stream(writer.gen_chapter(i, prompt))
            if not __gen_image():
                assert novel.chapters is not None
                chapter = novel.chapters[i]
                chapter.image = None
            if should_save:
                project.save()
    # Render
    assert novel.chapters is not None
    chapter = novel.chapters[i]
    st.write(chapter.content)


def chapter_block(i: int, gen: bool):
    project, writer, novel = __project()
    assert novel.outline is not None
    if gen or i < len(novel.outline.chapters or []):
        assert novel.outline and novel.outline.chapters
        outdated = (
            not gen
            and novel.chapter_is_outdated(i)
            and not st.session_state.get(__get_key(f"chapter.{i}"), False)
        )
        if not gen and novel.chapters and i < len(novel.chapters):
            title = novel.chapters[i].title
        elif i >= len(novel.outline.chapters):
            if novel.chapters and i < len(novel.chapters):
                title = novel.chapters[i].title
            else:
                title = f"..."
        else:
            title = novel.outline.chapters[i].title
        with st.status(
            f"**{i + 1}\\. {title}**" + (" :red-badge[Outdated]" if outdated else ""),
            expanded=__should_expand(gen, f"chapter.{i}"),
            state="running" if not outdated else "error",
        ):
            inner_image = st.empty()
            inner_content = st.empty()
            if not st.session_state.get(__get_key(f"chapter.{i}"), False):
                with inner_content:
                    __chapter(i, gen)
                with inner_image:
                    __chapter_image(i, gen)
            if i < len(novel.outline.chapters):
                if regen := __regenerate_button(f"chapter.{i}", image=True):
                    if regen.text:
                        with inner_content:
                            __chapter(i, True, prompt=regen.prompt)
                    if regen.image:
                        with inner_image:
                            __chapter_image(i, True)
                    st.rerun()
            else:
                if st.button(
                    "Delete", icon=":material/delete:", key=f"chapter.{i}.button.delete"
                ):
                    novel.delete_chapter(i)
                    if __autosave():
                        project.save()
                    st.rerun()
