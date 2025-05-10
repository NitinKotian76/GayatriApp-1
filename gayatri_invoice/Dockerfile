FROM python:3-slim as builder
WORKDIR /gayatri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1











FROM python:3-slim
WORKDIR /gayatri

COPY gayatriapp/ /gayatri/
COPY poetry.lock /gayatri/
COPY pyproject.toml /gayatri/
COPY entrypoint.sh /gayatri/
COPY settings.py /gayatri/gayatriapp/main/
RUN pip install --upgrade pip \
	&& pip install pipx \
	&& pipx ensurepath
ENV PATH="$PATH:/root/.local/bin"
RUN pipx install poetry==1.8.4
RUN poetry install --only main --no-directory
EXPOSE 8000
ENTRYPOINT ["sh","entrypoint.sh"]
