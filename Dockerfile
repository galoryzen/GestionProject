FROM python:3.9

RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./bot.py" ]
