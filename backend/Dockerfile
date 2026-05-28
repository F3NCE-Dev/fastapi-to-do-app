FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x prestart.sh
RUN chmod +x run.py

ENTRYPOINT [ "./prestart.sh" ]
CMD [ "python", "run.py" ]
