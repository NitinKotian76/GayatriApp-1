FROM python:3-slim
WORKDIR /gayatriapp
COPY gayatriapp/* /
COPY poetry.lock /
COPY pyproject.toml /
COPY deploy/entrypoint.sh /
RUN pip install --upgrade pip \
	&& pip install pipx \
	&& pipx ensurepath
ENV PATH="$PATH:/root/.local/bin"
RUN pipx install poetry==1.8.4
RUN poetry install --only main --no-directory
EXPOSE 8000
ENTRYPOINT ["sh","/entrypoint.sh"]
