FROM python:3.13-slim AS builder
WORKDIR /gayatri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Copy only poetry files first for better caching
COPY pyproject.toml poetry.lock /gayatri/

# Install dependencies (no dev dependencies for production)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy the rest of the app
COPY gayatriapp/ /gayatri/gayatriapp/
COPY entrypoint.sh /gayatri/
COPY settings.py /gayatri/gayatriapp/main/

FROM python:3.13-slim
RUN useradd -m -r appuser && \
	mkdir /gayatri && \
	chown -R appuser /gayatri
WORKDIR /gayatri

# Copy installed dependencies and app from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /gayatri/ /gayatri/

USER appuser
EXPOSE 8000
ENTRYPOINT ["sh","entrypoint.sh"]
