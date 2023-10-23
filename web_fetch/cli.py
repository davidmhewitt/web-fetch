import argparse
import asyncio
import os

import aiofiles
import aiohttp
from web_fetch.html_parser import HTMLParser


async def write_to_file(filename: str, text: str) -> None:
    """
    Write text to a file asynchronously.
    """
    try:
        async with aiofiles.open(filename, "w") as f:
            await f.write(text)
    except Exception as e:
        raise RuntimeError(f"Failed to write to {filename}: {e}") from e

async def fetch(url: str, session: aiohttp.ClientSession) -> tuple[str, str]:
    """
    Fetch a URL and return a tuple of the response text and the HTTP host that
    returned the response (useful for identifying the request).

    :param url: URL to fetch
    :param session: aiohttp session
    :return: response text
    :raises RuntimeError: if the URL could not be fetched
    """
    try:
        async with session.get(url) as response:
            if response.status >= 400:
                raise RuntimeError(f"Failed to fetch {url}: {response.status}")

            return (await response.text(), response.host)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}") from e


def dir_path(path: str) -> str:
    """
    Check if a path is a valid directory.

    :param path: path to check
    :return: path if valid
    :raises argparse.ArgumentTypeError: if the path is not a valid directory
    """
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"{path} is not a valid directory")

    return path

async def fetch_urls(urls: list[str], output_path: str) -> None:
    """
    Fetch a list of URLs and write the responses to files.

    :param urls: URLs to fetch
    :param output_path: path to folder to write files into
    """
    async with aiohttp.ClientSession() as session:
        fetch_tasks = [fetch(url, session) for url in urls]
        for response in asyncio.as_completed(fetch_tasks):
            try:
                response, host = await response
                parser = HTMLParser(response)
                links = parser.get_links()
                images = parser.get_images()
                print(f"Found {len(links)} links and {len(images)} images on {host}")
                await write_to_file(f"{output_path}/{host}.html", response)
            except RuntimeError as e:
                print(e)

async def cli():
    """
    Main CLI entrypoint.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="URLs to fetch")
    parser.add_argument("--output", "-o", help="Output folder", default="/tmp", type=dir_path)
    args = parser.parse_args()

    await fetch_urls(args.urls, args.output)


def main():
    """
    Main entrypoint, runs the CLI in an asyncio event loop.
    """
    asyncio.run(cli())


if __name__ == "__main__":
    main()
