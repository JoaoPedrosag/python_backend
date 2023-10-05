FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code


# Instale as dependências
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copie o projeto para o contêiner
COPY . /code/