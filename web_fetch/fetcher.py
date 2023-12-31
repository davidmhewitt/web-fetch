import asyncio
import os
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


async def save_image(url: str, output_path: str, session: aiohttp.ClientSession) -> None:
    """
    Save an image from a URL to disk.

    :param url: URL to fetch
    :param output_path: path to folder to write files into
    :param session: aiohttp session
    :raises RuntimeError: if the URL could not be fetched
    """
    try:
        async with session.get(url) as response:
            if response.status >= 400:
                raise RuntimeError(f"Failed to fetch {url}: {response.status}")

            url_filename = url.split("/")[-1]
            async with aiofiles.open(os.path.join(output_path, url_filename), "wb") as f:
                await f.write(await response.read())
    except Exception as e:
        raise RuntimeError(f"Failed to fetch image {url}: {e}") from e


async def fetch(url: str, output_path: str, session: aiohttp.ClientSession) -> FetchResult:
    """
    Fetch a URL and return a tuple of the response text and the HTTP host that
    returned the response (useful for identifying the request).

    :param url: URL to fetch
    :param output_path: path to folder to write files into
    :param session: aiohttp session
    :return: FetchResult containing the response text and host
    :raises RuntimeError: if the URL could not be fetched
    """
    try:
        async with session.get(url) as response:
            if response.status >= 400:
                raise RuntimeError(f"Failed to fetch {url}: {response.status}")

            # make a directory for any assets
            relative_assets_path = f"{response.host}_assets"
            try:
                os.mkdir(os.path.join(output_path, relative_assets_path))
            except FileExistsError:
                pass

            text = await response.text()
            parser = HTMLParser(text, url, relative_assets_path)
            links = parser.get_links()
            images = parser.get_images()

            image_tasks = [save_image(image, os.path.join(
                output_path, relative_assets_path), session) for image in images]

            image_results = await asyncio.gather(*image_tasks, return_exceptions=True)
            for result in image_results:
                if isinstance(result, Exception):
                    print(result)

            await write_to_file(os.path.join(output_path, f"{response.host}.html"), parser.replace_image_urls())

            return FetchResult(text, response.host, images, links)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}") from e


async def fetch_urls(urls: list[str], output_path: str) -> list[FetchResult]:
    """
    Fetch a list of URLs and save the pages to disk.

    :param urls: URLs to fetch
    :param output_path: path to folder to write files into
    :return: list of results
    """
    responses = []

    async with aiohttp.ClientSession() as session:
        fetch_tasks = [fetch(url, output_path, session) for url in urls]
        fetch_results = await asyncio.gather(*fetch_tasks)
        for result in fetch_results:
            if isinstance(result, Exception):
                print(result)
            else:
                responses.append(result)

    return responses
