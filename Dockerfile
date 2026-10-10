FROM library/python:3.12-slim

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt /app/
COPY rello/ /app/rello/

RUN \
    pip install -U pip setuptools && \
    pip install -r requirements.txt && \
    rm -f requirements.txt

EXPOSE 8000

USER nobody

ENTRYPOINT ["fastapi", "run", "rello/main.py"]

