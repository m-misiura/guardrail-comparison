FROM python:3.10.9-slim 

USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY .python-version .

COPY pyproject.toml poetry.lock ./

RUN poetry run pip install --no-cache-dir --use-deprecated=legacy-resolver pystemmer==2.2.0.1 && \
    poetry install --no-root

COPY notebooks /app/notebooks

WORKDIR /app/

CMD ["poetry", "run", "jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]