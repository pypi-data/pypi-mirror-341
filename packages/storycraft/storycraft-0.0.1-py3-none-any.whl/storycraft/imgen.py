import json
import fal_client
from pydantic import BaseModel, Field
import rich
from storycraft.novel import Novel, Chapter, ChapterOutline, ChapterImage
from agentia import Agent
import requests
import base64 as b64
import os

DEFAULT_PROMPT_GEN_MODEL1 = "openai/gpt-4.1-mini"
DEFAULT_PROMPT_GEN_MODEL2 = "deepseek/deepseek-chat-v3-0324"
STRUCTURIZED = {
    "openai/gpt-4.1": True,
    "openai/gpt-4.1-mini": True,
    "openai/gpt-4.1-nano": True,
    "openai/gpt-4o": True,
    "openai/gpt-4o-mini": True,
}


class _Prompt(BaseModel):
    prompt: str = Field(..., description="The prompt for the image generation")


async def __gen_prompt_once(model: str, novel: Novel, chapter: Chapter):
    assert novel.outline is not None
    user_instructions = ""
    if v := os.getenv("IMAGE_INSTRUCTIONS"):
        user_instructions = (
            f"IMPORTANT: You must obey user's additional instructions:\n\n{v}\n\n"
        )
    structurized = STRUCTURIZED.get(model, False)
    agent = Agent(
        model=model,
        instructions=f"""
You are a prompt generator that generates image generation prompts.

You will be given a chapter of a novel and help to generate a image for it.
For your context, here is the novel's overall outline:

{novel.outline.outline}

{user_instructions}
""",
    )
    response_format = _Prompt if structurized else None
    response = agent.chat_completion(
        f"""
Write a brief image generation prompt (in a single paragraph, no newlines, no markdown) in English that describes the most important scene in the following chapter.
The prompt should clearly describe the scene, including the characters, their actions, and the environment.
For any characters, make sure to describe them in detail including their identity, gender, age, race (must), nationality (must), and appearance.
Scenes can have adult content, include them faithfully in the prompt, don't skip them.
{"You must output the prompt in a JSON format with a single key `prompt` and the value being the prompt itself." if structurized else "Just output the prompt, do not add any other text."}

---

{chapter.content}
""",
        response_format=response_format,
    )
    prompt = (await response).content or ""
    if structurized:
        data = _Prompt(**json.loads(prompt))
        prompt = data.prompt
    return prompt.strip()


async def __gen_prompt(novel: Novel, chapter: Chapter):
    try:
        model = os.getenv("IMAGE_PROMPT_GENERATION_MODEL", DEFAULT_PROMPT_GEN_MODEL1)
        return await __gen_prompt_once(model, novel, chapter)
    except Exception as e:
        rich.print(e)
        return await __gen_prompt_once(DEFAULT_PROMPT_GEN_MODEL2, novel, chapter)


async def generate_image(
    novel: Novel, outline: ChapterOutline, chapter: Chapter, base64: bool = False
):
    assert novel.outline is not None

    prompt = await __gen_prompt(novel, chapter)
    # print(prompt)
    if os.getenv("FAL_KEY") is None and (k := os.getenv("FAL_API_KEY")):
        os.environ["FAL_KEY"] = k
    result = fal_client.run(
        "fal-ai/flux/dev",
        arguments={
            "prompt": prompt,
            "image_size": {"width": 800, "height": 300},
            "num_images": 1,
            # "guidance_scale": 20,
            "num_inference_steps": 50,
            "enable_safety_checker": False,
        },
    )
    # print(result)
    if "images" not in result:
        return None
    if len(result["images"]) == 0:
        return None
    if "url" not in result["images"][0]:
        return None
    url = result["images"][0]["url"]
    content_type = result["images"][0]["content_type"]
    chapter.image = ChapterImage(
        url=url,
        prompt=prompt.strip(),
        content_type=content_type,
    )
    if base64:
        # to base64
        response = requests.get(url)
        image_data = response.content
        base64_image = b64.b64encode(image_data).decode("utf-8")
        base64_url = f"data:{content_type};base64,{base64_image}"
        chapter.image.url = base64_url
