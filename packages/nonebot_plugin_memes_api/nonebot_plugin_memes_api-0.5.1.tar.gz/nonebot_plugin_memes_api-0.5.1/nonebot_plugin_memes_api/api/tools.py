from typing import Literal

from nonebot.compat import model_dump, type_validate_python
from pydantic import BaseModel

from . import ImageResponse, get_image, send_request


class MemeProperties(BaseModel):
    disabled: bool = False
    hot: bool = False
    new: bool = False


class RenderMemeListParams(BaseModel):
    meme_properties: dict[str, MemeProperties]
    exclude_memes: list[str]
    sort_by: Literal[
        "key", "keywords", "keywords_pinyin", "date_created", "date_modified"
    ]
    sort_reverse: bool
    text_template: str
    add_category_icon: bool


async def render_meme_list(
    meme_properties: dict[str, MemeProperties] = {},
    exclude_memes: list[str] = [],
    sort_by: Literal[
        "key", "keywords", "keywords_pinyin", "date_created", "date_modified"
    ] = "keywords_pinyin",
    sort_reverse: bool = False,
    text_template: str = "{index}. {keywords}",
    add_category_icon: bool = True,
) -> bytes:
    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/render_list",
            "POST",
            "JSON",
            json=model_dump(
                RenderMemeListParams(
                    meme_properties=meme_properties,
                    exclude_memes=exclude_memes,
                    sort_by=sort_by,
                    sort_reverse=sort_reverse,
                    text_template=text_template,
                    add_category_icon=add_category_icon,
                )
            ),
        ),
    ).image_id
    return await get_image(image_id)


class RenderMemeStatisticsParams(BaseModel):
    title: str
    statistics_type: Literal["meme_count", "time_count"]
    data: list[tuple[str, int]]


async def render_meme_statistics(
    title: str,
    statistics_type: Literal["meme_count", "time_count"],
    data: list[tuple[str, int]],
) -> bytes:
    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/render_statistics",
            "POST",
            "JSON",
            json=model_dump(
                RenderMemeStatisticsParams(
                    title=title, statistics_type=statistics_type, data=data
                )
            ),
        ),
    ).image_id
    return await get_image(image_id)
