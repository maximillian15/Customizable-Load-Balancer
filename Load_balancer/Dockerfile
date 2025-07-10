FROM python:3.9-slim

WORKDIR /app

COPY balancer.py .
COPY consistent_hash.py .

RUN pip install flask requests docker

EXPOSE 5000

CMD ["python", "balancer.py"]