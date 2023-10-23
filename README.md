# web-fetch

## Usage 

The included Dockerfile is built and published to GHCR using a GitHub action, so the application can be run with:
```
docker run ghcr.io/davidmhewitt/web-fetch:main [urls]
```

For example:

```
docker run ghcr.io/davidmhewitt/web-fetch:main https://www.google.com http://neverssl.com
```

To build and run the Docker container manually:

```
docker build . -t web-fetch
docker run web-fetch [urls]
```

## Development Time

- 0.5 hours, repository setup and Docker build and push
- 1 hour, URL fetch and save to disk, plus basic HTML parsing