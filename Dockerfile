FROM python:3.11-slim

WORKDIR /app

COPY setup.py /app/
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -e .

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "AniAlert/bot.py"]
