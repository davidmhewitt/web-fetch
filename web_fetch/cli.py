import argparse
import asyncio
import os

import aiohttp
import aiofiles


async def write_to_file(filename: str, text: str) -> None:
    """
    Write text to a file asynchronously.
    """
    async with aiofiles.open(filename, "w") as f:
        await f.write(text)

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

async def cli():
    """
    Main CLI entrypoint.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="URLs to fetch")
    parser.add_argument("--output", "-o", help="Output folder", default="/tmp", type=dir_path)
    args = parser.parse_args()

    async with aiohttp.ClientSession() as session:
        fetch_tasks = [fetch(url, session) for url in args.urls]
        for response in asyncio.as_completed(fetch_tasks):
            try:
                response, host = await response
                print(response[:100], "...")
                output_path = args.output
                await write_to_file(f"{output_path}/{host}.html", response)
            except RuntimeError as e:
                print(e)


def main():
    """
    Main entrypoint, runs the CLI in an asyncio event loop.
    """
    asyncio.run(cli())


if __name__ == "__main__":
    main()
