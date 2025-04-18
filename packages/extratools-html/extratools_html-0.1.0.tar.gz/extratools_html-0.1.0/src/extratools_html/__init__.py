from __future__ import annotations

import asyncio
from http import HTTPStatus
from typing import Any

import backoff
import httpx
from html2text import HTML2Text

from .cleanup import cleanup_page

MAX_TRIES: int = 3
MAX_TIMEOUT: int = 60
REQUEST_TIMEOUT: int = 10


@backoff.on_predicate(
    backoff.expo,
    max_tries=MAX_TRIES,
    max_time=MAX_TIMEOUT,
)
async def download_page_async(
    page_url: str,
    *,
    cleanup: bool = False,
    text_only: bool = False,
    user_agent: str | None = None,
) -> str | None:
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(
            page_url,
            follow_redirects=True,
            timeout=REQUEST_TIMEOUT,
            headers=(
                {
                    "User-Agent": user_agent,
                } if user_agent
                else {}
            ),
        )

    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        # It also triggers backoff if necessary
        return None

    response.raise_for_status()

    page_html: str = response.text

    if cleanup:
        page_html: str = await cleanup_page(page_html)

    if text_only:
        h = HTML2Text()
        h.ignore_images = True
        h.ignore_links = True
        return h.handle(page_html)

    return page_html


def download_page(
    image_url: str,
    **kwargs: Any,
) -> str | None:
    return asyncio.run(download_page_async(
        image_url,
        **kwargs,
    ))
