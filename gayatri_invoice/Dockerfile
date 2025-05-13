FROM python:3.13-slim AS builder
WORKDIR /gayatri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /gayatri/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /gayatri/requirements.txt

FROM python:3.13-slim
RUN useradd -m -r appuser && \
	mkdir /gayatri && \
	chown -R appuser /gayatri
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
WORKDIR /gayatri
COPY --chown=appuser:appuser gayatriapp/ /gayatri/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY entrypoint.sh /gayatri/
COPY settings.py /gayatri/gayatriapp/main/
USER appuser
EXPOSE 8000
ENTRYPOINT ["sh","entrypoint.sh"]
