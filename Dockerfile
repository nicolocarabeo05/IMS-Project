FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
RUN python manage.py collectstatic --no-input

COPY docker-entrypoint.sh /usr/local/bin

RUN chmod 777 /usr/local/bin/docker-entrypoint.sh \
    && ln -s /usr/local/bin/docker-entrypoint.sh /

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["runprod"]