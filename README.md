# Back-end TCC 3

Este projeto Django atua como o backend de um aplicativo de envio de áudios. O sistema é capaz de receber arquivos de áudio, convertê-los para o formato AAC e, em seguida, transcrever o áudio para texto. Tanto o áudio convertido quanto o texto transcrito são armazenados para acesso posterior.

## Funcionalidades

- **Recebimento de Áudio:** O sistema aceita o upload de arquivos de áudio enviados pelo aplicativo.
- **Conversão para AAC:** Após o recebimento, o áudio é automaticamente convertido para o formato AAC, otimizando a compatibilidade e o armazenamento.
- **Transcrição de Áudio:** Utilizando tecnologias de reconhecimento de voz, o sistema converte o conteúdo de áudio em texto.
- **Armazenamento:** Tanto o áudio convertido quanto o texto transcrito são armazenados para que possam ser acessados e utilizados conforme a necessidade.

## Pré-requisitos

- Python (3.11.3)
- PostgreSQL
- Redis

## Para instalar as libs

```bash
pip install -r requirements.txt
```

## Executando o Projeto
1. Inicie o serviço Celery para tarefas em background:
```bash
celery -A django_back worker --pool=solo -l info
```

2. Em outro terminal, inicie o servidor Django:

```bash
python manage.py runserver 0.0.0.0:8000
```
