# web-fetch

## Description

Python application to fetch and save web pages. Currently supports saving the HTML and images from a page. `<img>` `src` attributes are re-written to point to the local copy of the image.

Could be further extended to support downloading other assets locally, such as CSS and JavaScript files.

Arguments:
- `--metadata`: Print JSON output to the console with information about the number of images and links on the page
- `--output`: Save the downloaded files to the specified directory

## Requirements

Tested with Python 3.11, but some earlier Python 3 versions should work. Poetry is used for dependency management. To install the dependencies, run:

```
poetry install
```

## Usage 

The included Dockerfile is built and published to GHCR using a GitHub action, so the application can be run with:
```
docker run ghcr.io/davidmhewitt/web-fetch:main [urls]
```

For example:

```
docker run ghcr.io/davidmhewitt/web-fetch:main --metadata https://www.google.com http://github.com
```

By default, the downloaded files are saved to the /tmp directory, so they will be within the container. To create a volume that the container can save the downloaded files into so they are accessible on the host, run the container with the `-v` flag. For example:

```
docker run -v ${PWD}/output:/output ghcr.io/davidmhewitt/web-fetch:main -o /output --metadata https://www.google.com http://github.com
```

Downloaded files will be saved to the `output` directory on the host. The usual issues with Docker filesystem permissions will probably apply. The `--metadata` flag is optional.

To build and run the Docker container manually:

```
docker build . -t web-fetch
docker run web-fetch [urls]
```

## Development Time

- 0.5 hours, repository setup and Docker build and push
- 1 hour, URL fetch and save to disk, plus basic HTML parsing
- 1.5 hours, refactoring metadata fetching and adding image saving