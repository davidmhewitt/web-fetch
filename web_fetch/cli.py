import argparse
import asyncio

import aiohttp


async def fetch(url: str, session: aiohttp.ClientSession) -> str:
    """
    Fetch a URL and return the response text.

    :param url: URL to fetch
    :param session: aiohttp session
    :return: response text
    :raises RuntimeError: if the URL could not be fetched
    """
    try:
        async with session.get(url) as response:
            if response.status >= 400:
                raise RuntimeError(f"Failed to fetch {url}: {response.status}")

            return await response.text()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}") from e


async def cli():
    """
    Main CLI entrypoint.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="URLs to fetch")
    args = parser.parse_args()

    async with aiohttp.ClientSession() as session:
        fetch_tasks = [fetch(url, session) for url in args.urls]
        for response in asyncio.as_completed(fetch_tasks):
            try:
                print((await response)[:100], "...")
            except RuntimeError as e:
                print(e)


def main():
    """
    Main entrypoint, runs the CLI in an asyncio event loop.
    """
    asyncio.run(cli())


if __name__ == "__main__":
    main()
