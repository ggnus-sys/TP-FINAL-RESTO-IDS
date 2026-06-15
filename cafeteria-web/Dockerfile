FROM python:3.11.9

WORKDIR /web-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5001

EXPOSE 5001

EXPOSE 8000

CMD ["python", "app.py"]