FROM python:slim

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --system --deploy 

WORKDIR /app/src
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

CMD ["python","bot_affinity/__init__.py"]
