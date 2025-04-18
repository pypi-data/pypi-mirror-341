from __future__ import annotations

import asyncio
from contextlib import suppress
from http import HTTPStatus
from typing import Any

import backoff
import httpx
from html2text import HTML2Text

with suppress(ImportError):
    from playwright.async_api import Browser, async_playwright

from .cleanup import cleanup_page

MAX_TRIES: int = 3
MAX_TIMEOUT: int = 60
REQUEST_TIMEOUT: int = 10


async def __download_via_request(
    page_url: str,
    *,
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

    return response.text


async def __download_via_browser(
    page_url: str,
    *,
    user_agent: str | None = None,
) -> str | None:
    async with async_playwright() as playwright:
        browser: Browser = await playwright.chromium.launch()
        await browser.new_context(
            user_agent=user_agent,
        )

        page = await browser.new_page()
        response = await page.goto(page_url)
        if not response:
            return None
        if response.status == HTTPStatus.TOO_MANY_REQUESTS:
            # It also triggers backoff if necessary
            return None

        html: str = await page.content()

        await browser.close()

    return html


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
    use_browser: bool = False,
) -> str | None:
    page_html: str | None = await (
        __download_via_browser if use_browser
        else __download_via_request
    )(page_url, user_agent=user_agent)
    if page_html is None:
        return page_html

    if cleanup:
        page_html = await cleanup_page(page_html)

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
