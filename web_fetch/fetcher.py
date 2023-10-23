import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import aiofiles
import aiohttp

from web_fetch.html_parser import HTMLParser


@dataclass
class Metadata:
    num_links: int
    num_images: int
    host: str
    time_fetched: str = datetime.now().isoformat()


@dataclass
class FetchResult:
    body: str
    host: str
    metadata: Optional[Metadata] = None


async def write_to_file(filename: str, text: str) -> None:
    """
    Write text to a file asynchronously.
    """
    try:
        async with aiofiles.open(filename, "w") as f:
            await f.write(text)
    except Exception as e:
        raise RuntimeError(f"Failed to write to {filename}: {e}") from e


async def fetch(url: str, session: aiohttp.ClientSession, fetch_metadata: bool) -> FetchResult:
    """
    Fetch a URL and return a tuple of the response text and the HTTP host that
    returned the response (useful for identifying the request).

    :param url: URL to fetch
    :param session: aiohttp session
    :param fetch_metadata: whether to fetch metadata
    :return: FetchResult containing the response text and host
    :raises RuntimeError: if the URL could not be fetched
    """
    try:
        async with session.get(url) as response:
            if response.status >= 400:
                raise RuntimeError(f"Failed to fetch {url}: {response.status}")

            text = await response.text()

            metadata = None
            if fetch_metadata:
                parser = HTMLParser(text)
                links = parser.get_links()
                images = parser.get_images()
                metadata = Metadata(len(links), len(images), response.host)

            return FetchResult(text, response.host, metadata)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}") from e


async def fetch_urls(urls: list[str], output_path: str, fetch_metadata: bool) -> list[FetchResult]:
    """
    Fetch a list of URLs and write the responses to files.

    :param urls: URLs to fetch
    :param output_path: path to folder to write files into
    :param fetch_metadata: whether to fetch metadata
    :return: list of results
    """
    responses = []

    async with aiohttp.ClientSession() as session:
        fetch_tasks = [fetch(url, session, fetch_metadata) for url in urls]
        for response in asyncio.as_completed(fetch_tasks):
            try:
                response = await response
                responses.append(response)
                await write_to_file(f"{output_path}/{response.host}.html", response.body)
            except RuntimeError as e:
                print(e)

    return responses
