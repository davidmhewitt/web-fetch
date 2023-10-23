import argparse


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="URLs to fetch")
    args = parser.parse_args()
    print(args.urls)


if __name__ == "__main__":
    cli()
