FROM downloads.unstructured.io/unstructured-io/unstructured:latest

WORKDIR /src

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

CMD ["python", "main.py"]
