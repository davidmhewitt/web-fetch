FROM python:3.11-slim
WORKDIR /code
RUN pip install poetry
COPY . /code
RUN poetry install --no-dev
ENTRYPOINT ["poetry", "run", "web-fetch"]