FROM python:3.10
WORKDIR /app
COPY app/ .
COPY versions/ ./versions/
RUN pip install flask pytest
CMD ["python","app.py"]

