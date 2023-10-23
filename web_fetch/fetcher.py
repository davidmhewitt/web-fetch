import asyncio
from dataclasses import dataclass

import aiofiles
import aiohttp

from web_fetch.html_parser import HTMLParser


@dataclass
class FetchResult:
    body: str
    host: str
    images: list[str]
    links: list[str]


async def write_to_file(filename: str, text: str) -> None:
    """
    Write text to a file asynchronously.
    """
    try:
        async with aiofiles.open(filename, "w") as f:
            await f.write(text)
    except Exception as e:
        raise RuntimeError(f"Failed to write to {filename}: {e}") from e


async def fetch(url: str, session: aiohttp.ClientSession) -> FetchResult:
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
            parser = HTMLParser(text, url)
            links = parser.get_links()
            images = parser.get_images()

            return FetchResult(text, response.host, images, links)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}") from e


async def fetch_urls(urls: list[str], output_path: str) -> list[FetchResult]:
    """
    Fetch a list of URLs and write the responses to files.

    :param urls: URLs to fetch
    :param output_path: path to folder to write files into
    :param fetch_metadata: whether to fetch metadata
    :return: list of results
    """
    responses = []

    async with aiohttp.ClientSession() as session:
        fetch_tasks = [fetch(url, session) for url in urls]
        for response in asyncio.as_completed(fetch_tasks):
            try:
                response = await response
                for image in response.images:
                    print(f"Fetching {image}")
                responses.append(response)
                await write_to_file(f"{output_path}/{response.host}.html", response.body)
            except RuntimeError as e:
                print(e)

    return responses
