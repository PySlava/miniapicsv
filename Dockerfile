FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /code
RUN apt-get update && apt-get install -y build-essential gcc wget
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /usr/local/bin/wait-for-it && chmod +x /usr/local/bin/wait-for-it
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
RUN mkdir -p /code/media
CMD ["gunicorn", "baseapi.wsgi:application", "--bind", "0.0.0.0:8000"]
