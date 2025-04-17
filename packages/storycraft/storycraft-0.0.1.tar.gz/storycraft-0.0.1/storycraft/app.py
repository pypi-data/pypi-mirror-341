import copy
import os
import time
import streamlit as st
import storycraft.blocks as blocks
from storycraft.novel import DEFAULT_LANGUAGE
from storycraft.project import Project
import dotenv

from storycraft.settings import Settings

st.set_page_config(
    page_title="StoryCraft",
    page_icon=":book:",
)

dotenv.load_dotenv()

# Projects

PROJECTS = st.session_state["projects"] = Project.get_projects(
    st.session_state.get("projects")
)
PROJECT_LIST = sorted(list(PROJECTS.values()), key=lambda x: x.title or "")

if not st.session_state.get("project"):
    first = next(iter(PROJECT_LIST), None)
    pid = st.query_params.get("project", "")
    st.session_state["project"] = PROJECTS.get(pid) or first


def new_project():
    st.write("### Create a new novel:")
    name = st.text_input("The novel name (optional):", placeholder="Untitled").strip()
    if st.button("Create"):
        try:
            st.query_params["project"] = Project.create(name)
            del st.session_state["project"]
            st.rerun()
        except Exception as e:
            st.error(str(e))


if len(PROJECTS) == 0:
    new_project()
    st.stop()


@st.dialog(title="New Project")
def new_project_dialog():
    new_project()


@st.dialog(title="Delete Project")
def delete_project_dialog(project: Project):
    st.write(f"### Delete: _{project.title}_?")
    st.write("This action cannot be undone.")
    # st.caption(f"Project ID: `{project.id}`")
    if st.button("Delete", icon=":material/delete:"):
        try:
            Project.delete(project.id)
            st.session_state.clear()
            del st.query_params["project"]
            st.rerun()
        except Exception as e:
            st.error(str(e))


with st.sidebar:
    # Select a project
    selected_project = st.selectbox(
        "Select a project:",
        options=PROJECT_LIST,
        key="project",
        format_func=lambda x: x.title or "Untitled",
    )
    st.query_params["project"] = selected_project.id
    if (
        "active_project" not in st.session_state
        or st.session_state["active_project"].id != selected_project.id
    ):
        st.session_state["active_project"] = selected_project
        st.session_state["user_instructions"] = selected_project.novel.instructions
        st.session_state["language"] = selected_project.novel.language
    project: Project = st.session_state["active_project"]
    # Create or remove project
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "New", icon=":material/add:", type="secondary", use_container_width=True
        ):
            new_project_dialog()
    with col2:
        if st.button(
            "Delete",
            icon=":material/delete:",
            type="secondary",
            use_container_width=True,
        ):
            delete_project_dialog(project)

    writer = project.writer
    novel = project.novel

    initial_novel = copy.deepcopy(project.novel)

    st.divider()

    st.session_state.setdefault("user_instructions", project.novel.instructions)
    user_instructions = st.text_area(
        "Description",
        key="user_instructions",
        placeholder="The description of the book, and/or other instructions ...",
        height=300,
    )

    st.session_state.setdefault("language", project.novel.language)
    language = st.text_input(
        "Language", key="language", placeholder=DEFAULT_LANGUAGE
    ).strip()

    changed = (
        user_instructions != project.novel.instructions
        or language != project.novel.language
    )

    save = st.button(
        "Save", icon=":material/save:", use_container_width=True, disabled=not changed
    )

    gen_all = st.button(
        (
            "Save & Generate"
            if changed
            else ("Regenerate" if project.novel.outline else "Generate")
        ),
        icon="✨",
        type="primary",
        use_container_width=True,
    )

    if save or gen_all:
        new_user_instructions = user_instructions.strip()
        new_language = language.strip()
        if (
            new_user_instructions != project.novel.instructions
            or new_language != project.novel.language
        ):
            project.novel.instructions = user_instructions.strip()
            project.novel.language = language.strip()
            project.novel.instructions_timestamp = time.time()
            project.save()
        st.toast(":green-badge[:material/check:]&nbsp;&nbsp;Saved successfully!")

    st.divider()

    with st.expander("Settings", expanded=False, icon=":material/settings:"):
        settings = Settings.load()
        if "autosave" not in st.session_state:
            st.session_state["autosave"] = settings.auto_save
        AUTOSAVE = st.toggle(
            "Auto Save",
            key="autosave",
            help="Automatically save the newly generated content.",
        )
        if "hide_title" not in st.session_state:
            st.session_state["hide_title"] = settings.hide_title
        HIDE_TITLE = st.toggle("Hide Title", key="hide_title", help="Hide the title.")
        if "gen_image" not in st.session_state:
            st.session_state["gen_image"] = settings.gen_image
        api_key_exists = Settings.fal_api_key_exists()
        if not api_key_exists:
            st.session_state["gen_image"] = False
        GEN_IMAGE = st.toggle(
            "Generate Images",
            key="gen_image",
            help="Generate images at the end of each chapter. You need to set `FAL_KEY` to use this feature.",
            disabled=not api_key_exists,
        )
        new_settings = Settings(
            auto_save=AUTOSAVE, hide_title=HIDE_TITLE, gen_image=GEN_IMAGE
        )
        if "markdown_exclude_outline" not in st.session_state:
            st.session_state["markdown_exclude_outline"] = (
                settings.markdown_exclude_outline
            )
        new_settings.markdown_exclude_outline = st.toggle(
            "Download: Exclude Outline",
            key="markdown_exclude_outline",
            help="Download the novel without outline.",
        )
        if "markdown_exclude_images" not in st.session_state:
            st.session_state["markdown_exclude_images"] = (
                settings.markdown_exclude_images
            )
        new_settings.markdown_exclude_images = st.toggle(
            "Download: Exclude Images",
            key="markdown_exclude_images",
            help="Download the novel without images.",
        )
        if new_settings != settings:
            new_settings.save()


title_block = st.empty()
with title_block:
    if not HIDE_TITLE:
        title = novel.title or "Untitled"
        st.write("### 📔 " + title)

gen_outline = False
gen_chapter_outlines = False
gen_all_chapters = False
gen_chapters: list[bool] | None = None
delete_residual = False

with st.popover("**AI**", icon="✨"):
    if st.button(
        "Regenerate All" if not novel.is_empty() else "Generate All",
        type="primary",
        icon="✨",
        use_container_width=True,
    ):
        gen_all = True
        delete_residual = True
    if not novel.is_complete():
        # st.divider()
        if not novel.outline or novel.outline_is_outdated():
            st.write("Next Step: Outline")
        elif not novel.outline.chapters or novel.chapter_outline_is_outdated():
            st.write("Next Step: Chapter Outlines")
        elif novel.any_chapter_is_outdated():
            if (i := novel.first_invalid_chapter()) is not None:
                title = novel.outline.chapters[i].title
                st.write(f"Next Step: **{i + 1}\\. {title}**")
            else:
                st.write(f"Next Step: Delete Stale Chapters")
        if st.button(
            "Generate **One** Step",
            type="primary",
            icon="✨",
            use_container_width=True,
        ):
            if not novel.outline or novel.outline_is_outdated():
                gen_outline = True
            elif not novel.outline.chapters or novel.chapter_outline_is_outdated():
                gen_chapter_outlines = True
            elif novel.any_chapter_is_outdated():
                if (i := novel.first_invalid_chapter()) is not None:
                    if gen_chapters is None:
                        gen_chapters = [False] * len(novel.outline.chapters)
                    gen_chapters[i] = True
                else:
                    delete_residual = True
        if st.button(
            "Generate *All Incomplete* Steps",
            type="primary",
            icon="✨",
            use_container_width=True,
        ):
            if not novel.outline or novel.outline_is_outdated():
                gen_outline = True
            if (
                not novel.outline
                or not novel.outline.chapters
                or novel.chapter_outline_is_outdated()
            ):
                gen_chapter_outlines = True
            if not novel.outline or not novel.outline.chapters:
                gen_all_chapters = True
            else:
                ivs = novel.invalid_chapters()
                gen_chapters = [False] * len(novel.outline.chapters)
                for x in ivs:
                    gen_chapters[x] = True
            delete_residual = True


# Outline
blocks.outline_block(gen_all or gen_outline, title_block)

# Chapter Outlines
blocks.chapter_outlines_block(gen_all or gen_chapter_outlines)

# Chapters
if (novel.outline and novel.outline.chapters) or novel.chapters:
    if novel.outline and novel.outline.chapters:
        num_chapters = max(len(novel.outline.chapters), len(novel.chapters or []))
    else:
        num_chapters = len(novel.chapters or [])
    for i in range(num_chapters):
        gen = gen_all
        if not gen and gen_chapters and i < len(gen_chapters):
            gen = gen_chapters[i]
        if not gen and gen_all_chapters:
            gen = True
        blocks.chapter_block(i, gen)

if delete_residual:
    if novel.outline and novel.outline.chapters and novel.chapters:
        novel.chapters = novel.chapters[: len(novel.outline.chapters)]
    if AUTOSAVE:
        project.save()

# Save and download

col1, col2, _ = st.columns([1, 1, 2])

with col1:
    if st.button("Save", icon=":material/save:", key="save2", use_container_width=True):
        project.save()
        st.toast(":green-badge[:material/check:]&nbsp;&nbsp;Saved successfully!")

with col2:
    project.save()
    markdown_file = project.markdown_file
    data = markdown_file.read_text(encoding="utf-8") if markdown_file.exists() else ""
    st.download_button(
        "Download",
        icon=":material/download:",
        data=data,
        file_name=f"novel.md",
        use_container_width=True,
        disabled=not markdown_file.exists(),
    )

if any(
    [
        gen_all,
        gen_outline,
        gen_chapter_outlines,
        gen_all_chapters,
        delete_residual,
        *(gen_chapters or []),
    ]
):
    st.rerun()
