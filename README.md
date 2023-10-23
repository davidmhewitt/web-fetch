# web-fetch

## Running 

The included Dockerfile is built and published to GHCR using a GitHub action, so the application can be run with:
```
docker run ghcr.io/davidmhewitt/web-fetch:main
```

To build and run the Docker container manually:

```
docker build . -t web-fetch
docker run web-fetch
```