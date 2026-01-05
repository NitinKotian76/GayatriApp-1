FROM python:3.13-slim AS builder
WORKDIR /gayatri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install uv
RUN --mount=type=cache,target=/root/.cache,id=uv_cache \
	python -m pip install uv

COPY requirements.txt /gayatri/requirements.txt

# Install dependencies (no dev dependencies for production)
RUN --mount=type=cache,target=/root/.cache,id=uv_cache \
	uv pip install --system -r /gayatri/requirements.txt

# Copy the rest of the app
COPY ./gayatriapp/ /gayatri/gayatriapp/
COPY entrypoint.sh deploy.sh test.sh /gayatri/
RUN chmod +x /gayatri/*.sh

FROM python:3.13-slim
RUN apt-get update && \
    apt-get install -y gcc libpq-dev \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 libffi-dev shared-mime-info \
    && rm -rf /var/cache/apt/*

RUN useradd -m -r appuser && \
	mkdir /gayatri && \
	chown -R appuser /gayatri

RUN mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app/staticfiles && \
    chmod -R u+rwx /app/staticfiles

WORKDIR /gayatri

# Copy installed dependencies and app from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /gayatri/ /gayatri/

RUN chown -R appuser:appuser /gayatri

USER appuser
EXPOSE 8000
ENTRYPOINT ["/gayatri/entrypoint.sh"]
