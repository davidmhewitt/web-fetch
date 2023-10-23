import argparse
import asyncio
import os

from web_fetch.fetcher import fetch_urls


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

    await fetch_urls(args.urls, args.output, args.metadata)


def main():
    """
    Main entrypoint, runs the CLI in an asyncio event loop.
    """
    asyncio.run(cli())


if __name__ == "__main__":
    main()
