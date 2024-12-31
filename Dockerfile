FROM python:3-slim
WORKDIR /gayatriapp
COPY ../gayatriapp ../poetry.lock ../pyproject.toml /
COPY ../deploy/entrypoint.sh /
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     python3-dev \
#     gcc \
#     g++ \
#     && rm -rf /var/lib/apt/lists/*
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install pipx -y
RUN pipx ensurepath
ENV PATH="$PATH:/root/.local/bin"
RUN pipx install poetry==1.8.4
RUN poetry install --only main --no-directory 
EXPOSE 8000
ENTRYPOINT ["sh","/entrypoint.sh"]
