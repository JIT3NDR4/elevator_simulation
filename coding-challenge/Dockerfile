FROM python:3.9-slim

WORKDIR /app

EXPOSE 8000

COPY ./code/requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY ./code .

CMD [ "python", "app.py" ]

