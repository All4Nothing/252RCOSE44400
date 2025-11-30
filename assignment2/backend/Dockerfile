FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask
RUN mkdir /data
EXPOSE 5001
CMD ["python", "app.py"]