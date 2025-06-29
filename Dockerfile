FROM python:3.9-slim AS builder
WORKDIR /install

RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev libmariadb-dev pkg-config ca-certificates

COPY requirements.txt .

RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt --prefix=/install

FROM python:3.9-slim
WORKDIR /app

COPY --from=builder /install /usr/local

COPY static/ static/
COPY templates/ templates/
COPY app.py dbcontext.py person.py ./

EXPOSE 5000
CMD ["python3", "app.py"]
