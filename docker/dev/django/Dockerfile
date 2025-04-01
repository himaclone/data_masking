FROM python:3.10.12-slim-buster
ENV PYTHONWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /code
RUN apt update 
RUN mkdir requirements
COPY requirements/ /code/requirements
RUN pip install --upgrade pip && pip install -r requirements/dev.txt

COPY docker/dev/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY . /code

ENTRYPOINT ["/entrypoint"]
