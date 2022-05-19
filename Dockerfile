FROM python:3.8.13-slim

RUN pip3 install pipenv

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system

COPY . /app
ENV PYTHONPATH=/app
CMD [""]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9999"]

EXPOSE 9999