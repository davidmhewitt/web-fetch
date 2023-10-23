import argparse
import asyncio
from dataclasses import dataclass
from datetime import datetime
import os

from web_fetch.fetcher import fetch_urls


@dataclass
class Metadata:
    num_links: int
    num_images: int
    host: str
    time_fetched: str = datetime.now().isoformat()


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
    parser.add_argument("--output", "-o", help="Output folder",
                        default="/tmp", type=dir_path)
    parser.add_argument(
        "--metadata", "-m", help="Display metadata for each url fetched", action="store_true")
    args = parser.parse_args()

    results = await fetch_urls(args.urls, args.output)
    if args.metadata:
        metadata = [Metadata(len(result.links), len(result.images), result.host)
                    for result in results]

        print(metadata)


def main():
    """
    Main entrypoint, runs the CLI in an asyncio event loop.
    """
    asyncio.run(cli())


if __name__ == "__main__":
    main()
