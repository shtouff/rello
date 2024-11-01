FROM library/python:3.12-slim

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt rello.py /app/

RUN pip install -r requirements.txt

EXPOSE 8000

USER nobody

ENTRYPOINT ["fastapi", "run", "rello.py"]

LABEL name=rello
LABEL version=0.2
