import argparse
import asyncio

async def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="URLs to fetch")
    args = parser.parse_args()
    print(args.urls)

def main():
    asyncio.run(cli())

if __name__ == "__main__":
    main()
