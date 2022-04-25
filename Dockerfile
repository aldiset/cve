FROM tiangolo/uvicorn-gunicorn:python3.8

RUN pip3 install pipenv

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system

COPY . /app
ENV PYTHONPATH=/app

CMD ["alembic","upgrade","head"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9999"]

EXPOSE 3030