import base64
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, Optional, Union, cast, overload

import httpx
from nonebot.compat import type_validate_python
from pydantic import BaseModel

from ..config import memes_config
from ..exception import (
    DeserializeError,
    ImageAssetMissing,
    ImageDecodeError,
    ImageEncodeError,
    ImageNumberMismatch,
    IOError,
    MemeFeedback,
    MemeGeneratorException,
    RequestError,
    TextNumberMismatch,
    TextOverLength,
)

BASE_URL = memes_config.meme_generator_base_url


@overload
async def send_request(
    router: str,
    request_type: Literal["POST", "GET"],
    response_type: Literal["JSON"],
    **kwargs,
) -> Union[dict[str, Any], list[Any]]: ...


@overload
async def send_request(
    router: str,
    request_type: Literal["POST", "GET"],
    response_type: Literal["BYTES"],
    **kwargs,
) -> bytes: ...


@overload
async def send_request(
    router: str,
    request_type: Literal["POST", "GET"],
    response_type: Literal["TEXT"],
    **kwargs,
) -> str: ...


async def send_request(
    router: str,
    request_type: Literal["POST", "GET"],
    response_type: Literal["JSON", "BYTES", "TEXT"],
    **kwargs,
):
    async with httpx.AsyncClient(timeout=60) as client:
        request_method = client.post if request_type == "POST" else client.get
        resp = await request_method(BASE_URL + router, **kwargs)

        status_code = resp.status_code
        if status_code == 200:
            if response_type == "JSON":
                return resp.json()
            elif response_type == "BYTES":
                return resp.content
            else:
                return resp.text

        elif status_code == 500:
            result = resp.json()
            code: int = result["code"]
            message: str = result["message"]
            data: dict = result["data"]
            if code == 410:
                error = data["error"]
                raise RequestError(message, error)
            elif code == 420:
                error = data["error"]
                raise IOError(message, error)
            elif code == 510:
                error = data["error"]
                raise ImageDecodeError(message, error)
            elif code == 520:
                error = data["error"]
                raise ImageEncodeError(message, error)
            elif code == 530:
                path = data["path"]
                raise ImageAssetMissing(message, path)
            elif code == 540:
                error = data["error"]
                raise DeserializeError(message, error)
            elif code == 550:
                min = data["min"]
                max = data["max"]
                actual = data["actual"]
                raise ImageNumberMismatch(message, min, max, actual)
            elif code == 551:
                min = data["min"]
                max = data["max"]
                actual = data["actual"]
                raise TextNumberMismatch(message, min, max, actual)
            elif code == 560:
                text = data["text"]
                raise TextOverLength(message, text)
            elif code == 570:
                feedback = data["feedback"]
                raise MemeFeedback(message, feedback)
            else:
                raise MemeGeneratorException(message)

        else:
            resp.raise_for_status()


class ImageResponse(BaseModel):
    image_id: str


class ImagesResponse(BaseModel):
    image_ids: list[str]


async def upload_image(image: bytes) -> str:
    payload = {"type": "data", "data": base64.b64encode(image).decode()}

    return type_validate_python(
        ImageResponse, await send_request("/image/upload", "POST", "JSON", json=payload)
    ).image_id


async def get_image(image_id: str) -> bytes:
    return await send_request(f"/image/{image_id}", "GET", "BYTES")


async def get_version() -> str:
    return cast(str, await send_request("/meme/version", "GET", "TEXT"))


async def get_meme_keys() -> list[str]:
    return cast(list[str], await send_request("/meme/keys", "GET", "JSON"))


async def search_memes(query: str, include_tags: bool = False) -> list[str]:
    return cast(
        list[str],
        await send_request(
            "/meme/search",
            "GET",
            "JSON",
            params={"query": query, "include_tags": include_tags},
        ),
    )


class ParserFlags(BaseModel):
    short: bool
    long: bool
    short_aliases: list[str]
    long_aliases: list[str]


class MemeBoolean(BaseModel):
    name: str
    type: Literal["boolean", "string", "integer", "float"]
    description: Optional[str]
    parser_flags: ParserFlags


class BooleanOption(MemeBoolean):
    type: Literal["boolean"]
    default: Optional[bool]


class StringOption(MemeBoolean):
    type: Literal["string"]
    default: Optional[str]
    choices: Optional[list[str]]


class IntegerOption(MemeBoolean):
    type: Literal["integer"]
    default: Optional[int]
    minimum: Optional[int]
    maximum: Optional[int]


class FloatOption(MemeBoolean):
    type: Literal["float"]
    default: Optional[float]
    minimum: Optional[float]
    maximum: Optional[float]


class MemeParams(BaseModel):
    min_images: int
    max_images: int
    min_texts: int
    max_texts: int
    default_texts: list[str]
    options: list[Union[BooleanOption, StringOption, IntegerOption, FloatOption]]


class MemeShortcut(BaseModel):
    pattern: str
    humanized: Optional[str]
    names: list[str]
    texts: list[str]
    options: dict[str, Union[bool, str, int, float]]


class MemeInfo(BaseModel):
    key: str
    params: MemeParams
    keywords: list[str]
    shortcuts: list[MemeShortcut]
    tags: set[str]
    date_created: datetime
    date_modified: datetime


async def get_meme_info(meme_key: str) -> MemeInfo:
    return type_validate_python(
        MemeInfo, await send_request(f"/memes/{meme_key}/info", "GET", "JSON")
    )


async def get_meme_infos() -> list[MemeInfo]:
    resp = cast(
        list[dict[str, Any]],
        await send_request("/meme/infos", "GET", "JSON"),
    )
    return [type_validate_python(MemeInfo, meme_info) for meme_info in resp]


async def generate_meme_preview(meme_key: str) -> bytes:
    image_id = type_validate_python(
        ImageResponse, await send_request(f"/memes/{meme_key}/preview", "GET", "JSON")
    ).image_id
    return await get_image(image_id)


@dataclass
class Image:
    name: str
    data: bytes


async def generate_meme(
    meme_key: str,
    images: list[Image],
    texts: list[str],
    options: dict[str, Union[bool, str, int, float]],
) -> bytes:
    image_dicts: list[dict[str, str]] = []

    for image in images:
        image_id = await upload_image(image.data)
        image_dicts.append({"name": image.name, "id": image_id})

    payload = {"images": image_dicts, "texts": texts, "options": options}
    image_id = type_validate_python(
        ImageResponse,
        await send_request(f"/memes/{meme_key}", "POST", "JSON", json=payload),
    ).image_id
    return await get_image(image_id)


@dataclass
class Meme:
    key: str
    _info: MemeInfo

    @property
    def info(self) -> MemeInfo:
        return deepcopy(self._info)

    async def generate(
        self,
        images: list[Image],
        texts: list[str],
        options: dict[str, Union[bool, str, int, float]],
    ) -> bytes:
        return await generate_meme(self.key, images, texts, options)

    async def generate_preview(self) -> bytes:
        return await generate_meme_preview(self.key)


async def get_memes() -> list[Meme]:
    meme_infos = await get_meme_infos()
    return [Meme(info.key, info) for info in meme_infos]
